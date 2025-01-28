import logging
import requests
from flask import Flask
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
import asyncio


# Flask app to keep the web service alive
app = Flask(__name__)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Replace with your bot's token from BotFather
BOT_TOKEN = "8112873353:AAEDnRHY7N0URG4V5fHdF5VI1bCCEfyuqDU"

# Command to start the bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text(
        "Welcome! Send me an image URL, and I'll download it for you."
    )

# Function to handle the image URL
async def handle_image_url(update: Update, context: CallbackContext) -> None:
    url = update.message.text.strip()
    user_id = update.message.chat_id

    # Validate URL
    if not url.startswith("http"):
        await update.message.reply_text("Please provide a valid image URL.")
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
            await context.bot.send_photo(chat_id=user_id, photo=f)

        await update.message.reply_text("Here is your downloaded image!")

    except requests.exceptions.RequestException as e:
        await update.message.reply_text(f"Failed to download the image. Error: {e}")

# Function to handle errors
async def error(update: Update, context: CallbackContext) -> None:
    logger.warning('Update "%s" caused error "%s"', update, context.error)

def main():
    # Initialize the bot application
    application = Application.builder().token(BOT_TOKEN).build()

    # Register handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_image_url))

    # Run the bot in polling mode
    asyncio.run(application.run_polling())

# Flask route to keep the service alive
@app.route('/')
def index():
    return 'Bot is running!'

if __name__ == "__main__":
    # Run the Flask app and the bot in the same thread
    main()
    app.run(host="0.0.0.0", port=5000)
