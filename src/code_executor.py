"""Code execution and file management using local file system."""

import json
import os
import shutil
import subprocess
from pathlib import Path
from typing import Optional

from .config import config


class CodeExecutor:
    """Manages code execution environments using local file system."""

    DEFAULT_CODE_PATH = "src"
    DEFAULT_PROJECT_ROOT = "."

    def __init__(self):
        self.projects_dir = Path(config.PROJECTS_DIR)
        self.projects_dir.mkdir(parents=True, exist_ok=True)

    def get_project_path(self, session_id: str) -> Path:
        """Get the file system path for a session's project."""
        return self.projects_dir / session_id

    def create_project(self, session_id: str) -> dict:
        """Create a new React project for a session."""
        project_path = self.get_project_path(session_id)

        if project_path.exists():
            # Project already exists
            return {
                "url": f"http://localhost:3000/{session_id}",
                "session_id": session_id,
                "exists": True,
            }

        # Create project directory
        project_path.mkdir(parents=True, exist_ok=True)

        # Initialize a basic React + Vite project structure
        # For production, you might want to use a template or clone a starter
        src_path = project_path / self.DEFAULT_CODE_PATH
        src_path.mkdir(parents=True, exist_ok=True)

        # Create basic package.json
        package_json = {
            "name": f"project-{session_id}",
            "version": "0.1.0",
            "type": "module",
            "scripts": {
                "dev": "vite",
                "build": "vite build",
                "preview": "vite preview",
            },
            "dependencies": {
                "react": "^18.2.0",
                "react-dom": "^18.2.0",
                "@tanstack/react-query": "^5.0.0",
                "react-router-dom": "^6.20.0",
                "recharts": "^2.10.0",
                "sonner": "^1.2.0",
                "zod": "^3.22.0",
                "react-hook-form": "^7.48.0",
                "@hookform/resolvers": "^3.3.0",
                "date-fns": "^2.30.0",
                "uuid": "^9.0.0",
                "lucide-react": "^0.294.0",
                "@supabase/supabase-js": "^2.38.0",
            },
            "devDependencies": {
                "@types/react": "^18.2.0",
                "@types/react-dom": "^18.2.0",
                "@vitejs/plugin-react": "^4.2.0",
                "vite": "^5.0.0",
                "typescript": "^5.2.0",
                "tailwindcss": "^3.3.0",
                "autoprefixer": "^10.4.16",
                "postcss": "^8.4.31",
            },
        }

        with open(project_path / "package.json", "w") as f:
            json.dump(package_json, f, indent=2)

        return {
            "url": f"http://localhost:3000/{session_id}",
            "session_id": session_id,
            "exists": False,
        }

    def load_code(self, session_id: str) -> tuple[dict[str, bytes], str]:
        """Load code files from the project directory."""
        project_path = self.get_project_path(session_id)
        code_path = project_path / self.DEFAULT_CODE_PATH

        file_map = {}

        if code_path.exists():
            for file_path in code_path.rglob("*"):
                if file_path.is_file():
                    relative_path = file_path.relative_to(code_path)
                    with open(file_path, "rb") as f:
                        file_map[str(relative_path)] = f.read()

        # Load package.json
        package_json_path = project_path / "package.json"
        package_json = "{}"
        if package_json_path.exists():
            with open(package_json_path, "r") as f:
                package_json = f.read()

        return file_map, package_json

    def save_code(self, session_id: str, code_map: dict[str, str]) -> dict:
        """Save code files to the project directory."""
        project_path = self.get_project_path(session_id)
        code_path = project_path / self.DEFAULT_CODE_PATH
        code_path.mkdir(parents=True, exist_ok=True)

        for file_path_str, content in code_map.items():
            file_path = code_path / file_path_str
            file_path.parent.mkdir(parents=True, exist_ok=True)

            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)

        return {"session_id": session_id}

    def start_dev_server(self, session_id: str) -> Optional[subprocess.Popen]:
        """Start a development server for the project (optional - for local preview)."""
        project_path = self.get_project_path(session_id)
        if not (project_path / "node_modules").exists():
            # Install dependencies first
            subprocess.run(["npm", "install"], cwd=project_path, check=False)

        # Start dev server in background
        # Note: In production, you'd want to use a proper process manager
        try:
            process = subprocess.Popen(
                ["npm", "run", "dev"],
                cwd=project_path,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )
            return process
        except Exception as e:
            print(f"Error starting dev server: {e}")
            return None

    def delete_project(self, session_id: str):
        """Delete a project directory."""
        project_path = self.get_project_path(session_id)
        if project_path.exists():
            shutil.rmtree(project_path)


# Global code executor instance
code_executor = CodeExecutor()

