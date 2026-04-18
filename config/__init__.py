import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # Telegram
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # File conversion
    SUPPORTED_FORMATS = os.getenv('SUPPORTED_FORMATS', 'epub,mobi,azw3').split(',')
    OUTPUT_FORMAT = os.getenv('OUTPUT_FORMAT', 'mobi')
    
    # Kindle
    KINDLE_MOUNT_POINT = os.getenv('KINDLE_MOUNT_POINT', '/mnt/kindle')
    KINDLE_DOCUMENTS_FOLDER = os.getenv('KINDLE_DOCUMENTS_FOLDER', 'documents')
    
    # Paths
    UPLOAD_DIR = '/tmp/uploads'
    CONVERT_DIR = '/tmp/converted'
    
    # Logging
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    def __init__(self):
        self._validate_config()
    
    def _validate_config(self):
        """Validate required configuration"""
        if not self.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN environment variable is not set")
        
        # Create required directories
        os.makedirs(self.UPLOAD_DIR, exist_ok=True)
        os.makedirs(self.CONVERT_DIR, exist_ok=True)

config = Config()
