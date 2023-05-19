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


def approve_nomination(nomination) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Да, участвую', callback_data=f'{nomination}_yes')],
        [InlineKeyboardButton('Нет, буду сдавать другую номинацию', callback_data=f'{nomination}_no')]
    ])
    return kb


def confirm_nomination(nomination) -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Подтвердить', callback_data=f"gg_{nomination}")],
        [InlineKeyboardButton('Исправить ошибку', callback_data=f'cancel_{nomination}')]
    ])
    return kb


def confirm_angle_photo() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Перейти к следующему ракурсу', callback_data=f"next_angle")],
        [InlineKeyboardButton('Заменить фото по этому ракурсу', callback_data='resend_photo')]
    ])
    return kb


def confirm_angle_video() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Перейти к следующему ракурсу', callback_data=f"next_angle")],
        [InlineKeyboardButton('Заменить видео по этому ракурсу', callback_data='resend_video')]
    ])
    return kb


def confirm_angle_finish() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Завершить сдачу работы в номинации', callback_data=f"finish_nominations")],
        [InlineKeyboardButton('Заменить фото по этому ракурсу', callback_data='resend_photo')]
    ])
    return kb


def nomination_choice() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Редкие волосы', callback_data=f"hh_Редкие волосы")],
        [InlineKeyboardButton('Ровный срез', callback_data=f'hh_Ровный срез')],
        [InlineKeyboardButton('Короткие волосы', callback_data='hh_Короткие волосы')]
    ])
    return kb
