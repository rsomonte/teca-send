import asyncio
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
            "Bienvenido a TECA-Send! 🎉\n\n"
            "Envíame un archivo de ebook (EPUB, MOBI o AZW3) y lo convertiré al formato de Kindle.\n"
            "Si un dispositivo Kindle está conectado al servidor, lo transferiré automáticamente.\n\n"
            "Formatos soportados: EPUB, MOBI, AZW3"
        )
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        await update.message.reply_text(
            "Commands:\n"
            "/start - Mensaje de bienvenida\n"
            "/help - Este mensaje de ayuda\n"
            "/status - Verificar estado de conexión de Kindle\n\n"
            "Simplemente envíame un archivo de ebook para comenzar!"
        )
    
    async def status_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Check Kindle connection status"""
        if KindleTransfer.is_kindle_connected() and KindleTransfer.is_kindle_writable():
            await update.message.reply_text(
                "✅ Dispositivo Kindle conectado y listo para transferencias!"
            )
        elif KindleTransfer.is_kindle_connected():
            await update.message.reply_text(
                "⚠️ Dispositivo Kindle conectado, pero la carpeta de documentos es de solo lectura.\n"
                "La conversión funcionará, pero la transferencia automática no estará disponible hasta que se habilite el acceso de escritura."
            )
        else:
            await update.message.reply_text(
                "⚠️ Dispositivo Kindle no está conectado.\n"
                "Los archivos seguirán siendo convertidos, pero no se transferirán hasta que se conecte un dispositivo."
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
                    f"❌ Formato de archivo no soportado: {Path(file_name).suffix}\n"
                    f"Formatos soportados: {', '.join(FileConverter.SUPPORTED_FORMATS)}"
                )
                return
            
            # Download file
            await update.message.reply_text(
                f"📥 Archivo recibido: {file_name}\n"
                "🔄 Iniciando conversión..."
            )
            
            file = await context.bot.get_file(document.file_id)
            input_path = os.path.join(config.UPLOAD_DIR, file_name)
            await file.download_to_drive(input_path)

            if not os.path.exists(input_path) or os.path.getsize(input_path) == 0:
                logger.error(f"Downloaded file is missing or empty: {input_path}")
                await update.message.reply_text(
                    "❌ El archivo subido parece estar vacío después de la descarga. "
                    "Por favor, reenvía el archivo y vuelve a intentarlo."
                )
                return
            
            # Convert file
            output_filename = FileConverter.get_output_filename(file_name)
            output_path = os.path.join(config.CONVERT_DIR, output_filename)
            
            conversion_success = FileConverter.convert(input_path, output_path)
            
            if not conversion_success:
                await update.message.reply_text(
                    "❌ La conversión del archivo falló. Por favor, intenta de nuevo o contacta con soporte."
                )
                return

            if not os.path.exists(output_path) or os.path.getsize(output_path) == 0:
                logger.error(f"Converted output is missing or empty: {output_path}")
                await update.message.reply_text(
                    "❌ La conversión produjo un archivo vacío. "
                    "Por favor, intenta con otro archivo fuente."
                )
                return
            
            # Conversion successful
            await update.message.reply_text(
                f"✅ Conversión completada!\n"
                f"Salida: {output_filename}"
            )
            
            # Transfer to Kindle if connected
            if KindleTransfer.is_kindle_connected():
                await update.message.reply_text(
                    "📱 Transfiriendo al dispositivo Kindle..."
                )
                
                transfer_success = KindleTransfer.transfer_file(output_path)
                
                if transfer_success:
                    await update.message.reply_text(
                        f"✅ Archivo transferido exitosamente al Kindle!\n"
                        f"Ahora puedes desconectar tu dispositivo de forma segura."
                    )
                else:
                    await update.message.reply_text(
                        f"⚠️ Conversión completada, pero la transferencia al Kindle falló (el dispositivo puede estar en modo de solo lectura).\n"
                        f"El archivo está listo en: {output_path}"
                    )
            else:
                await update.message.reply_text(
                    f"⚠️ Dispositivo Kindle no conectado.\n"
                    f"Tu archivo convertido está listo y esperando."
                )
            
            # Cleanup
            try:
                os.remove(input_path)
            except Exception as e:
                logger.error(f"Error cleaning up input file: {str(e)}")
            
        except Exception as e:
            logger.error(f"Error handling document: {str(e)}")
            await update.message.reply_text(
                "❌ Ocurrió un error mientras se procesaba tu archivo. Por favor, inténtalo de nuevo."
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
