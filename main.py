from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
    CallbackQueryHandler
)
import json
from pathlib import Path

from handlers import (
    START,
    start,
    menu_buttons,
    button_language,
    change_language,
    cancel
)

def load_token_from_config():
    config_path = Path("config/config.json")
    with config_path.open("r") as file:
        config_data = json.load(file)
        return config_data["bot_token"]
    
def main():
    TOKEN = load_token_from_config()
    updater = Updater(TOKEN)
    dp = updater.dispatcher

    start_handler = ConversationHandler(
        entry_points = [CommandHandler('start', start)],
        states = {
            START: [CallbackQueryHandler(button_language, pattern='^(русский|english)$')]
        },
        fallbacks = [CommandHandler('cancel', cancel)]
    )

    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, menu_buttons))
    dp.add_handler(start_handler)
    dp.add_handler(CommandHandler('change_language', change_language))

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()