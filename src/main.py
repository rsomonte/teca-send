#!/usr/bin/env python3
"""
TECA-Send: Telegram bot for converting and transferring ebooks to Kindle
"""

import asyncio
import logging
import sys
import os
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

load_dotenv()

from src.telegram_bot import TelegramBotHandler

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=LOG_LEVEL
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point"""
    try:
        logger.info("Starting TECA-Send service...")
        
        # Validate configuration
        if not TELEGRAM_BOT_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN is not set. Please set it in .env file.")
            sys.exit(1)
        
        # Create and run bot
        bot = TelegramBotHandler()
        await bot.run()
        
    except KeyboardInterrupt:
        logger.info("Service interrupted by user")
    except Exception as e:
        logger.error(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    asyncio.run(main())
