import logging


class TelegramLogsHandler(logging.Handler):
    def __init__(self, bot, tg_chat_id):
        super().__init__()
        self.bot = bot
        self.tg_chat_id = tg_chat_id

    def emit(self, record):
        log_entry = self.format(record)
        self.bot.send_message(chat_id=self.tg_chat_id, text=log_entry)