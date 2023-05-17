from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton

kb_remove = ReplyKeyboardRemove()


def contact() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton('Отправить мой номер телефона', request_contact=True)]
    ], resize_keyboard=True, one_time_keyboard=True)
    return kb
