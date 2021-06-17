import logging
import os
from functools import partial

import telegram
from dotenv import load_dotenv
from telegram.ext import CommandHandler
from telegram.ext import Filters
from telegram.ext import MessageHandler
from telegram.ext import Updater

from detect_intent import detect_intent_text
from logs_handler import TelegramLogsHandler

logger = logging.getLogger('chatbots logger')


def start(bot, update):
    update.message.reply_text('Чатбот активирован!')


def reply(bot, update, project_id):
    session_id = f'tg{update.message.chat.id}'
    language_code = 'ru-RU'

    intent = detect_intent_text(project_id, session_id, update.message.text,
                                language_code)
    update.message.reply_text(intent.fulfillment_text)


def error(bot, update, error):
    logger.warning('Update "%s" caused error "%s"', update, error)


def main():
    load_dotenv()
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    tg_token = os.getenv('TG_BOT_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    tg_bot = telegram.Bot(token=tg_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))
    logger.info('ТГ бот запущен')

    updater = Updater(tg_token)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(
        MessageHandler(
            Filters.text,
            partial(reply, project_id=project_id)
        )
    )
    dp.add_error_handler(error)
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
