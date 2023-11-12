import json
import logging
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

with open("assets/texts/texts.json", "r", encoding="utf-8") as file:
    bot_texts = json.load(file)

START = range(1)

def start(update: Update, context: CallbackContext) -> int:
    context.user_data['telegramUserID'] = update.message.from_user.id

    keyboard = [['🚩Rules', '🎉Rooms'],
                ['🤵Profile', '👬Pairs']]

    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    update.message.reply_text(bot_texts['start_message']['ru'], reply_markup=reply_markup)

    return START

def menu_buttons(update: Update, context: CallbackContext) -> int:
    text = update.message.text

    if text == "🚩Rules":
        return rules(update, context)
    elif text == "🎉Rooms":
        return open_rooms(update, context)
    elif text == "🤵Profile":
        return open_profile(update, context)
    elif text == "👬Pairs":
        return open_pairs(update, context)
    
def rules(update, context):
    update.message.reply_text(bot_texts['rules']['ru'])

def open_rooms(update, context):
    update.message.reply_text("open_rooms called")

def open_profile(update, context):
    update.message.reply_text("open_profile called")

def open_pairs(update, context):
    update.message.reply_text("open_pairs called")

def cancel(update: Update, context: CallbackContext):
    update.message.reply_text('Разговор отменен. Чтобы начать сначала, нажмите /start.')

    context.user_data.clear()

    return ConversationHandler.END