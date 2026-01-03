"""File watcher for hot reloading - watches code changes and triggers rebuilds."""

import asyncio
import time
from pathlib import Path
from typing import Callable, Optional
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler, FileSystemEvent

from .config import config
from .code_executor import code_executor


class CodeChangeHandler(FileSystemEventHandler):
    """Handles file system events for code changes."""
    
    def __init__(self, session_id: str, on_change: Callable[[str], None], debounce_seconds: float = 1.0):
        self.session_id = session_id
        self.on_change = on_change
        self.debounce_seconds = debounce_seconds
        self.last_change_time: dict[str, float] = {}
        self.pending_tasks: dict[str, asyncio.Task] = {}
    
    def should_process_event(self, event_path: str) -> bool:
        """Check if we should process this event."""
        # Only watch source files, not build outputs or node_modules
        path = Path(event_path)
        if any(part in path.parts for part in ['node_modules', 'dist', '.git', '__pycache__']):
            return False
        
        # Only watch source files
        if path.suffix not in ['.tsx', '.ts', '.jsx', '.js', '.css', '.json']:
            return False
        
        return True
    
    def on_modified(self, event: FileSystemEvent):
        """Handle file modification events."""
        if event.is_directory:
            return
        
        event_path = event.src_path
        if not self.should_process_event(event_path):
            return
        
        # Debounce: only process if enough time has passed since last change
        current_time = time.time()
        last_time = self.last_change_time.get(event_path, 0)
        
        if current_time - last_time < self.debounce_seconds:
            # Cancel previous pending task
            if event_path in self.pending_tasks:
                self.pending_tasks[event_path].cancel()
            
            # Schedule new task
            task = asyncio.create_task(self._debounced_change(event_path, current_time))
            self.pending_tasks[event_path] = task
        else:
            # Process immediately
            self.last_change_time[event_path] = current_time
            asyncio.create_task(self._handle_change(event_path))
    
    async def _debounced_change(self, event_path: str, change_time: float):
        """Handle debounced file change."""
        await asyncio.sleep(self.debounce_seconds)
        
        # Only process if this is still the latest change
        if self.last_change_time.get(event_path, 0) <= change_time:
            self.last_change_time[event_path] = change_time
            await self._handle_change(event_path)
    
    async def _handle_change(self, event_path: str):
        """Handle a file change event."""
        try:
            print(f"File changed: {event_path} for session {self.session_id}")
            await self.on_change(self.session_id)
        except Exception as e:
            print(f"Error handling file change: {e}")


class FileWatcher:
    """Watches file changes and triggers rebuilds (hot reloading)."""
    
    def __init__(self):
        self.observers: dict[str, Observer] = {}
        self.handlers: dict[str, CodeChangeHandler] = {}
        self.is_watching: dict[str, bool] = {}
    
    async def watch_session(self, session_id: str, on_change: Callable[[str], None]):
        """Start watching a session's code files for changes."""
        if session_id in self.observers:
            # Already watching
            return
        
        project_path = code_executor.get_project_path(session_id)
        src_path = project_path / "src"
        
        if not src_path.exists():
            return
        
        # Create handler
        handler = CodeChangeHandler(session_id, on_change, debounce_seconds=1.0)
        self.handlers[session_id] = handler
        
        # Create observer
        observer = Observer()
        observer.schedule(handler, str(src_path), recursive=True)
        observer.start()
        
        self.observers[session_id] = observer
        self.is_watching[session_id] = True
        
        print(f"Started watching files for session {session_id}")
    
    def stop_watching(self, session_id: str):
        """Stop watching a session's files."""
        if session_id in self.observers:
            observer = self.observers[session_id]
            observer.stop()
            observer.join()
            
            del self.observers[session_id]
            self.handlers.pop(session_id, None)
            self.is_watching.pop(session_id, None)
            
            print(f"Stopped watching files for session {session_id}")
    
    def is_watching_session(self, session_id: str) -> bool:
        """Check if we're watching a session."""
        return self.is_watching.get(session_id, False)
    
    def stop_all(self):
        """Stop watching all sessions."""
        for session_id in list(self.observers.keys()):
            self.stop_watching(session_id)


# Global file watcher instance
file_watcher = FileWatcher()

