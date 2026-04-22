MESSAGES = {
    'start': (
        'Welcome to TECA-Send! 🎉\n\n'
        'Send me an ebook file (EPUB, MOBI, or AZW3) and I’ll convert it to Kindle format.\n'
        'If a Kindle device is connected to the server, I’ll transfer it automatically.\n\n'
        'Supported formats: EPUB, MOBI, AZW3'
    ),
    'help': (
        'Commands:\n'
        '/start - Welcome message\n'
        '/help - This help message\n'
        '/status - Check Kindle connection status\n\n'
        'Just send me an ebook file to get started!'
    ),
    'status_connected': '✅ Kindle device connected and ready for transfers!',
    'status_connected_readonly': (
        '⚠️ Kindle device connected, but the documents folder is read-only.\n'
        'Conversion will work, but automatic transfer will stay unavailable until write access is enabled.'
    ),
    'status_disconnected': (
        '⚠️ Kindle device is not connected.\n'
        'Files will still be converted, but they will not be transferred until a device is connected.'
    ),
    'unsupported_format': (
        '❌ Unsupported file format: {extension}\n'
        'Supported formats: {supported_formats}'
    ),
    'receiving_file': (
        '📥 File received: {file_name}\n'
        '🔄 Starting conversion...'
    ),
    'empty_downloaded_file': (
        '❌ The uploaded file looks empty after download. Please send it again and try once more.'
    ),
    'conversion_failed': (
        '❌ File conversion failed. Please try again or contact support.'
    ),
    'empty_converted_file': (
        '❌ Conversion produced an empty file. Please try another source file.'
    ),
    'conversion_complete': (
        '✅ Conversion completed!\n'
        'Output: {output_filename}'
    ),
    'transferring_to_kindle': '📱 Transferring to Kindle device...',
    'transfer_success': (
        '✅ File transferred successfully to Kindle!\n'
        'You can now safely disconnect your device.'
    ),
    'transfer_readonly_failed': (
        '⚠️ Conversion completed, but transfer to Kindle failed (the device may be read-only).\n'
        'The file is ready at: {output_path}'
    ),
    'kindle_not_connected': (
        '⚠️ Kindle device not connected.\n'
        'Your converted file is ready and waiting.'
    ),
    'processing_error': (
        '❌ An error occurred while processing your file. Please try again.'
    ),
}