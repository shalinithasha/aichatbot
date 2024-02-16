import os
import logging
import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext
from telegram.error import TelegramError

# Set up logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Replace 'your-bot-token' with your actual bot token
BOT_TOKEN = '6588488706:AAFOUX4RAnHVGiAA_Dr_37Kxv6ciCQsCHtU'
BOT_URL = f'https://api.telegram.org/bot{BOT_TOKEN}/'

# Set up OpenAI API key and base URL
OPENAI_API_KEY = os.environ.get('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')
OPENAI_BASE_URL = 'https://api.openai.com/v1'

# Function to send a request to OpenAI
def openai_request(messages):
    headers = {
        'Authorization': f'Bearer {OPENAI_API_KEY}',
        'Content-Type': 'application/json'
    }
    data = {
        'model': 'text-davinci-003',
        'messages': messages,
        'temperature': 0.7,
        'max_tokens': 150
    }

    try:
        response = requests.post(OPENAI_BASE_URL + '/completions', headers=headers, json=data)
        response.raise_for_status()
        return response.json()['choices'][0]['text']
    except requests.exceptions.RequestException as e:
        logger.error(f'Error while sending a request to OpenAI: {e}')
        return 'An error occurred while processing your request. Please try again later.'

# Function to handle /start command
def start(update: Update, context: CallbackContext) -> None:
    update.message.reply_text('Hi! I am an AI chatbot. Feel free to ask any question.')

# Function to handle messages
def handle_message(update: Update, context: CallbackContext) -> None:
    chat_id = update.message.chat_id
    msg = update.message.text

    try:
        response = openai_request([{'role': 'user', 'content': msg}])
        update.message.reply_text(response)
    except TelegramError as e:
        logger.error(f'Telegram error: {e}')

# Function to handle errors
def error(update: Update, context: CallbackContext) -> None:
    logger.error(f'Update {update} caused error {context.error}')

# Set up the bot
def main() -> None:
    updater = Updater(token=BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    dispatcher.add_handler(CommandHandler('start', start))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    dispatcher.add_error_handler(error)

    updater.start_webhook(listen='0.0.0.0',
                          port=int(os.environ.get('PORT', 
