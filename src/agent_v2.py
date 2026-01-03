"""New agent implementation with Supabase and multiple AI models."""

import json
import time
import uuid
from dataclasses import dataclass
from enum import Enum
from typing import AsyncGenerator

from baml_client.sync_client import BamlSyncClient, b
from baml_client.types import Message as ConvoMessage

from .code_executor import code_executor
from .database import db


class MessageType(Enum):
    INIT = "init"
    USER = "user"
    AGENT_PARTIAL = "agent_partial"
    AGENT_FINAL = "agent_final"
    LOAD_CODE = "load_code"
    EDIT_CODE = "edit_code"
    UPDATE_IN_PROGRESS = "update_in_progress"
    UPDATE_FILE = "update_file"
    UPDATE_COMPLETED = "update_completed"


@dataclass
class Message:
    id: str
    timestamp: int
    type: MessageType
    data: dict
    session_id: str

    @classmethod
    def new(
        cls,
        type: MessageType,
        data: dict,
        id: str | None = None,
        session_id: str | None = None,
    ) -> "Message":
        return cls(
            type=type,
            data=data,
            id=id or str(uuid.uuid4()),
            timestamp=time.time_ns() // 1_000_000,
            session_id=session_id or str(uuid.uuid4()),
        )

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "type": self.type.value,
            "data": self.data,
            "timestamp": self.timestamp,
            "session_id": self.session_id,
        }


class Agent:
    """Agent that uses multiple AI models and Supabase for storage."""

    def __init__(self):
        self.model_client: BamlSyncClient = b

    async def init(self, session_id: str) -> bool:
        """Initialize a new session."""
        # Check if session exists in database
        existing_session = db.get_session(session_id)
        exists = existing_session is not None

        if not exists:
            # Create session in database
            db.create_session(session_id)
            # Create project file structure
            code_executor.create_project(session_id)
        else:
            # Ensure project exists
            code_executor.create_project(session_id)

        return exists

    async def load_code(self, *, session_id: str) -> dict:
        """Load code files for a session."""
        # Load from file system
        file_map, package_json = code_executor.load_code(session_id)

        # Also sync with database
        db_files = db.get_code_files(session_id)
        if db_files:
            # Database takes precedence if it exists
            file_map = {k: v.encode("utf-8") for k, v in db_files.items()}

        # Convert bytes to strings for JSON serialization
        code_map = {path: content.decode("utf-8") for path, content in file_map.items()}

        return {"code_map": code_map, "package_json": package_json}

    async def edit_code(self, *, session_id: str, code_map: dict):
        """Save code changes for a session."""
        # Save to file system
        code_executor.save_code(session_id, code_map)

        # Also save to database
        for file_path, content in code_map.items():
            db.save_code_file(session_id, file_path, content)

        return {"session_id": session_id}

    def get_history(self, session_id: str) -> list[ConvoMessage]:
        """Get conversation history from database."""
        history = db.get_conversation_history(session_id)
        return [
            ConvoMessage(role=msg["role"], content=msg["content"]) for msg in history
        ]

    async def add_to_history(self, session_id: str, user_feedback: str, agent_plan: str):
        """Add messages to conversation history."""
        db.save_conversation(session_id, "user", user_feedback)
        db.save_conversation(session_id, "assistant", agent_plan)

    async def send_feedback(
        self, *, session_id: str, feedback: str
    ) -> AsyncGenerator[dict, None]:
        """Process user feedback and generate code changes."""
        yield Message.new(MessageType.UPDATE_IN_PROGRESS, {}, session_id=session_id).to_dict()

        # Load current code
        code_data = await self.load_code(session_id=session_id)
        code_map = code_data["code_map"]
        package_json = code_data["package_json"]

        code_files = []
        for path, content in code_map.items():
            code_files.append({"path": path, "content": content})

        # Get conversation history
        history = self.get_history(session_id)

        # Use the EditCode function (which uses FastCodingClient for quick edits)
        stream = self.model_client.stream.EditCode(
            history, feedback, code_files, package_json
        )

        sent_plan = False
        new_code_map = {}
        plan_msg_id = str(uuid.uuid4())
        file_msg_id = str(uuid.uuid4())

        for partial in stream:
            if partial.plan.state != "Complete" and not sent_plan:
                yield Message.new(
                    MessageType.AGENT_PARTIAL,
                    {"text": partial.plan.value},
                    id=plan_msg_id,
                    session_id=session_id,
                ).to_dict()

            if partial.plan.state == "Complete" and not sent_plan:
                yield Message.new(
                    MessageType.AGENT_FINAL,
                    {"text": partial.plan.value},
                    id=plan_msg_id,
                    session_id=session_id,
                ).to_dict()

                await self.add_to_history(session_id, feedback, partial.plan.value)
                sent_plan = True

            for file in partial.files:
                if file.path not in new_code_map:
                    yield Message.new(
                        MessageType.UPDATE_FILE,
                        {"text": f"Working on {file.path}"},
                        id=file_msg_id,
                        session_id=session_id,
                    ).to_dict()

                    new_code_map[file.path] = file.content

        # Save code changes
        await self.edit_code(session_id=session_id, code_map=new_code_map)

        yield Message.new(
            MessageType.UPDATE_COMPLETED, {}, session_id=session_id
        ).to_dict()

