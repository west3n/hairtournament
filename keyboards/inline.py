from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.callback_data import CallbackData

from database import works

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


async def all_nomination_referee_works(nomination, referee_name, status) -> InlineKeyboardMarkup:
    works_list = works.get_works_by_referee(nomination, referee_name)
    buttons = []
    for work in works_list:
        button = InlineKeyboardButton(text=f'{work[0]}', callback_data=f'{work[0]}')
        buttons.append(button)
    kb = InlineKeyboardMarkup(row_width=5)
    kb.add(*buttons)
    if status == "Комитет по судейству":
        back = InlineKeyboardButton(text='Назад', callback_data='back')
        kb.add(back)
    return kb


def back_button() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Назад', callback_data='back')]
    ])
    return kb


def back_to_work() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Вернуться к выбору номинации', callback_data="back_nominations")],
        [InlineKeyboardButton('Вернуться к выбору работы', callback_data='back_work')]
    ])
    return kb


def grades_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('0', callback_data="0"),
         InlineKeyboardButton('1', callback_data="1"),
         InlineKeyboardButton('2', callback_data="2"),
         InlineKeyboardButton('3', callback_data="3"),
         InlineKeyboardButton('4', callback_data="4"),
         InlineKeyboardButton('5', callback_data="5")],
        [InlineKeyboardButton('Вернуться', callback_data='back_grades')]
    ])
    return kb


def grades10_kb() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('0', callback_data="0"),
         InlineKeyboardButton('1', callback_data="1"),
         InlineKeyboardButton('2', callback_data="2"),
         InlineKeyboardButton('3', callback_data="3"),
         InlineKeyboardButton('4', callback_data="4"),
         InlineKeyboardButton('5', callback_data="5")],
        [InlineKeyboardButton('6', callback_data="6"),
         InlineKeyboardButton('7', callback_data="7"),
         InlineKeyboardButton('8', callback_data="8"),
         InlineKeyboardButton('9', callback_data="9"),
         InlineKeyboardButton('10', callback_data="10")
         ],
        [InlineKeyboardButton('Вернуться', callback_data='back_grades')]
    ])
    return kb


def change_grade() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Изменить оценку', callback_data="change_grade")],
        [InlineKeyboardButton('Перейти к следующему критерию', callback_data='next_grade')]
    ])
    return kb


def change_grade_() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Изменить оценку', callback_data="change_grade")],
        [InlineKeyboardButton('Написать советы, что необходимо улучшить мастеру', callback_data='next_grade')]
    ])
    return kb


def change_grade_2() -> InlineKeyboardMarkup:
    kb = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton('Все верно, отправить баллы на проверку главной судье', callback_data="finish_grade")],
        [InlineKeyboardButton('Исправить оценки', callback_data='change_grade')]
    ])
    return kb