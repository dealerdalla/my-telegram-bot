import os
import sys
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Set up detailed logging ---
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# --- Configuration & Sanity Checks ---
logger.info("Starting bot configuration...")

# 1. Get Bot Token
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    logger.critical("FATAL ERROR: TELEGRAM_TOKEN environment variable is not set!")
    sys.exit(1)
logger.info("TELEGRAM_TOKEN loaded successfully.")

# 2. Get Port
try:
    PORT = int(os.environ.get('PORT', 8443))
    logger.info(f"PORT is set to {PORT}.")
except ValueError:
    logger.critical("FATAL ERROR: Invalid PORT environment variable.")
    sys.exit(1)

# 3. Get Render URL (This is crucial for webhooks)
RENDER_URL = os.environ.get("RENDER_EXTERNAL_URL")
if not RENDER_URL:
    logger.critical("FATAL ERROR: RENDER_EXTERNAL_URL environment variable not found. Cannot set webhook.")
    sys.exit(1)
logger.info(f"Host URL is {RENDER_URL}.")


TARGET_USERNAME = "@indiandalla1bot"


# --- Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the pre-determined username."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=TARGET_USERNAME
    )


def main() -> None:
    """Starts the bot."""
    logger.info("Creating Telegram Application...")
    application = Application.builder().token(BOT_TOKEN).build()

    logger.info("Adding /start command handler...")
    application.add_handler(CommandHandler("start", start))

    # This is the full URL that Telegram will send updates to
    webhook_url = f"{RENDER_URL}/{BOT_TOKEN}"
    
    logger.info(f"Starting webhook and listening on port {PORT}...")
    logger.info(f"Telegram will be set to call this URL: {webhook_url}")

    # Run the bot in webhook mode
    application.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=BOT_TOKEN,  # The secret path part of the URL
        webhook_url=webhook_url
    )


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Log any other unexpected crashes
        logger.critical("Bot crashed with an unhandled exception!", exc_info=True)
