"""Configuration and environment variables."""

import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    """Application configuration."""

    # API Keys
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")  # For future Gemini support

    # Supabase
    SUPABASE_URL = os.getenv("SUPABASE_URL", "")
    SUPABASE_ANON_KEY = os.getenv("SUPABASE_ANON_KEY", "")
    SUPABASE_SERVICE_ROLE_KEY = os.getenv("SUPABASE_SERVICE_ROLE_KEY", "")

    # Server
    HOST = os.getenv("HOST", "0.0.0.0")
    PORT = int(os.getenv("PORT", "8000"))
    DEBUG = os.getenv("DEBUG", "false").lower() == "true"

    # Code execution (local file system path)
    PROJECTS_DIR = os.getenv("PROJECTS_DIR", "./projects")

    @classmethod
    def validate(cls):
        """Validate required configuration."""
        errors = []
        if not cls.OPENAI_API_KEY:
            errors.append("OPENAI_API_KEY is required")
        if not cls.SUPABASE_URL:
            errors.append("SUPABASE_URL is required")
        if not cls.SUPABASE_ANON_KEY and not cls.SUPABASE_SERVICE_ROLE_KEY:
            errors.append("SUPABASE_ANON_KEY or SUPABASE_SERVICE_ROLE_KEY is required")
        if errors:
            raise ValueError(f"Configuration errors: {', '.join(errors)}")


config = Config()

