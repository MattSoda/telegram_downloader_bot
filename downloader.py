from telegram import Update
import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from telegram.request import HTTPXRequest
import yt_dlp
import os
import shutil
from pathlib import Path
import time

logging.basicConfig(level=logging.INFO)


# TOKEN = os.environ.get("8500282127:AAEJHUNhND70Nti4ngnbQTEAI7ZK63ix-7M")
TOKEN = "8500282127:AAEJHUNhND70Nti4ngnbQTEAI7ZK63ix-7M"

# Detect ffmpeg: first check PATH, then a common downloads location
FFMPEG_PATH = shutil.which("ffmpeg")
if not FFMPEG_PATH:
    possible = Path.home() / "Downloads" / "ffmpeg-8.0.1-essentials_build" / "ffmpeg-8.0.1-essentials_build" / "bin" / "ffmpeg.exe"
    if possible.exists():
        FFMPEG_PATH = str(possible)

if FFMPEG_PATH:
    logging.info(f"ffmpeg found at {FFMPEG_PATH}")
else:
    logging.warning("ffmpeg not found on PATH. yt-dlp may fail to merge formats.")

request = HTTPXRequest(
    read_timeout=60.0,
    write_timeout=600.0,
    connect_timeout=20.0,
    pool_timeout=300.0,
    media_write_timeout=600.0,
    connection_pool_size=64,
)

# Start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to the YouTube/TikTok Downloader Bot! Send me a link to download media.")


async def error_handler(update: object, context: ContextTypes.DEFAULT_TYPE):
    logging.exception("Unhandled exception in update handler", exc_info=context.error)

# Download - returns the downloaded file path
def download_video(url):
    os.makedirs('downloads', exist_ok=True)
    ydl_opts = {
    'format': 'bestvideo+bestaudio/best',
    'outtmpl': 'downloads/%(title)s.%(ext)s',
    'merge_output_format': 'mp4',
    'quiet': True,
    'no_warnings': True,
    'socket_timeout': 60,
    'retries': 10,
    'http_chunk_size': 1048576,
    'http_headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
        'Referer': 'https://www.tiktok.com/'
    },
    
    # optional if you need a proxy:
    # 'proxy': 'http://HOST:PORT',
}
    if FFMPEG_PATH:
        ydl_opts['ffmpeg_location'] = FFMPEG_PATH

    # Retry/backoff loop for transient download errors
    max_attempts = 3
    backoff = 2
    for attempt in range(1, max_attempts + 1):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                file_path = ydl.prepare_filename(info)
            return file_path
        except Exception as e:
            logging.exception("Download attempt %s failed", attempt)
            if attempt == max_attempts:
                raise
            time.sleep(backoff)
            backoff *= 2

# Message Handler
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text.strip()
    await update.message.reply_text("Downloading...")
    try:
        file_path = download_video(url)
        await update.message.reply_text("Uploading...")

        file_size = os.path.getsize(file_path)
        ext = os.path.splitext(file_path)[1].lower()

        # Retry uploads to Telegram on transient network errors
        send_max_attempts = 3
        send_backoff = 2
        for send_attempt in range(1, send_max_attempts + 1):
            try:
                # If it's a common video type and small enough, send as video; otherwise send as document
                if file_size <= 50 * 1024 * 1024 and ext in ('.mp4', '.mkv', '.webm', '.mov', '.avi'):
                    with open(file_path, "rb") as f:
                        await update.message.reply_video(video=f, caption="Downloaded by @YouTube_TikTok_Downloader_MM_bot")
                else:
                    with open(file_path, "rb") as f:
                        await update.message.reply_document(document=f, caption="Downloaded by @YouTube_TikTok_Downloader_MM_bot")

                os.remove(file_path)
                break
            except Exception as e:
                logging.exception("Upload attempt %s failed", send_attempt)
                if send_attempt == send_max_attempts:
                    # re-raise to be caught by outer handler
                    raise
                time.sleep(send_backoff)
                send_backoff *= 2

    except Exception as e:
        await update.message.reply_text(f"Failed to download or send file: {e}")

# Main Function
def main():
    app = Application.builder().token(TOKEN).request(request).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_error_handler(error_handler)

    print("Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()