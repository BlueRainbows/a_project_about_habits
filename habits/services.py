import logging
import requests

from config.settings import TELEGRAM_URL, TELEGRAM_BOT_TOKEN

logger = logging.getLogger(__name__)


def send_telegram_message(telegram_id, message):
    """
    Принимает и отправляет сообщение в телеграм
    """
    params = {'chat_id': telegram_id, 'text': message}
    requests.post(
        TELEGRAM_URL + TELEGRAM_BOT_TOKEN + '/sendMessage',
        params=params
    )


def create_message(habits):
    """
    Формирует сообщение для Telegram, передает параметры
    в функцию send_telegram_message для отправки,
    формирует отчёт о проделанной работе.
    """
    message = ("Когда: " + str(habits.time) + '\n' +
               "Где: " + habits.place + '\n' +
               "Что сделать: " + habits.action)
    send_telegram_message(habits.user.telegram_id, message)
    logger.info(f'Уведомление {message} отправлено')
