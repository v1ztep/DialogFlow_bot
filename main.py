import logging
import os

import telegram
from dotenv import load_dotenv
from google.cloud import dialogflow
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

logger = logging.getLogger('Telegram logger')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, tg_chat_id):
        super().__init__()
        self.bot = bot
        self.tg_chat_id = tg_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.tg_chat_id, text=log_entry)


def detect_intent_text(project_id, session_id, text, language_code):
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(
        request={"session": session, "query_input": query_input}
    )
    return response.query_result


def start(bot, update):
    update.message.reply_text('Чатбот активирован!')


def reply(bot, update):
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_id = update.message.chat.id
    language_code = 'ru-RU'
    text = update.message.text

    intent = detect_intent_text(project_id, session_id, text, language_code)
    update.message.reply_text(intent.fulfillment_text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    load_dotenv()
    tg_token = os.getenv('TG_BOT_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    tg_bot = telegram.Bot(token=tg_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))
    logger.info('Бот запущен')

    updater = Updater(tg_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text, reply))
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
