"""WebSocket connection manager for real-time communication."""

import json
import time
import uuid
from typing import Dict, Set
from fastapi import WebSocket


class WebSocketManager:
    """Manages WebSocket connections and broadcasts messages."""
    
    def __init__(self):
        # Map of session_id -> Set of WebSocket connections
        self.active_connections: Dict[str, Set[WebSocket]] = {}
    
    async def connect(self, websocket: WebSocket, session_id: str):
        """Connect a WebSocket to a session."""
        await websocket.accept()
        if session_id not in self.active_connections:
            self.active_connections[session_id] = set()
        self.active_connections[session_id].add(websocket)
        print(f"WebSocket connected for session {session_id}")
    
    def disconnect(self, websocket: WebSocket, session_id: str):
        """Disconnect a WebSocket from a session."""
        if session_id in self.active_connections:
            self.active_connections[session_id].discard(websocket)
            if not self.active_connections[session_id]:
                del self.active_connections[session_id]
        print(f"WebSocket disconnected for session {session_id}")
    
    async def send_personal_message(self, message: dict, websocket: WebSocket):
        """Send a message to a specific WebSocket connection."""
        try:
            await websocket.send_json(message)
        except Exception as e:
            print(f"Error sending personal message: {e}")
    
    async def broadcast_to_session(self, session_id: str, message: dict):
        """Broadcast a message to all connections for a session."""
        if session_id not in self.active_connections:
            return
        
        # Create a copy of the set to avoid modification during iteration
        connections = self.active_connections[session_id].copy()
        
        for connection in connections:
            try:
                await connection.send_json(message)
            except Exception as e:
                print(f"Error broadcasting to session {session_id}: {e}")
                # Remove dead connection
                self.active_connections[session_id].discard(connection)
    
    def get_connection_count(self, session_id: str) -> int:
        """Get the number of active connections for a session."""
        return len(self.active_connections.get(session_id, set()))


# Global WebSocket manager instance
websocket_manager = WebSocketManager()

