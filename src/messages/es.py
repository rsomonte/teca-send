MESSAGES = {
    'start': (
        '¡Bienvenido a TECA-Send! 🎉\n\n'
        'Envíame un archivo de ebook (EPUB, MOBI o AZW3) y lo convertiré al formato de Kindle.\n'
        'Si un dispositivo Kindle está conectado al servidor, lo transferiré automáticamente.\n\n'
        'Formatos soportados: EPUB, MOBI, AZW3'
    ),
    'help': (
        'Comandos:\n'
        '/start - Mensaje de bienvenida\n'
        '/help - Este mensaje de ayuda\n'
        '/status - Verificar estado de conexión de Kindle\n\n'
        '¡Solo envíame un archivo de ebook para comenzar!'
    ),
    'status_connected': '✅ ¡Dispositivo Kindle conectado y listo para transferencias!',
    'status_connected_readonly': (
        '⚠️ El dispositivo Kindle está conectado, pero la carpeta de documentos es de solo lectura.\n'
        'La conversión funcionará, pero la transferencia automática seguirá sin estar disponible hasta habilitar el acceso de escritura.'
    ),
    'status_disconnected': (
        '⚠️ El dispositivo Kindle no está conectado.\n'
        'Los archivos seguirán convirtiéndose, pero no se transferirán hasta que se conecte un dispositivo.'
    ),
    'unsupported_format': (
        '❌ Formato de archivo no soportado: {extension}\n'
        'Formatos soportados: {supported_formats}'
    ),
    'receiving_file': (
        '📥 Archivo recibido: {file_name}\n'
        '🔄 Iniciando conversión...'
    ),
    'empty_downloaded_file': (
        '❌ El archivo subido parece estar vacío después de la descarga. Vuelve a enviarlo e inténtalo otra vez.'
    ),
    'conversion_failed': (
        '❌ La conversión del archivo falló. Por favor, intenta de nuevo o contacta con soporte.'
    ),
    'empty_converted_file': (
        '❌ La conversión produjo un archivo vacío. Por favor, intenta con otro archivo fuente.'
    ),
    'conversion_complete': (
        '✅ ¡Conversión completada!\n'
        'Salida: {output_filename}'
    ),
    'transferring_to_kindle': '📱 Transfiriendo al dispositivo Kindle...',
    'transfer_success': (
        '✅ ¡Archivo transferido exitosamente al Kindle!\n'
        'Ahora puedes desconectar tu dispositivo de forma segura.'
    ),
    'transfer_readonly_failed': (
        '⚠️ La conversión se completó, pero la transferencia al Kindle falló (el dispositivo puede estar en modo de solo lectura).\n'
        'El archivo está listo en: {output_path}'
    ),
    'kindle_not_connected': (
        '⚠️ El dispositivo Kindle no está conectado.\n'
        'Tu archivo convertido está listo y esperando.'
    ),
    'processing_error': (
        '❌ Ocurrió un error mientras se procesaba tu archivo. Por favor, inténtalo de nuevo.'
    ),
}