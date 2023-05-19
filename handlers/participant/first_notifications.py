import asyncio
from datetime import datetime

import decouple
from aiogram import Dispatcher, types, Bot
from aiogram.utils.exceptions import BotBlocked

from database import participants
from keyboards import inline

bot = Bot(decouple.config('BOT_TOKEN'), parse_mode="HTML")


async def first_notification():
    all_tg_ids = [tg_id[0] for tg_id in await participants.get_all_participants_tg_id()]
    for tg_id in all_tg_ids:
        try:
            video_path = 'media/shooting_instruction.mp4'
            with open(video_path, 'rb') as video:
                session = await bot.get_session()
                user_name = await participants.get_name_by_tg_id(tg_id)
                await bot.send_message(
                    chat_id=tg_id,
                    text=f"Добрый день, {user_name[0]}! Уже через неделю пройдет первый день Чемпионата 2023. Вы готовы?"
                         "\n\nРасписание:\n<b>Номинация “Редкие волосы”</b> пройдет 29 мая в 10:00 по мск"
                         "\n<b>Номинация “Ровный срез”</b> пройдет 1 июня в 10:00 по мск"
                         "\n<b>Номинация “Короткие волосы”</b> пройдет 4 июня в 10:00 по мск"
                         "\n\nВ день Чемпионата зайдите в этот чат-бот <b>с первого устройства</b>, "
                         "с которого будете снимать работу, и одновременно зайдете в конференцию "
                         "ZOOM со <b>второго устройства</b>"
                         "\n\n<b>Если у вас нет приложения ZOOM, скачайте по ссылке ниже</b>"
                         "\n\nAndroid - https://play.google.com/store/apps/details?id=us.zoom.videomeetings"
                         "\n\niOS - https://apps.apple.com/ru/app/zoom-one-platform-to-connect/id546505307"
                         "\n\nWindows - https://zoom.us/support/download"
                         "\n\nMac - https://zoom.us/download?os=mac")
                await bot.send_video(chat_id=tg_id, video=video, caption="Инструкция по общей съемке работы")
                await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def second_notification():
    all_tg_ids = [tg_id[0] for tg_id in await participants.get_all_participants_tg_id()]
    for tg_id in all_tg_ids:
        try:
            video_path = 'media/shooting_instruction.mp4'
            with open(video_path, 'rb') as video:
                session = await bot.get_session()
                user_name = await participants.get_name_by_tg_id(tg_id)
                await bot.send_message(
                    chat_id=tg_id,
                    text=f"Прекрасного дня, {user_name[0]}! Вы не забыли, что уже через 3 дня пройдет первый день "
                         f"Чемпионата 2023? \nНапоминаем!"
                         "\n\nРасписание:\n<b>Номинация “Редкие волосы”</b> пройдет 29 мая в 10:00 по мск"
                         "\n<b>Номинация “Ровный срез”</b> пройдет 1 июня в 10:00 по мск"
                         "\n<b>Номинация “Короткие волосы”</b> пройдет 4 июня в 10:00 по мск"
                         "\n\nВ день Чемпионата зайдите в этот чат-бот <b>с первого устройства</b>, "
                         "с которого будете снимать работу, и одновременно зайдете в конференцию "
                         "ZOOM со <b>второго устройства</b>"
                         "\n\n<b>Если у вас нет приложения ZOOM, скачайте по ссылке ниже</b>"
                         "\n\nAndroid - https://play.google.com/store/apps/details?id=us.zoom.videomeetings"
                         "\n\niOS - https://apps.apple.com/ru/app/zoom-one-platform-to-connect/id546505307"
                         "\n\nWindows - https://zoom.us/support/download"
                         "\n\nMac - https://zoom.us/download?os=mac")
                await bot.send_video(chat_id=tg_id, video=video, caption="Инструкция по общей съемке работы")
                await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def third_notification():
    all_tg_ids = [tg_id[0] for tg_id in await participants.get_all_participants_tg_id()]
    for tg_id in all_tg_ids:
        try:
            video_path = 'media/shooting_instruction.mp4'
            with open(video_path, 'rb') as video:
                session = await bot.get_session()
                user_name = await participants.get_name_by_tg_id(tg_id)
                await bot.send_message(
                    chat_id=tg_id,
                    text=f"Приветствуем вас, {user_name[0]}! Остались считанные часы до первого дня Чемпионата! "
                         f"Буквально через 24 часа вы сможете показать всё своё мастерство и выиграть свой кубок!"
                         "\n\nРасписание:\n<b>Номинация “Редкие волосы”</b> пройдет 29 мая в 10:00 по мск"
                         "\n<b>Номинация “Ровный срез”</b> пройдет 1 июня в 10:00 по мск"
                         "\n<b>Номинация “Короткие волосы”</b> пройдет 4 июня в 10:00 по мск"
                         "\n\nВ день Чемпионата зайдите в этот чат-бот <b>с первого устройства</b>, "
                         "с которого будете снимать работу, и одновременно зайдете в конференцию "
                         "ZOOM со <b>второго устройства</b>"
                         "\n\n<b>Если у вас нет приложения ZOOM, скачайте по ссылке ниже</b>"
                         "\n\nAndroid - https://play.google.com/store/apps/details?id=us.zoom.videomeetings"
                         "\n\niOS - https://apps.apple.com/ru/app/zoom-one-platform-to-connect/id546505307"
                         "\n\nWindows - https://zoom.us/support/download"
                         "\n\nMac - https://zoom.us/download?os=mac")
                await bot.send_video(chat_id=tg_id, video=video, caption="Инструкция по общей съемке работы")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def fourth_notification():
    all_tg_ids = [tg_id[0] for tg_id in await participants.get_all_participants_tg_id()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await participants.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"<b>{user_name[0]}</b>, сегодня первый день Чемпионата - номинация <b>”Редкие волосы”</b>, "
                     f"который пройдет в 10:00 по мск! \n\nУчаствуете ли вы в номинации <b>”Редкие волосы”</b>?",
                reply_markup=inline.approve_nomination("Редкие волосы"))
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def approve_participation_first_nomination(call: types.CallbackQuery):
    user_name = await participants.get_name_by_tg_id(call.from_user.id)
    if call.data == "Редкие волосы_yes":
        await call.message.edit_text(f"{user_name[0]}, вы участвуете в номинации <b>“Редкие волосы”</b>. "
                                     f"Подтвердите свой выбор, нажав на кнопку ниже",
                                     reply_markup=inline.confirm_nomination("Редкие волосы"))
    else:
        await call.message.edit_text(f"Вы отклонили предложение участия в номинации <b>”Редкие волосы”!</b>\n"
                                     f"\nНоминация <b>“Ровный срез”</b> пройдет 1 июня в 10:00 по мск"
                                     f"\n\nНоминация <b>“Короткие волосы”</b> пройдет 4 июня в 10:00 по мск")


async def confirm_first_nomination(call: types.CallbackQuery):
    if call.data == "cancel_Редкие волосы":
        user_name = await participants.get_name_by_tg_id(call.from_user.id)
        await call.message.edit_text(f"<b>{user_name[0]}</b>, сегодня первый день Чемпионата - номинация <b>”Редкие "
                                     f"волосы”</b>, "
                                     f"который пройдет в 10:00 по мск! \n\nУчаствуете ли вы в номинации <b>”Редкие "
                                     f"волосы”</b>?",
                                     reply_markup=inline.approve_nomination("Редкие волосы"))
    else:
        nomination = call.data.split("_")[1]
        await participants.add_nomination(call.from_user.id, f"[{nomination}];")
        await call.message.edit_text("Участие подтверждено. Ожидайте инструкцию в 9:30 по мск")


# async def task():
#     date = datetime.now()
#     if date.hour == 17:
#         await fourth_notification()
#
#
# asyncio.run(task())


def register(dp: Dispatcher):
    dp.register_callback_query_handler(approve_participation_first_nomination,
                                       lambda c: c.data in ["Редкие волосы_yes", "Редкие волосы_no"])
    dp.register_callback_query_handler(confirm_first_nomination,
                                       lambda c: c.data in ["cancel_Редкие волосы", "gg_Редкие волосы"])
