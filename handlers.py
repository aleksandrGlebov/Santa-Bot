import json
import logging
import data.database_helpers as db
from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, ConversationHandler

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Open assests
with open("assets/texts/texts.json", "r", encoding="utf-8") as file:
    bot_texts = json.load(file)

# Const for states
START = range(1)

def start(update: Update, context: CallbackContext) -> int:
    logger.info("start called")
    chat_id = update.message.chat_id

    keyboard = [['🚩Rules', '🎉Rooms'],
                ['🤵Profile', '👬Pairs']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    photo_file = open('assets\pictures\start_pic.png', 'rb')
    context.bot.send_photo(chat_id=chat_id, photo=photo_file)
    update.message.reply_text(bot_texts['start_message']['ru'], reply_markup=reply_markup)
    update.message.reply_text(bot_texts['start_message']['en'])

    select_language(update, context)

    return START

def menu_buttons(update: Update, context: CallbackContext):
    logger.info("menu_buttons")

    text = update.message.text

    if text == "🚩Rules":
        return open_rules(update, context)
    elif text == "🎉Rooms":
        return open_rooms(update, context)
    elif text == "🤵Profile":
        return open_profile(update, context)
    elif text == "👬Pairs":
        return open_pairs(update, context)

def select_language(update: Update, context: CallbackContext) -> int:
    logger.info("select_language called")

    keyboard = [
        [InlineKeyboardButton("🇷🇺Русский", callback_data='русский')],
        [InlineKeyboardButton("🇬🇧English", callback_data='english')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Для начала выберем язык бота:\nFirst, let's select the bot language:", reply_markup=reply_markup)

    return START

def button_language(update: Update, context: CallbackContext):
    logger.info("button_language called")

    query = update.callback_query
    language = query.data
    telegramUserID = query.from_user.id

    context.user_data['language'] = language
    context.user_data['telegramUserID'] = telegramUserID

    try:
        user = db.read_user(telegramUserID)
        
        if user is None:
            create_anonym_user(context.user_data, update)
            
            if language == "русский":
                query.edit_message_text(bot_texts['selected_language']['ru'])
            elif language == "english":
                query.edit_message_text(bot_texts['selected_language']['en'])
        else:
            language = user[5]
            
            if language == "русский":
                query.edit_message_text(bot_texts['existing_language']['ru'])
            elif language == "english":
                query.edit_message_text(bot_texts['existing_language']['en'])

    except Exception as e:
        logger.error(f"Error: {e}")

def create_anonym_user(user_data, update: Update):
    logger.info("create_anonym_user called")

    try:
        db.create_user(user_data)
    except Exception as e:
        logger.error(f"Error: {e}")

def define_language(update: Update, telegramUserID):
    try:
        user = db.read_user(telegramUserID)
        if user is None:
            update.message.reply_text("Profile does not exist")
        else:
            language = user[5]

    except Exception as e:
        logger.error(f"Error: {e}")

    return language

def open_rules(update, context):
    logger.info("open_rules called")

    telegramUserId = update.message.from_user.id
    chat_id = update.message.chat_id

    photo_file = open(r'assets/pictures/rules_pic.png', 'rb')
    context.bot.send_photo(chat_id=chat_id, photo=photo_file)

    language = define_language(update, telegramUserId)
    
    if language == "русский":
        update.message.reply_text(bot_texts['rules']['ru'])
    elif language == "english":
        update.message.reply_text(bot_texts['rules']['en'])

def change_language(update: Update, context: CallbackContext):
    logger.info("change_language called")

    telegramUserID = update.message.from_user.id
    parameter = "Language"

    language = define_language(update, telegramUserID)

    if language == "русский":
        language = "english"
        update.message.reply_text(bot_texts['changed_language']['en'])
    elif language == "english":
        language = "русский"
        update.message.reply_text(bot_texts['changed_language']['ru'])
        
    try:
        db.update_user(telegramUserID, parameter, language)

    except Exception as e:
        logger.error(f"Error: {e}")

def open_rooms(update, context):
    update.message.reply_text("open_rooms called")

def open_profile(update, context):
    update.message.reply_text("open_profile called")

def open_pairs(update, context):
    update.message.reply_text("open_pairs called")

def cancel(update: Update, context: CallbackContext):
    logger.info("cancel called")

    telegramUserId = update.message.from_user.id

    language = define_language(update, telegramUserId)
    
    if language == "русский":
        update.message.reply_text(bot_texts['end_conversation']['ru'])
    elif language == "english":
        update.message.reply_text(bot_texts['end_conversation']['en'])

    context.user_data.clear()

    return ConversationHandler.END