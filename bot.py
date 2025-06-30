import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# --- Configuration ---
# Get the bot token from an environment variable for security
# We will set this in the Render dashboard later
BOT_TOKEN = os.environ.get("TELEGRAM_TOKEN")
if not BOT_TOKEN:
    print("Error: TELEGRAM_TOKEN environment variable not set.")
    exit()

# This is the username the bot will send
TARGET_USERNAME = "@the_username_you_set"

# The port number your web service will listen on. Render will set this.
PORT = int(os.environ.get('PORT', 8443))

# --- Bot Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Sends the pre-determined username when the /start command is issued."""
    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=TARGET_USERNAME
    )

def main() -> None:
    """Start the bot with webhooks."""
    
    # Create the Application object
    application = Application.builder().token(BOT_TOKEN).build()

    # Add the handler for the /start command
    application.add_handler(CommandHandler("start", start))

    # Get the public URL provided by Render
    # We will set this in the Render dashboard
    render_url = os.environ.get("RENDER_EXTERNAL_URL")
    if not render_url:
        print("Error: RENDER_EXTERNAL_URL environment variable not set.")
        # Don't exit if running locally, just warn
    else:
        # Start the bot with webhooks
        print(f"Starting bot with webhook at {render_url}")
        application.run_webhook(
            listen="0.0.0.0",
            port=PORT,
            url_path=BOT_TOKEN,  # A secret path so only Telegram can find it
            webhook_url=f"{render_url}/{BOT_TOKEN}"
        )

if __name__ == "__main__":
    main()
