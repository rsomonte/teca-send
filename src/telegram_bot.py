import asyncio
import logging
import os
import sys
from dotenv import load_dotenv
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from src.file_converter import FileConverter
from src.kindle_transfer import KindleTransfer
from src.messages import get_messages

load_dotenv()

UPLOAD_DIR = os.getenv('UPLOAD_DIR', '/tmp/uploads')
CONVERT_DIR = os.getenv('CONVERT_DIR', '/tmp/converted')

logger = logging.getLogger(__name__)

class TelegramBotHandler:
    """Handle Telegram bot interactions"""
    
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.messages = get_messages(os.getenv('BOT_LANGUAGE', 'en'))
        self.application = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(self.messages['start'])
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(self.messages['help'])
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check Kindle connection status"""
        if KindleTransfer.is_kindle_connected() and KindleTransfer.is_kindle_writable():
            await update.message.reply_text(self.messages['status_connected'])
        elif KindleTransfer.is_kindle_connected():
            await update.message.reply_text(self.messages['status_connected_readonly'])
        else:
            await update.message.reply_text(self.messages['status_disconnected'])
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle file uploads"""
        try:
            # Get file info
            document = update.message.document
            
            # Check file extension
            file_name = document.file_name
            if not FileConverter.is_supported(file_name):
                await update.message.reply_text(
                    self.messages['unsupported_format'].format(
                        extension=Path(file_name).suffix,
                        supported_formats=', '.join(FileConverter.SUPPORTED_FORMATS),
                    )
                )
                return
            
            # Download file
            await update.message.reply_text(
                self.messages['receiving_file'].format(file_name=file_name)
            )
            
            file = await context.bot.get_file(document.file_id)
            input_path = os.path.join(UPLOAD_DIR, file_name)
            await file.download_to_drive(input_path)

            if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
                logger.error(f"Downloaded file is missing or empty: {input_path}")
                await update.message.reply_text(self.messages['empty_downloaded_file'])
                return
            
            # Convert file
            output_filename = FileConverter.get_output_filename(file_name)
            output_path = os.path.join(CONVERT_DIR, output_filename)
            
            conversion_success = FileConverter.convert(input_path, output_path)
            
            if not conversion_success:
                await update.message.reply_text(self.messages['conversion_failed'])
                return

            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                logger.error(f"Converted output is missing or empty: {output_path}")
                await update.message.reply_text(self.messages['empty_converted_file'])
                return
            
            # Conversion successful
            await update.message.reply_text(
                self.messages['conversion_complete'].format(output_filename=output_filename)
            )
            
            # Transfer to Kindle if connected
            if KindleTransfer.is_kindle_connected():
                await update.message.reply_text(self.messages['transferring_to_kindle'])
                
                transfer_success = KindleTransfer.transfer_file(output_path)
                
                if transfer_success:
                    await update.message.reply_text(self.messages['transfer_success'])
                else:
                    await update.message.reply_text(
                        self.messages['transfer_readonly_failed'].format(output_path=output_path)
                    )
            else:
                await update.message.reply_text(self.messages['kindle_not_connected'])
            
            # Cleanup
            try:
                os.remove(input_path)
            except Exception as e:
                logger.error(f"Error cleaning up input file: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error handling document: {str(e)}")
            await update.message.reply_text(self.messages['processing_error'])
    
    def setup_handlers(self):
        """Setup all command and message handlers"""
        self.application.add_handler(CommandHandler("start", self.start_command))
        self.application.add_handler(CommandHandler("help", self.help_command))
        self.application.add_handler(CommandHandler("status", self.status_command))
        self.application.add_handler(
            MessageHandler(filters.Document.ALL, self.handle_document)
        )
    
    async def run(self):
        """Start the bot"""
        self.application = Application.builder().token(self.bot_token).build()
        self.setup_handlers()
        
        logger.info("Starting Telegram bot...")
        await self.application.initialize()
        await self.application.start()
        await self.application.updater.start_polling()

        logger.info("Bot is running. Press Ctrl+C to stop.")

        try:
            # Keep the event loop alive so the updater can continuously process updates.
            await asyncio.Event().wait()
        finally:
            logger.info("Stopping Telegram bot...")
            if self.application.updater:
                await self.application.updater.stop()
            await self.application.stop()
            await self.application.shutdown()

def get_bot_instance():
    """Get singleton bot instance"""
    if not hasattr(get_bot_instance, '_instance'):
        get_bot_instance._instance = TelegramBotHandler()
    return get_bot_instance._instance
