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
    CHAINSYNC_TIMEOUT = int(os.getenv('CHAINSYNC_TIMEOUT', '10'))
    
    # Server Configuration
    PYTHON_AGENT_PORT = int(os.getenv('PYTHON_AGENT_PORT', '8000'))
    
    # Development Settings
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.OPENAI_API_KEY:
            print("⚠️  Warning: OPENAI_API_KEY not set. Using mock responses.")
        
        return True