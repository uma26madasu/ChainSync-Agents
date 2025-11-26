"""Configuration management for ChainSync AI Agent"""
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Application configuration"""

    # OpenAI Configuration
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

    # ChainSync API Configuration
    CHAINSYNC_API_URL = os.getenv('CHAINSYNC_API_URL', 'http://localhost:8081/api')
    CHAINSYNC_API_KEY = os.getenv('CHAINSYNC_API_KEY')
    CHAINSYNC_TIMEOUT = int(os.getenv('CHAINSYNC_TIMEOUT', '10'))

    # Slotify API Configuration
    SLOTIFY_API_URL = os.getenv('SLOTIFY_API_URL', 'https://api.slotify.com/v1')
    SLOTIFY_API_KEY = os.getenv('SLOTIFY_API_KEY')
    SLOTIFY_TIMEOUT = int(os.getenv('SLOTIFY_TIMEOUT', '10'))

    # Webhook Security
    WEBHOOK_API_KEY = os.getenv('WEBHOOK_API_KEY')
    WEBHOOK_SECRET_KEY = os.getenv('WEBHOOK_SECRET_KEY')

    # Server Configuration
    PYTHON_AGENT_PORT = int(os.getenv('PYTHON_AGENT_PORT', '8000'))

    # Database Configuration
    DATABASE_URL = os.getenv('DATABASE_URL', 'sqlite:///./chainsync_agents.db')

    # Development Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

    @classmethod
    def validate(cls):
        """Validate required configuration"""
        warnings = []

        if not cls.OPENAI_API_KEY:
            warnings.append("OPENAI_API_KEY not set. Using mock responses.")

        if not cls.SLOTIFY_API_KEY:
            warnings.append("SLOTIFY_API_KEY not set. Slotify integration disabled.")

        if not cls.CHAINSYNC_API_KEY:
            warnings.append("CHAINSYNC_API_KEY not set. ChainSync API calls disabled.")

        if not cls.WEBHOOK_API_KEY or not cls.WEBHOOK_SECRET_KEY:
            warnings.append("Webhook security not configured. Webhooks are unprotected.")

        if warnings:
            print("⚠️  Configuration Warnings:")
            for warning in warnings:
                print(f"   - {warning}")

        return True