import logging
import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import config
from src.file_converter import FileConverter
from src.kindle_transfer import KindleTransfer

logger = logging.getLogger(__name__)

class TelegramBotHandler:
    """Handle Telegram bot interactions"""
    
    def __init__(self):
        self.bot_token = config.TELEGRAM_BOT_TOKEN
        self.application = None
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        await update.message.reply_text(
            "Welcome to TECA-Send! 🎉\n\n"
            "Send me an ebook file (EPUB, MOBI, or AZW3) and I'll convert it to Kindle format.\n"
            "If a Kindle device is connected, I'll transfer it automatically.\n\n"
            "Supported formats: EPUB, MOBI, AZW3"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(
            "Commands:\n"
            "/start - Welcome message\n"
            "/help - This help message\n"
            "/status - Check Kindle connection status\n\n"
            "Simply send me an ebook file to get started!"
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check Kindle connection status"""
        if KindleTransfer.is_kindle_connected():
            await update.message.reply_text(
                "✅ Kindle device is connected and ready!"
            )
        else:
            await update.message.reply_text(
                "⚠️ Kindle device is not connected.\n"
                "Files will still be converted, but won't be transferred until a device is connected."
            )
    
    async def handle_document(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle file uploads"""
        try:
            # Get file info
            document = update.message.document
            
            # Check file extension
            file_name = document.file_name
            if not FileConverter.is_supported(file_name):
                await update.message.reply_text(
                    f"❌ Unsupported file format: {Path(file_name).suffix}\n"
                    f"Supported formats: {', '.join(FileConverter.SUPPORTED_FORMATS)}"
                )
                return
            
            # Download file
            await update.message.reply_text(
                f"📥 Received file: {file_name}\n"
                "🔄 Starting conversion..."
            )
            
            file = await context.bot.get_file(document.file_id)
            input_path = os.path.join(config.UPLOAD_DIR, file_name)
            await file.download_to_drive(input_path)
            
            # Convert file
            output_filename = FileConverter.get_output_filename(file_name)
            output_path = os.path.join(config.CONVERT_DIR, output_filename)
            
            conversion_success = FileConverter.convert(input_path, output_path)
            
            if not conversion_success:
                await update.message.reply_text(
                    "❌ File conversion failed. Please try again or contact support."
                )
                return
            
            # Conversion successful
            await update.message.reply_text(
                f"✅ Conversion completed!\n"
                f"Output: {output_filename}"
            )
            
            # Transfer to Kindle if connected
            if KindleTransfer.is_kindle_connected():
                await update.message.reply_text(
                    "📱 Transferring to Kindle device..."
                )
                
                transfer_success = KindleTransfer.transfer_file(output_path)
                
                if transfer_success:
                    await update.message.reply_text(
                        f"✅ File successfully transferred to Kindle!\n"
                        f"You can now safely disconnect your device."
                    )
                else:
                    await update.message.reply_text(
                        f"⚠️ Conversion completed, but transfer to Kindle failed.\n"
                        f"File is ready at: {output_path}"
                    )
            else:
                await update.message.reply_text(
                    f"⚠️ Kindle device not connected.\n"
                    f"Your converted file is ready and waiting."
                )
            
            # Cleanup
            try:
                os.remove(input_path)
            except Exception as e:
                logger.error(f"Error cleaning up input file: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error handling document: {str(e)}")
            await update.message.reply_text(
                "❌ An error occurred while processing your file. Please try again."
            )
    
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

def get_bot_instance():
    """Get singleton bot instance"""
    if not hasattr(get_bot_instance, '_instance'):
        get_bot_instance._instance = TelegramBotHandler()
    return get_bot_instance._instance
