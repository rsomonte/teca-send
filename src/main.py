#!/usr/bin/env python3
"""
TECA-Send: Telegram bot for converting and transferring ebooks to Kindle
"""

import asyncio
import logging
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import config
from src.telegram_bot import TelegramBotHandler

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=config.LOG_LEVEL
)
logger = logging.getLogger(__name__)

async def main():
    """Main entry point"""
    try:
        logger.info("Starting TECA-Send service...")
        
        # Validate configuration
        if not config.TELEGRAM_BOT_TOKEN:
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
