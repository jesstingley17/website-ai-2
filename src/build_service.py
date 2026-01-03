"""Build service for compiling React/Vite projects."""

import asyncio
import json
import subprocess
import time
import uuid
from enum import Enum
from pathlib import Path
from typing import Optional, Callable, AsyncGenerator

from .config import config
from .code_executor import code_executor

# Import websocket manager (avoid circular import)
def get_websocket_manager():
    from .websocket_manager import websocket_manager
    return websocket_manager


class BuildStatus(Enum):
    """Build status enumeration."""
    PENDING = "pending"
    BUILDING = "building"
    SUCCESS = "success"
    ERROR = "error"


class BuildService:
    """Service for building React/Vite projects with background queue support."""
    
    def __init__(self):
        self.build_status: dict[str, BuildStatus] = {}
        self.build_errors: dict[str, str] = {}
        self.build_times: dict[str, float] = {}
        self.build_logs: dict[str, list[str]] = {}
        self.build_progress_callbacks: dict[str, Callable] = {}
        self.build_tasks: dict[str, asyncio.Task] = {}
        self.build_queue: asyncio.Queue = asyncio.Queue()
        self._queue_processor_task: Optional[asyncio.Task] = None
    
    def _add_log(self, session_id: str, message: str):
        """Add a log message for a session."""
        if session_id not in self.build_logs:
            self.build_logs[session_id] = []
        self.build_logs[session_id].append(message)
        # Keep only last 100 logs
        if len(self.build_logs[session_id]) > 100:
            self.build_logs[session_id] = self.build_logs[session_id][-100:]
        
        # Broadcast log via WebSocket (real-time updates!)
        asyncio.create_task(self._broadcast_build_progress(session_id, {
            "type": "build_progress",
            "message": message,
            "logs": self.build_logs[session_id][-20:],  # Last 20 log lines
        }))
        
        # Call progress callback if set (for backwards compatibility)
        if session_id in self.build_progress_callbacks:
            callback = self.build_progress_callbacks[session_id]
            try:
                callback({"type": "log", "message": message})
            except Exception as e:
                print(f"Error in progress callback: {e}")
    
    async def _broadcast_build_progress(self, session_id: str, data: dict):
        """Broadcast build progress to WebSocket connections."""
        try:
            ws_manager = get_websocket_manager()
            message = {
                "id": str(uuid.uuid4()),
                "type": "build_progress",
                "data": data,
                "timestamp": int(time.time() * 1000),
                "session_id": session_id,
            }
            await ws_manager.broadcast_to_session(session_id, message)
        except Exception as e:
            print(f"Error broadcasting build progress: {e}")
    
    async def _broadcast_build_completion(self, session_id: str, build_time: float):
        """Broadcast build completion to WebSocket connections."""
        try:
            ws_manager = get_websocket_manager()
            message = {
                "id": str(uuid.uuid4()),
                "type": "build_completed",
                "data": {
                    "status": "success",
                    "build_time": build_time,
                    "message": f"Build completed successfully in {build_time:.2f}s",
                },
                "timestamp": int(time.time() * 1000),
                "session_id": session_id,
            }
            await ws_manager.broadcast_to_session(session_id, message)
        except Exception as e:
            print(f"Error broadcasting build completion: {e}")
    
    async def _broadcast_build_error(self, session_id: str, error: str):
        """Broadcast build error to WebSocket connections."""
        try:
            ws_manager = get_websocket_manager()
            message = {
                "id": str(uuid.uuid4()),
                "type": "build_error",
                "data": {
                    "status": "error",
                    "error": error,
                },
                "timestamp": int(time.time() * 1000),
                "session_id": session_id,
            }
            await ws_manager.broadcast_to_session(session_id, message)
        except Exception as e:
            print(f"Error broadcasting build error: {e}")
    
    def set_progress_callback(self, session_id: str, callback: Callable):
        """Set a callback for build progress updates."""
        self.build_progress_callbacks[session_id] = callback
    
    def clear_progress_callback(self, session_id: str):
        """Clear the progress callback for a session."""
        self.build_progress_callbacks.pop(session_id, None)
    
    def get_build_logs(self, session_id: str) -> list[str]:
        """Get build logs for a session."""
        return self.build_logs.get(session_id, [])
    
    async def queue_build(self, session_id: str, force_rebuild: bool = False) -> dict:
        """
        Queue a build (non-blocking).
        
        Returns immediately with status, build runs in background.
        """
        # Check if already building
        if self.build_status.get(session_id) == BuildStatus.BUILDING:
            return {
                "status": BuildStatus.BUILDING.value,
                "message": "Build already in progress",
            }
        
        # Check if build is up to date
        if not force_rebuild and self.is_built(session_id):
            dist_path = code_executor.get_project_path(session_id) / "dist"
            src_path = code_executor.get_project_path(session_id) / "src"
            if src_path.exists():
                dist_mtime = dist_path.stat().st_mtime
                src_files_newer = any(
                    f.stat().st_mtime > dist_mtime
                    for f in src_path.rglob("*")
                    if f.is_file()
                )
                if not src_files_newer:
                    return {
                        "status": BuildStatus.SUCCESS.value,
                        "message": "Build is up to date",
                    }
        
        # Queue the build
        await self.build_queue.put((session_id, force_rebuild))
        self.build_status[session_id] = BuildStatus.PENDING
        self.build_logs[session_id] = []
        
        # Start queue processor if not running
        if self._queue_processor_task is None or self._queue_processor_task.done():
            self._queue_processor_task = asyncio.create_task(self._process_build_queue())
        
        return {
            "status": BuildStatus.PENDING.value,
            "message": "Build queued",
        }
    
    async def _process_build_queue(self):
        """Background task to process build queue."""
        while True:
            try:
                session_id, force_rebuild = await self.build_queue.get()
                # Run build in background
                asyncio.create_task(self.build_project(session_id, force_rebuild))
                self.build_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                print(f"Error processing build queue: {e}")
    
    async def build_project(self, session_id: str, force_rebuild: bool = False) -> dict:
        """
        Build a project for a session.
        
        Returns:
            dict with status, error (if any), and build time
        """
        project_path = code_executor.get_project_path(session_id)
        
        if not project_path.exists():
            return {
                "status": BuildStatus.ERROR.value,
                "error": f"Project not found for session {session_id}",
            }
        
        # Check if build is already in progress
        if self.build_status.get(session_id) == BuildStatus.BUILDING:
            return {
                "status": BuildStatus.BUILDING.value,
                "message": "Build already in progress",
            }
        
        # Check if build exists and is recent (unless force rebuild)
        dist_path = project_path / "dist"
        if dist_path.exists() and not force_rebuild:
            # Check if dist is newer than src files
            src_path = project_path / "src"
            if src_path.exists():
                dist_mtime = dist_path.stat().st_mtime
                src_files_newer = any(
                    f.stat().st_mtime > dist_mtime
                    for f in src_path.rglob("*")
                    if f.is_file()
                )
                if not src_files_newer:
                    return {
                        "status": BuildStatus.SUCCESS.value,
                        "message": "Build is up to date",
                    }
        
        # Start build
        start_time = time.time()
        self.build_status[session_id] = BuildStatus.BUILDING
        self._add_log(session_id, "Build started")
        
        try:
            # Step 1: Install dependencies
            self._add_log(session_id, "Installing dependencies...")
            install_result = await asyncio.to_thread(
                subprocess.run,
                ["npm", "install"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300,
            )
            
            if install_result.returncode != 0:
                error_msg = install_result.stderr or install_result.stdout
                self.build_status[session_id] = BuildStatus.ERROR
                self.build_errors[session_id] = f"npm install failed: {error_msg}"
                self._add_log(session_id, f"Error: npm install failed")
                return {
                    "status": BuildStatus.ERROR.value,
                    "error": f"npm install failed: {error_msg[:500]}",
                }
            
            self._add_log(session_id, "Dependencies installed successfully")
            
            # Step 2: Build the project
            self._add_log(session_id, "Building project...")
            build_result = await asyncio.to_thread(
                subprocess.run,
                ["npm", "run", "build"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300,
            )
            
            if build_result.returncode != 0:
                error_msg = build_result.stderr or build_result.stdout
                self.build_status[session_id] = BuildStatus.ERROR
                self.build_errors[session_id] = f"Build failed: {error_msg}"
                self._add_log(session_id, f"Error: Build failed")
                # Send last few lines of error
                error_lines = error_msg.split('\n')[-10:]
                for line in error_lines:
                    if line.strip():
                        self._add_log(session_id, f"  {line}")
                return {
                    "status": BuildStatus.ERROR.value,
                    "error": f"Build failed: {error_msg[:500]}",
                }
            
            # Build successful
            build_time = time.time() - start_time
            self.build_status[session_id] = BuildStatus.SUCCESS
            self.build_times[session_id] = build_time
            self._add_log(session_id, f"Build completed successfully in {build_time:.2f}s")
            
            # Broadcast build completion (real-time update!)
            asyncio.create_task(self._broadcast_build_completion(session_id, build_time))
            
            return {
                "status": BuildStatus.SUCCESS.value,
                "message": "Build completed successfully",
                "build_time": build_time,
            }
            
        except subprocess.TimeoutExpired:
            self.build_status[session_id] = BuildStatus.ERROR
            error_msg = "Build timed out after 5 minutes"
            self.build_errors[session_id] = error_msg
            self._add_log(session_id, f"Error: {error_msg}")
            asyncio.create_task(self._broadcast_build_error(session_id, error_msg))
            return {
                "status": BuildStatus.ERROR.value,
                "error": error_msg,
            }
        except Exception as e:
            self.build_status[session_id] = BuildStatus.ERROR
            error_msg = f"Build error: {str(e)}"
            self.build_errors[session_id] = error_msg
            self._add_log(session_id, f"Error: {error_msg}")
            asyncio.create_task(self._broadcast_build_error(session_id, error_msg))
            return {
                "status": BuildStatus.ERROR.value,
                "error": error_msg,
            }
        finally:
            # Clear callback after build completes
            self.clear_progress_callback(session_id)
    
    def get_build_status(self, session_id: str) -> dict:
        """Get the current build status for a session."""
        status = self.build_status.get(session_id, BuildStatus.PENDING)
        return {
            "status": status.value,
            "error": self.build_errors.get(session_id),
            "build_time": self.build_times.get(session_id),
            "logs": self.build_logs.get(session_id, [])[-20:],  # Last 20 log lines
        }
    
    def is_built(self, session_id: str) -> bool:
        """Check if a project has been built."""
        project_path = code_executor.get_project_path(session_id)
        dist_path = project_path / "dist"
        return dist_path.exists() and (dist_path / "index.html").exists()
    
    def get_build_path(self, session_id: str) -> Optional[Path]:
        """Get the path to the built dist folder."""
        project_path = code_executor.get_project_path(session_id)
        dist_path = project_path / "dist"
        if dist_path.exists():
            return dist_path
        return None


# Global build service instance
build_service = BuildService()

