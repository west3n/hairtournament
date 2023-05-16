from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

teacher_names = [
    'Ольга Лебединская', 'Сандра Лотос', 'Яна Чумаченко', 'Дарья Ерес', 'Яна Волкова', 'Ольга Бычкова',
    'Мария Пугач', 'Юлия Шкода', 'Анна Дубовик', 'Елена Михайлова', 'Мария Гужва', 'Марина Бобылева',
    'Екатерина Малюкина', 'Татьяна Сидорок', 'Анастасия Шумовска', 'Екатерина Осипова', 'Виктория Матвеева',
    'Светлана Зотова', 'Мария Вольт', 'Екатерина Бессараб', 'Алина Краплина', 'Дарья Дмитриева',
    'Наталья Трепалина', 'Алёна Логинова', 'Екатерина Шеина', 'Евгения Максименко',
]


def wrong_number() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Отправить мой номер', callback_data='send_my_number')],
        [InlineKeyboardButton('Связаться с менеджером', url='https://t.me/valeria_tvv')]
    ])
    return kb


def send_number() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Отправить', callback_data='send_number')]
    ])
    return kb


def yesno_reg() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Да,всё верно', callback_data='yes_reg')],
        [InlineKeyboardButton('Нет, есть ошибка', url='https://t.me/valeria_tvv')]
    ])
    return kb


def teachers_list() -> InlineKeyboardMarkup:
    buttons = []
    for teacher_name in teacher_names:
        button_text = teacher_name
        buttons.append(InlineKeyboardButton(button_text, callback_data=button_text))
    kb = InlineKeyboardMarkup(row_width=2)
    kb.add(*buttons)
    none_button = InlineKeyboardButton('Не училась у них', callback_data='none_of_them')
    kb.add(none_button)
    return kb

