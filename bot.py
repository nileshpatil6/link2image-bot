import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot's token from BotFather
BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"

# Command to start the bot
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(
        "Welcome! Send me an image URL, and I'll download it for you."
    )

# Function to handle the image URL
def handle_image_url(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()
    user_id = update.message.chat_id
    
    # Validate URL
    if not url.startswith("http"):
        update.message.reply_text("Please provide a valid image URL.")
        return

    try:
        # Download the image
        response = requests.get(url, stream=True)
        response.raise_for_status()

        # Save the image temporarily
        file_name = "downloaded_image.jpg"
        with open(file_name, "wb") as f:
            f.write(response.content)

        # Send the image back to the user
        with open(file_name, "rb") as f:
            context.bot.send_photo(chat_id=user_id, photo=f)

        update.message.reply_text("Here is your downloaded image!")

    except requests.exceptions.RequestException as e:
        update.message.reply_text(f"Failed to download the image. Error: {e}")

# Function to handle errors
def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Initialize the bot
    updater = Updater(BOT_TOKEN)

    # Get the dispatcher to register handlers
    dp = updater.dispatcher

    # Register commands and message handlers
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_image_url))

    # Log all errors
    dp.add_error_handler(error)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
