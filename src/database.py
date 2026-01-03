"""Supabase database integration for session and code storage."""

import os
from typing import Optional
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()


class Database:
    """Database interface for Supabase operations."""

    def __init__(self):
        supabase_url = os.getenv("SUPABASE_URL")
        supabase_key = os.getenv("SUPABASE_SERVICE_ROLE_KEY") or os.getenv("SUPABASE_ANON_KEY")

        if not supabase_url or not supabase_key:
            raise ValueError(
                "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY (or SUPABASE_ANON_KEY) must be set"
            )

        self.supabase: Client = create_client(supabase_url, supabase_key)

    def create_session(
        self, session_id: str, project_url: Optional[str] = None, metadata: Optional[dict] = None
    ) -> dict:
        """Create a new session."""
        data = {
            "session_id": session_id,
            "project_url": project_url,
            "metadata": metadata or {},
        }
        result = self.supabase.table("sessions").insert(data).execute()
        return result.data[0] if result.data else {}

    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session by session_id."""
        result = (
            self.supabase.table("sessions").select("*").eq("session_id", session_id).execute()
        )
        return result.data[0] if result.data else None

    def update_session(self, session_id: str, **kwargs) -> dict:
        """Update session."""
        result = (
            self.supabase.table("sessions")
            .update(kwargs)
            .eq("session_id", session_id)
            .execute()
        )
        return result.data[0] if result.data else {}

    def save_code_file(self, session_id: str, file_path: str, content: str) -> dict:
        """Save or update a code file."""
        data = {
            "session_id": session_id,
            "file_path": file_path,
            "content": content,
        }
        # Use upsert to handle both insert and update
        result = (
            self.supabase.table("code_files")
            .upsert(data, on_conflict="session_id,file_path")
            .execute()
        )
        return result.data[0] if result.data else {}

    def get_code_files(self, session_id: str) -> dict[str, str]:
        """Get all code files for a session."""
        result = (
            self.supabase.table("code_files")
            .select("file_path, content")
            .eq("session_id", session_id)
            .execute()
        )
        return {file["file_path"]: file["content"] for file in result.data}

    def save_conversation(self, session_id: str, role: str, content: str) -> dict:
        """Save a conversation message."""
        data = {
            "session_id": session_id,
            "role": role,
            "content": content,
        }
        result = self.supabase.table("conversations").insert(data).execute()
        return result.data[0] if result.data else {}

    def get_conversation_history(self, session_id: str, limit: int = 50) -> list[dict]:
        """Get conversation history for a session."""
        result = (
            self.supabase.table("conversations")
            .select("role, content")
            .eq("session_id", session_id)
            .order("created_at", desc=False)
            .limit(limit)
            .execute()
        )
        return result.data


# Global database instance
db = Database()

