from functools import wraps
import json
import logging
import data.database_helpers as db
import handlers as hd

# Logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Open assests
with open("assets/texts/texts.json", "r", encoding="utf-8") as file:
    bot_texts = json.load(file)

def validate_text_input(state_if_error):
    def decorator_wrapper(func):
        @wraps(func)
        def wrapped(update, context):
            text_input = update.message.text
            telegramUserId = update.message.from_user.id
            language = hd.define_language(update, telegramUserId)

            if not text_input:
                if language == "русский":
                    update.message.reply_text(bot_texts['empty_text_input']['ru'])
                elif language == "english":
                    update.message.reply_text(bot_texts['empty_text_input']['en'])
                return state_if_error
            
            if  len(text_input) > 256:
                if language == "русский":
                    update.message.reply_text(bot_texts['long_text_input']['ru'])
                elif language == "english":
                    update.message.reply_text(bot_texts['long_text_input']['en'])
                return state_if_error
            
            if  len(text_input) < 3:
                if language == "русский":
                    update.message.reply_text(bot_texts['short_text_input']['ru'])
                elif language == "english":
                    update.message.reply_text(bot_texts['short_text_input']['en'])
                return state_if_error

            if not any(char.isalpha() for char in text_input):
                if language == "русский":
                    update.message.reply_text(bot_texts['incorrect_text_input']['ru'])
                elif language == "english":
                    update.message.reply_text(bot_texts['incorrect_text_input']['en'])
                return state_if_error

            return func(update, context)

        return wrapped
    return decorator_wrapper

def validate_numeric_input(min_value, max_value, state_if_error, float_allowed=True):
    def decorator_wrapper(func):
        @wraps(func)
        def wrapped(update, context):
            value = update.message.text
            telegramUserId = update.message.from_user.id
            language = hd.define_language(update, telegramUserId)

            if not value.replace('.', '', 1).isdigit() or (float_allowed and '.' in value and value.count('.') > 1):
                if language == "русский":
                    update.message.reply_text(bot_texts['incorrect_numeric_input']['ru'])
                elif language == "english":
                    update.message.reply_text(bot_texts['incorrect_numeric_input']['en'])
                return state_if_error
            
            numeric_value = float(value) if float_allowed and '.' in value else int(value)

            if not (min_value <= numeric_value <= max_value):
                if language == "русский":
                    message_template = bot_texts['incorrect_range_numeric_input']['ru']
                elif language == "english":
                    message_template = bot_texts['incorrect_range_numeric_input']['en']

                formatted_message = message_template.format(min_value=min_value, max_value=max_value)
                update.message.reply_text(formatted_message)
                return state_if_error
            
            return func(update, context)
        
        return wrapped
    return decorator_wrapper

def checking_profile_existence(state_if_error):
    def decorator_wrapper(func):
        @wraps(func)
        def wrapped(update, context):
            telegramUserId = update.message.from_user.id
            language = hd.define_language(update, telegramUserId)
            
            try:
                user = db.read_user(telegramUserId)

                if user is None:
                    context.user_data['isProfileExist'] = 'No'
                    update.message.reply_text(bot_texts['profile_doesnt_exist']['en'])
                    return state_if_error
                
                else:
                    userName = user[2]

                    if userName is None:
                        if language == "русский":
                            update.message.reply_text(bot_texts['anonymous_profile']['ru'])
                        elif language == "english":
                            update.message.reply_text(bot_texts['anonymous_profile']['en'])
                        return state_if_error
                    
                    else:
                        context.user_data['isProfileExist'] = 'Yes'
                        return func(update, context)
                    
            except Exception as e:
                logger.error(f"Error: {e}")
        
        return wrapped
    return decorator_wrapper