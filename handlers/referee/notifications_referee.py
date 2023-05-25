import asyncio
from datetime import datetime

import decouple

from aiogram import Bot, Dispatcher
from aiogram.utils.exceptions import BotBlocked
from database import referees

bot = Bot(decouple.config('BOT_TOKEN'), parse_mode="HTML")


async def may_22():
    all_tg_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await referees.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"Добрый день, {user_name[0]}! Уже через 8 дней пройдет первый день судейства Чемпионата 2023."
                     "\n\nРасписание:\n<b>Номинация “Редкие волосы”</b> пройдет 29 мая в 10:00 по мск"
                     "\n<b>Судейство номинации “Редкие волосы”</b> пройдет 30 и 31 мая"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\n<b>Номинация “Ровный срез”</b> пройдет 1 июня в 10:00 по мск"
                     "\n<b>Судейство номинации “Ровный срез”</b> пройдет 2 и 3 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\n<b>Номинация “Короткие волосы”</b> пройдет 4 июня в 10:00 по мск"
                     "\n<b>Судейство номинации “Короткие волосы”</b> пройдет 5 и 6 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\nВ дни номинаций вы можете присоединиться к участникам"
                     "\n\n<b>Если у вас нет приложения ZOOM, скачайте по ссылке ниже</b>"
                     "\n\nAndroid - https://play.google.com/store/apps/details?id=us.zoom.videomeetings"
                     "\n\niOS - https://apps.apple.com/ru/app/zoom-one-platform-to-connect/id546505307"
                     "\n\nWindows - https://zoom.us/support/download"
                     "\n\nMac - https://zoom.us/download?os=mac")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def may_26():
    all_tg_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await referees.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"Прекрасного дня, {user_name[0]}! Вы не забыли, что уже через 4 дня пройдет первый день "
                     f"судейства Чемпионата 2023? \nНапоминаем!"
                     "\n\nРасписание:\n<b>Номинация “Редкие волосы”</b> пройдет 29 мая в 10:00 по мск"
                     "\n<b>Судейство номинации “Редкие волосы”</b> пройдет 30 и 31 мая"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\n<b>Номинация “Ровный срез”</b> пройдет 1 июня в 10:00 по мск"
                     "\n<b>Судейство номинации “Ровный срез”</b> пройдет 2 и 3 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\n<b>Номинация “Короткие волосы”</b> пройдет 4 июня в 10:00 по мск"
                     "\n<b>Судейство номинации “Короткие волосы”</b> пройдет 5 и 6 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\nВ дни номинаций вы можете присоединиться к участникам"
                     "\n\n<b>Если у вас нет приложения ZOOM, скачайте по ссылке ниже</b>"
                     "\n\nAndroid - https://play.google.com/store/apps/details?id=us.zoom.videomeetings"
                     "\n\niOS - https://apps.apple.com/ru/app/zoom-one-platform-to-connect/id546505307"
                     "\n\nWindows - https://zoom.us/support/download"
                     "\n\nMac - https://zoom.us/download?os=mac")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def may_28():
    all_tg_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await referees.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"Приветствуем вас, {user_name[0]}! Осталось всего 24 часа до Чемпионата! И 48 часов до судейства!"
                     "\n\nРасписание:\n<b>Номинация “Редкие волосы”</b> пройдет 29 мая в 10:00 по мск"
                     "\n<b>Судейство номинации “Редкие волосы”</b> пройдет 30 и 31 мая"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\n<b>Номинация “Ровный срез”</b> пройдет 1 июня в 10:00 по мск"
                     "\n<b>Судейство номинации “Ровный срез”</b> пройдет 2 и 3 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\n<b>Номинация “Короткие волосы”</b> пройдет 4 июня в 10:00 по мск"
                     "\n<b>Судейство номинации “Короткие волосы”</b> пройдет 5 и 6 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\nВ дни номинаций вы можете присоединиться к участникам"
                     "\n\n<b>Если у вас нет приложения ZOOM, скачайте по ссылке ниже</b>"
                     "\n\nAndroid - https://play.google.com/store/apps/details?id=us.zoom.videomeetings"
                     "\n\niOS - https://apps.apple.com/ru/app/zoom-one-platform-to-connect/id546505307"
                     "\n\nWindows - https://zoom.us/support/download"
                     "\n\nMac - https://zoom.us/download?os=mac")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def may_29():
    all_tg_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await referees.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"<b>{user_name[0]}</b>, сегодня первый день Чемпионата, который пройдет в 10:00 по мск! "
                     "\n<b>Судейство номинации “Редкие волосы”</b> пройдет 30 и 31 мая"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n<b>Судейство номинации “Ровный срез”</b> пройдет 2 и 3 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n<b>Судейство номинации “Короткие волосы”</b> пройдет 5 и 6 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\nВаша ссылка на подключение к конференции ZOOM "
                     "\nhttps://us06web.zoom.us/j/89140506499?pwd=ZjBobUZRckp3ckxtUGMvdWpwaDJJZz09")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def may_30():
    all_tg_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await referees.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"<b>{user_name[0]}</b>, сегодня судейство работ первого дня Чемпионата в номинации "
                     f"“Редкие волосы”!\n\nДля начала судейства нажмите на команду /rate")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def june_1():
    all_tg_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await referees.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"<b>{user_name[0]}</b>, сегодня второй день Чемпионата, который пройдет в 10:00 по мск! "
                     "\n<b>Судейство номинации “Ровный срез”</b> пройдет 2 и 3 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n<b>Судейство номинации “Короткие волосы”</b> пройдет 5 и 6 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\nВаша ссылка на подключение к конференции ZOOM "
                     "\nhttps://us06web.zoom.us/j/89140506499?pwd=ZjBobUZRckp3ckxtUGMvdWpwaDJJZz09")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def june_2():
    all_tg_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await referees.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"<b>{user_name[0]}</b>, сегодня судейство работ второго дня Чемпионата в номинации "
                     f"“Ровный срез”!\n\nДля начала судейства нажмите на команду /rate")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def june_4():
    all_tg_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await referees.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"<b>{user_name[0]}</b>, сегодня третий день Чемпионата, который пройдет в 10:00 по мск! "
                     "\n<b>Судейство номинации “Короткие волосы”</b> пройдет 5 и 6 июня"
                     "\nВремя 10:00-13:00, 14:00-17:00, 17:00-20:00"
                     "\n\nВаша ссылка на подключение к конференции ZOOM "
                     "\nhttps://us06web.zoom.us/j/89140506499?pwd=ZjBobUZRckp3ckxtUGMvdWpwaDJJZz09")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def june_5():
    all_tg_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await referees.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"<b>{user_name[0]}</b>, сегодня судейство работ третьего дня Чемпионата в номинации "
                     f"“Короткие волосы”!\n\nДля начала судейства нажмите на команду /rate")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


# async def task():
#     date = datetime.now()
#     if date.hour == 19:
#         await may_26()
# asyncio.run(task())


def register(dp: Dispatcher):
    pass
