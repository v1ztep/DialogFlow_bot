import logging
import os
import random

import telegram
import vk_api as vk
from dotenv import load_dotenv
from vk_api.longpoll import VkEventType
from vk_api.longpoll import VkLongPoll

from detect_intent import detect_intent_text

logger = logging.getLogger('VK logger')


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, tg_chat_id):
        super().__init__()
        self.bot = bot
        self.tg_chat_id = tg_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.tg_chat_id, text=log_entry)


def reply(event, vk_api):
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_id = f'vk{event.user_id}'
    text = event.text
    language_code = 'ru-RU'

    intent = detect_intent_text(project_id, session_id, text, language_code)
    if not intent.intent.is_fallback:
        vk_api.messages.send(
            user_id=event.user_id,
            message=intent.fulfillment_text,
            random_id=random.randint(1,1000)
        )


def main():
    load_dotenv()
    vk_token = os.getenv('VK_BOT_TOKEN')
    tg_token = os.getenv('TG_BOT_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    tg_bot = telegram.Bot(token=tg_token)
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(tg_bot, tg_chat_id))
    logger.info('ВК бот запущен')


    vk_session = vk.VkApi(token=vk_token)
    vk_api = vk_session.get_api()

    try:
        longpoll = VkLongPoll(vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                reply(event, vk_api)
    except Exception:
        logger.exception(msg='VK Бот упал с ошибкой:')


if __name__ == '__main__':
    main()
