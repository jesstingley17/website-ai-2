"""Build service for compiling React/Vite projects."""

import json
import subprocess
import time
from enum import Enum
from pathlib import Path
from typing import Optional

from .config import config
from .code_executor import code_executor


class BuildStatus(Enum):
    """Build status enumeration."""
    PENDING = "pending"
    BUILDING = "building"
    SUCCESS = "success"
    ERROR = "error"


class BuildService:
    """Service for building React/Vite projects."""
    
    def __init__(self):
        self.build_status: dict[str, BuildStatus] = {}
        self.build_errors: dict[str, str] = {}
        self.build_times: dict[str, float] = {}
    
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
        
        try:
            # Step 1: Install dependencies
            print(f"Installing dependencies for session {session_id}...")
            install_result = subprocess.run(
                ["npm", "install"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )
            
            if install_result.returncode != 0:
                error_msg = install_result.stderr or install_result.stdout
                self.build_status[session_id] = BuildStatus.ERROR
                self.build_errors[session_id] = f"npm install failed: {error_msg}"
                return {
                    "status": BuildStatus.ERROR.value,
                    "error": f"npm install failed: {error_msg[:500]}",
                }
            
            # Step 2: Build the project
            print(f"Building project for session {session_id}...")
            build_result = subprocess.run(
                ["npm", "run", "build"],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300,  # 5 minute timeout
            )
            
            if build_result.returncode != 0:
                error_msg = build_result.stderr or build_result.stdout
                self.build_status[session_id] = BuildStatus.ERROR
                self.build_errors[session_id] = f"Build failed: {error_msg}"
                return {
                    "status": BuildStatus.ERROR.value,
                    "error": f"Build failed: {error_msg[:500]}",
                }
            
            # Build successful
            build_time = time.time() - start_time
            self.build_status[session_id] = BuildStatus.SUCCESS
            self.build_times[session_id] = build_time
            
            return {
                "status": BuildStatus.SUCCESS.value,
                "message": "Build completed successfully",
                "build_time": build_time,
            }
            
        except subprocess.TimeoutExpired:
            self.build_status[session_id] = BuildStatus.ERROR
            error_msg = "Build timed out after 5 minutes"
            self.build_errors[session_id] = error_msg
            return {
                "status": BuildStatus.ERROR.value,
                "error": error_msg,
            }
        except Exception as e:
            self.build_status[session_id] = BuildStatus.ERROR
            error_msg = f"Build error: {str(e)}"
            self.build_errors[session_id] = error_msg
            return {
                "status": BuildStatus.ERROR.value,
                "error": error_msg,
            }
    
    def get_build_status(self, session_id: str) -> dict:
        """Get the current build status for a session."""
        status = self.build_status.get(session_id, BuildStatus.PENDING)
        return {
            "status": status.value,
            "error": self.build_errors.get(session_id),
            "build_time": self.build_times.get(session_id),
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

