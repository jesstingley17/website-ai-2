"""FastAPI server with WebSocket support to replace Beam realtime."""

import json
import time
import uuid
from contextlib import asynccontextmanager

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, FileResponse
from pathlib import Path

from .agent_v2 import Agent, MessageType
from .config import config, Config
from .code_executor import code_executor
from .build_service import build_service
from .websocket_manager import websocket_manager

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


@app.get("/preview/{session_id}/build")
async def build_preview(session_id: str, background: bool = True):
    """
    Trigger a build for a session's project.
    
    Args:
        background: If True (default), queue build in background (non-blocking, better UX)
                   If False, wait for build to complete (blocking)
    """
    try:
        if background:
            # Queue build (non-blocking - better than lovable!)
            result = await build_service.queue_build(session_id, force_rebuild=True)
        else:
            # Run build directly (blocking)
            result = await build_service.build_project(session_id, force_rebuild=True)
        return result
    except Exception as e:
        return {"status": "error", "error": str(e)}


@app.get("/preview/{session_id}/build/logs")
async def get_build_logs(session_id: str):
    """Get build logs for a session."""
    return {"logs": build_service.get_build_logs(session_id)}


@app.get("/preview/{session_id}/build/status")
async def build_status(session_id: str):
    """Get build status for a session."""
    return build_service.get_build_status(session_id)


@app.get("/preview/{session_id}/{full_path:path}")
async def serve_preview_files(session_id: str, full_path: str, request: Request):
    """Serve built files for a session - handles all paths under /preview/{session_id}/."""
    build_path = build_service.get_build_path(session_id)
    
    if build_path and build_path.exists():
        # Clean the path and serve the file
        file_path = build_path / full_path.lstrip("/")
        
        # Security: ensure path is within build directory
        try:
            file_path = file_path.resolve()
            build_path_resolved = build_path.resolve()
            if not str(file_path).startswith(str(build_path_resolved)):
                # Path traversal attempt - serve index.html
                full_path = ""
        except:
            full_path = ""
        
        if full_path and file_path.exists() and file_path.is_file():
            return FileResponse(file_path)
        
        # Fall back to index.html for SPA routing
        index_path = build_path / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
    
    # Fall back to simple preview if no build exists
    return await preview_session_simple(session_id)


@app.get("/preview/{session_id}")
async def serve_preview_root(session_id: str):
    """Serve the preview root - serves index.html or simple preview."""
    build_path = build_service.get_build_path(session_id)
    
    if build_path and build_path.exists():
        index_path = build_path / "index.html"
        if index_path.exists():
            return FileResponse(index_path)
    
    # Fall back to simple preview if no build exists
    return await preview_session_simple(session_id)


async def preview_session_simple(session_id: str):
    """Simple preview using React CDN (fallback when build not available)."""
    try:
        # Load code files for this session
        file_map, package_json = code_executor.load_code(session_id)
        
        # Also check database
        from .database import db
        db_files = db.get_code_files(session_id)
        if db_files:
            file_map = {k: v.encode("utf-8") for k, v in db_files.items()}
        
        # Convert bytes to strings
        code_map = {path: content.decode("utf-8") if isinstance(content, bytes) else content 
                   for path, content in file_map.items()}
        
        # Find App.tsx or App.jsx (main component)
        app_file = None
        for path in code_map.keys():
            if path.endswith("App.tsx") or path.endswith("App.jsx"):
                app_file = path
                break
        
        if not app_file:
            # If no App file, create a simple default
            app_code = """function App() {
  return React.createElement('div', { style: { padding: '20px', fontFamily: 'sans-serif' } },
    React.createElement('h1', null, 'Welcome to your app!'),
    React.createElement('p', null, 'Start by creating an App.tsx or App.jsx file.')
  );
}"""
        else:
            app_code = code_map[app_file]
        
        # Generate HTML with React from CDN
        html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Preview - {session_id}</title>
    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif; }}
        #root {{ width: 100%; min-height: 100vh; }}
    </style>
</head>
<body>
    <div id="root"></div>
    <script type="text/babel">
        const {{ useState, useEffect, useRef, useCallback, useMemo, useContext, createContext, useReducer, useImperativeHandle, forwardRef, memo, useLayoutEffect, useDebugValue }} = React;
        
        // User's App component code
        {app_code}
        
        // Render the app
        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(React.createElement(App));
    </script>
</body>
</html>"""
        
        return HTMLResponse(content=html_content)
        
    except Exception as e:
        error_html = f"""<!DOCTYPE html>
<html>
<head><title>Preview Error</title></head>
<body style="padding: 20px; font-family: sans-serif;">
    <h1>Preview Error</h1>
    <p>Error loading preview: {str(e)}</p>
    <p>Session ID: {session_id}</p>
</body>
</html>"""
        return HTMLResponse(content=error_html, status_code=500)


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    session_id: str | None = None
    
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
                    # Connect to session for build progress updates
                    await websocket_manager.connect(websocket, session_id)
                    
                    feedback = msg["data"]["text"]

                    # Stream responses
                    async for response in agent_instance.send_feedback(
                        session_id=session_id, feedback=feedback
                    ):
                        await websocket.send_json(response)

                case MessageType.INIT.value:
                    session_id = msg["data"]["session_id"]
                    # Connect to session for build progress updates
                    await websocket_manager.connect(websocket, session_id)
                    
                    exists = await agent_instance.init(session_id=session_id)

                    from .code_executor import code_executor
                    project_data = code_executor.create_project(session_id)
                    
                    # Set preview URL
                    preview_url = f"{config.BACKEND_URL}/preview/{session_id}"

                    response = {
                        "id": str(uuid.uuid4()),
                        "type": MessageType.INIT.value,
                        "data": {
                            "exists": exists,
                            "session_id": session_id,
                            "url": preview_url,
                        },
                        "timestamp": int(time.time() * 1000),
                        "session_id": session_id,
                    }
                    await websocket.send_json(response)

                case MessageType.LOAD_CODE.value:
                    session_id = msg["data"]["session_id"]
                    # Connect to session for build progress updates
                    await websocket_manager.connect(websocket, session_id)
                    
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
        if session_id:
            websocket_manager.disconnect(websocket, session_id)
        print("Client disconnected")
    except Exception as e:
        if session_id:
            websocket_manager.disconnect(websocket, session_id)
        print(f"WebSocket error: {e}")
        try:
            await websocket.send_json({"error": str(e)})
        except:
            pass


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host=config.HOST, port=config.PORT)

