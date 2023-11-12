from telegram.ext import (
    Updater,
    CommandHandler,
    MessageHandler,
    Filters,
    ConversationHandler,
)
import json
from pathlib import Path

from handlers import (
    START,
    start,
    menu_buttons,
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
    entry_points=[CommandHandler('start', start)],
    states={
        START: [MessageHandler(Filters.text & ~Filters.command, menu_buttons)]
    },
    fallbacks=[CommandHandler('cancel', cancel)]
    )

    dp.add_handler(start_handler)

    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()