# YT_TT_downloader

A simple personal project that provides two main pieces:

- a lightweight downloader script for video/audio (uses `yt-dlp`),
- a Telegram bot interface that lets you download media via chat.

This repository is intended as a small utility for private use and testing.

## Features

- Download YouTube / TikTok and other supported sites using `yt-dlp`.
- Optional Telegram bot to trigger downloads and receive files via chat.
- Minimal local setup using a Python virtual environment.

## Requirements

- Python 3.9+ (tested with 3.10/3.11)
- `yt-dlp`
- `python-telegram-bot` (if using the Telegram bot)

If you prefer, you can use the included virtual environment under `bot_env`, or create your own.

## Setup

1. (Optional) Create a virtual environment:

```powershell
python -m venv bot_env
```

2. Activate the virtual environment (PowerShell example):

```powershell
.\bot_env\Scripts\Activate.ps1
```

3. Install dependencies. If you have a `requirements.txt`, use it; otherwise install the main packages:

```powershell
pip install yt-dlp python-telegram-bot
```

## Configuration

- Telegram bot: set your bot token as an environment variable named `TELEGRAM_TOKEN`, or edit the bot's config file if one exists in `bot_env/`.
- (Optional) Adjust any download options inside `downloader.py`.

Example (PowerShell):

```powershell
$env:TELEGRAM_TOKEN = "<your-telegram-bot-token>"
```

## Running

- Run the downloader directly to fetch media:

```powershell
python downloader.py <URL>
```

- Run the Telegram bot (replace `bot_script.py` with your bot entrypoint if different):

```powershell
python bot_env/bot_script.py
```

If your bot script is named differently, run that file instead.

## Usage examples

- Download a YouTube video manually:

```powershell
python downloader.py "https://www.youtube.com/watch?v=..."
```

- Send a URL to the Telegram bot chat and the bot will download and return the file (subject to size limits).

## Notes & Troubleshooting

- Large files may exceed Telegram's max file size for direct upload; in that case send a link or use cloud storage.
- If `yt-dlp` reports missing formats or fails, update it:

```powershell
python -m pip install -U yt-dlp
```

- If the bot doesn't start, confirm `TELEGRAM_TOKEN` is set and that required packages are installed in the active environment.

## Security & Legal

This project is provided for personal/educational use. Respect copyright and the terms of service of content providers.

## Files of interest

- `downloader.py`: downloader entrypoint used to fetch media.
- `bot_env/`: virtualenv and bot-related files (edit or add your bot script here).

## License

Personal project — no explicit license. Add one if you plan to publish or share this repository.
