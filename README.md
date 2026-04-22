# TECA-Send
> Pronounced as "teck-uh" send. Teca comes from the Spanish word "Azteca"(Aztec), and since reading was so valuable and holy for the Aztecs, I thought it would be appropriate for a project that democratises the process of sending ebooks to Kindle devices. 

A Telegram bot service that converts ebook files (EPUB, MOBI, AZW3) to Kindle-compatible formats and automatically transfers them to connected Kindle devices.

## Features

- 📱 **Telegram Bot Interface** - Send files directly through Telegram
- 📖 **Ebook Conversion** - Converts EPUB, MOBI, and AZW3 formats using Calibre
- 🎯 **Kindle Integration** - Automatic transfer to connected Kindle devices
- 📬 **Status Messages** - Real-time updates on conversion and transfer progress
- 🐳 **Docker Ready** - Easy deployment with Docker and Docker Compose

## Prerequisites

- Docker and Docker Compose (for containerized deployment)
- Telegram Bot Token (get from [@BotFather](https://t.me/botfather))
- Python 3.11+ (for local development)
- Calibre (or install via Docker)

## Installation

### Using Docker (Recommended)

1. Clone the repository:
```bash
cd /path/to/dir/teca-send
```

2. Create `.env` file from template:
```bash
cp .env.example .env
```

3. Edit `.env` and add your Telegram bot token:
```
TELEGRAM_BOT_TOKEN=your_bot_token_here
```

4. Build and run:
```bash
docker-compose up -d
```

### Local Development

1. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Install Calibre:
```bash
# Ubuntu/Debian
sudo apt-get install calibre

# macOS
brew install calibre
```

4. Create `.env` file:
```bash
cp .env.example .env
```

5. Add your bot token to `.env`

6. Run the bot:
```bash
python src/main.py
```

## Usage

1. Start the bot in Telegram: `/start`
2. Send an ebook file (EPUB, MOBI, or AZW3)
3. The bot will:
   - Acknowledge receipt
   - Convert to Kindle format
   - Transfer to Kindle (if connected)
   - Send completion message

### Commands

- `/start` - Welcome and usage instructions
- `/help` - Show available commands
- `/status` - Check Kindle device connection status

## Configuration

Edit `.env` file to customize:

```env
TELEGRAM_BOT_TOKEN=your_token        # Required: Your Telegram bot token
KINDLE_MOUNT_POINT=/mnt/kindle       # Host path where Kindle is mounted
CONTAINER_KINDLE_MOUNT_POINT=/kindle # Container path mapped to host Kindle mount
KINDLE_MOUNT_OPTIONS=rw,z            # Bind options; use rw,z on SELinux hosts (Fedora/RHEL)
KINDLE_DOCUMENTS_FOLDER=documents    # Target folder on Kindle
OUTPUT_FORMAT=mobi                   # Output format (mobi, pdf, etc.)
LOG_LEVEL=INFO                       # Logging level (DEBUG, INFO, WARNING, ERROR)
```

## Project Structure

```
teca-send/
├── src/
│   ├── main.py                 # Entry point
│   ├── telegram_bot.py         # Telegram bot handler
│   ├── file_converter.py       # Ebook conversion logic
│   ├── kindle_transfer.py      # Kindle device operations
│   └── config.py               # Configuration management
├── config/
├── tests/                      # Unit tests (to be added)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

## Architecture

- **Telegram Bot**: Async handler using `python-telegram-bot` library
- **File Converter**: Wrapper around Calibre's `ebook-convert` command
- **Kindle Transfer**: Manages USB mount detection and file copy operations
- **Docker**: Multi-stage build with Calibre support

## Troubleshooting

### Kindle not detected
- Ensure device is connected and mounted
- Check `KINDLE_MOUNT_POINT` in `.env` points to the host mount path (example: `/run/media/<user>/Kindle`)
- Verify permissions on the host mount path

### Kindle connected but read-only in container
- On Fedora/RHEL with SELinux, set `KINDLE_MOUNT_OPTIONS=rw,z` in `.env`
- If the Kindle is mounted as VFAT/exFAT and still read-only, set `CONTAINER_SECURITY_OPT=label=disable` in `.env`
- Recreate the service after changing mount options: `docker compose up -d --build`
- Validate from container: `docker compose exec teca-send sh -lc 'touch /kindle/documents/.teca_write_test && rm /kindle/documents/.teca_write_test'`

### Conversion fails
- Ensure Calibre is installed
- Check ebook format is valid
- Review logs: `docker logs teca-send`

### Bot not responding
- Verify `TELEGRAM_BOT_TOKEN` in `.env`
- Check internet connection
- Review logs for errors

## Development

### Running Tests
```bash
pytest tests/
```

### Building Docker Image
```bash
docker build -t teca-send:latest .
```

### Checking Logs
```bash
docker-compose logs -f teca-send
```

## Support

For issues, questions, or suggestions, please open an issue on GitHub.

## Language Support

If you want to serve the bot in Spanish, change the branch to `spanish` and redeploy. The bot will respond in Spanish, but the configuration and logs will still be in English. (Planning on changing this via env vars in the future)