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
    texts = json.load(file)

# Const for states
START = range(1)

# Func for start messages and for keyboad
def start(update: Update, context: CallbackContext) -> int:
    logger.info("start called")
    chat_id = update.message.chat_id

    keyboard = [['🚩Rules', '🎉Rooms'],
                ['🤵Profile', '👬Pairs']]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

    with open('assets/pictures/start_pic.png', 'rb') as photo_file:
        context.bot.send_photo(chat_id=chat_id, photo=photo_file)

    update.message.reply_text(texts['start_message']['русский'], reply_markup=reply_markup)
    update.message.reply_text(texts['start_message']['english'])

    select_language(update, context)

    return START

# Func for handling keyboard buttons
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

# Func for create inline keyboard
def select_language(update: Update, context: CallbackContext) -> int:
    logger.info("select_language called")

    keyboard = [
        [InlineKeyboardButton("🇷🇺Русский", callback_data='русский')],
        [InlineKeyboardButton("🇬🇧English", callback_data='english')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Для начала выберем язык бота:\nFirst, let's select the bot language:", reply_markup=reply_markup)

    return START

# Func for localization bot messages
def localization(text_key, update, language, input_method = 'update'):
    logger.info("localization called")

    text_message = texts[text_key].get(language, "Text not found")

    if input_method == 'query':
        query = update.callback_query
        query.edit_message_text(text_message)
    else:
        update.message.reply_text(text_message)

# Func for handling inline keyboard and creating anonym customer with language
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

            localization("selected_language", update, language, 'query')

        else:
            language = user[5]
            
            localization("existing_language", update, language, 'query')

    except Exception as e:
        logger.error(f"Error: {e}")

# Func for create customer without info but only for save language
def create_anonym_user(user_data, update: Update):
    logger.info("create_anonym_user called")

    try:
        db.create_user(user_data)
    except Exception as e:
        logger.error(f"Error: {e}")

# Func for define customer language
def define_language(update: Update, telegramUserID):
    logger.info("define_language called")

    try:
        user = db.read_user(telegramUserID)
        if user is None:
            update.message.reply_text("Profile does not exist")
        else:
            language = user[5]

    except Exception as e:
        logger.error(f"Error: {e}")

    return language

# Func for show rules for customer
def open_rules(update, context):
    logger.info("open_rules called")

    telegramUserId = update.message.from_user.id
    chat_id = update.message.chat_id

    with open(r'assets/pictures/rules_pic.png', 'rb') as photo_file:
        context.bot.send_photo(chat_id=chat_id, photo=photo_file)

    language = define_language(update, telegramUserId)
    
    localization('rules', update, language)

# Func for changing the language
def change_language(update: Update, context: CallbackContext):
    logger.info("change_language called")

    telegramUserID = update.message.from_user.id
    parameter = "Language"

    language = define_language(update, telegramUserID)

    if language == "русский":
        language = "english"
    elif language == "english":
        language = "русский"

    try:
        db.update_user(telegramUserID, parameter, language)

    except Exception as e:
        logger.error(f"Error: {e}")

    localization('changed_language', update, language)

def open_rooms(update, context):
    update.message.reply_text("open_rooms called")

def open_profile(update, context):
    update.message.reply_text("open_profile called")

def open_pairs(update, context):
    update.message.reply_text("open_pairs called")

# Func for stop convers with bot
def cancel(update: Update, context: CallbackContext):
    logger.info("cancel called")

    telegramUserId = update.message.from_user.id

    language = define_language(update, telegramUserId)
    
    localization('end_conversation', update, language)

    context.user_data.clear()

    return ConversationHandler.END