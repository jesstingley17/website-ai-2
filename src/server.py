"""FastAPI server with WebSocket support to replace Beam realtime."""

import json
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from .agent_v2 import Agent, MessageType
from .config import config, Config

# Validate configuration on startup
Config.validate()

# Global agent instance
agent_instance: Agent | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown."""
    global agent_instance
    agent_instance = Agent()
    print("Agent initialized")
    yield
    agent_instance = None
    print("Agent shutdown")


app = FastAPI(title="Lovable Clone API", lifespan=lifespan)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "ok"}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    await websocket.accept()

    try:
        while True:
            # Receive message
            data = await websocket.receive_text()
            msg = json.loads(data)

            if not agent_instance:
                await websocket.send_json({"error": "Agent not initialized"})
                continue

            # Handle different message types
            match msg.get("type"):
                case MessageType.USER.value:
                    session_id = msg["data"]["session_id"]
                    feedback = msg["data"]["text"]

                    # Stream responses
                    async for response in agent_instance.send_feedback(
                        session_id=session_id, feedback=feedback
                    ):
                        await websocket.send_json(response)

                case MessageType.INIT.value:
                    session_id = msg["data"]["session_id"]
                    exists = await agent_instance.init(session_id=session_id)

                    from .code_executor import code_executor
                    project_data = code_executor.create_project(session_id)

                    response = {
                        "id": str(uuid.uuid4()),
                        "type": MessageType.INIT.value,
                        "data": {
                            "exists": exists,
                            "session_id": session_id,
                            "url": project_data.get("url"),
                        },
                        "timestamp": int(time.time() * 1000),
                        "session_id": session_id,
                    }
                    await websocket.send_json(response)

                case MessageType.LOAD_CODE.value:
                    session_id = msg["data"]["session_id"]
                    code_data = await agent_instance.load_code(session_id=session_id)

                    response = {
                        "id": str(uuid.uuid4()),
                        "type": MessageType.LOAD_CODE.value,
                        "data": code_data,
                        "timestamp": int(time.time() * 1000),
                        "session_id": session_id,
                    }
                    await websocket.send_json(response)

                case _:
                    await websocket.send_json({"error": f"Unknown message type: {msg.get('type')}"})

    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        print(f"WebSocket error: {e}")
        await websocket.send_json({"error": str(e)})


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.HOST, port=config.PORT)

