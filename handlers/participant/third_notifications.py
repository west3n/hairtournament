import asyncio
from datetime import datetime

import decouple
from aiogram import Dispatcher, types, Bot
from aiogram.utils.exceptions import BotBlocked

from database import users
from keyboards import inline

bot = Bot(decouple.config('BOT_TOKEN'), parse_mode="HTML")


async def fifth_notification():
    all_tg_ids = [tg_id[0] for tg_id in await users.get_all_third_nominations_tg_id()]
    for tg_id in all_tg_ids:
        try:
            video_path = 'media/shooting_instruction.mp4'
            with open(video_path, 'rb') as video:
                session = await bot.get_session()
                user_name = await users.get_name_by_tg_id(tg_id)
                await bot.send_message(
                    chat_id=tg_id,
                    text=f"Добрый день, {user_name[0]}! Через 24 часа начнется третий"
                         f"и последний день Чемпионата!\n\n"
                         f"Расписание:\n"
                         f"Номинация <b>“Короткие волосы”</b> пройдет 4 июня в 10:00 по мск"
                         f"\n\nВ день Чемпионата зайдите в этот чат-бот <b>с первого устройства</b>, с которого будете "
                         f"снимать работу, и одновременно зайдете в конференцию ZOOM <b>со второго устройства</b>"
                         f"\n\n<b>Если у вас нет приложения ZOOM, скачайте по ссылке ниже</b>"
                         f"\n\nAndroid - https://play.google.com/store/apps/details?id=us.zoom.videomeetings"
                         f"\n\niOS - https://apps.apple.com/ru/app/zoom-one-platform-to-connect/id546505307"
                         f"\n\nWindows - https://zoom.us/support/download"
                         f"\n\nMac - https://zoom.us/download?os=mac")

                await bot.send_video(chat_id=tg_id, video=video, caption="Инструкция по общей съемке работы")
                await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def sixth_notification():
    all_tg_ids = [tg_id[0] for tg_id in await users.get_all_third_nominations_tg_id()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await users.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"<b>{user_name[0]}</b>, сегодня второй день Чемпионата - номинация <b>”Короткие волосы”</b>, "
                     f"который пройдет в 10:00 по мск! \n\nУчаствуете ли вы в номинации <b>”Короткие волосы”</b>?",
                reply_markup=inline.approve_nomination("Короткие волосы"))
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def approve_participation_second_nomination(call: types.CallbackQuery):
    user_name = await users.get_name_by_tg_id(call.from_user.id)
    if call.data == "Короткие волосы_yes":
        await call.message.edit_text(f"{user_name[0]}, вы участвуете в номинации <b>“Короткие волосы”</b>. "
                                     f"Подтвердите свой выбор, нажав на кнопку ниже",
                                     reply_markup=inline.confirm_nomination("Короткие волосы"))
    else:
        await call.message.edit_text(f"Вы отклонили предложение участия в номинации <b>”Короткие волосы”!</b>\n"
                                     f"\n\nНоминация <b>“Короткие волосы”</b> пройдет 4 июня в 10:00 по мск")


async def confirm_second_nomination(call: types.CallbackQuery):
    if call.data == "cancel_Короткие волосы":
        user_name = await users.get_name_by_tg_id(call.from_user.id)
        await call.message.edit_text(f"<b>{user_name[0]}</b>, сегодня третий день Чемпионата - номинация <b>”Короткие волосы”</b>, "
                                     f"который пройдет в 10:00 по мск! \n\nУчаствуете ли вы в номинации <b>”Короткие волосы”</b>?",
                                     reply_markup=inline.approve_nomination("Короткие волосы"))
    else:
        nomination = call.data.split("_")[1]
        await users.add_nomination(call.from_user.id, f"[{nomination}];")
        await call.message.edit_text("Участие подтверждено. Ожидайте инструкцию в 9:30 по мск")


# async def task():
#     date = datetime.now()
#     if date.hour == 18:
#         await sixth_notification()
#
#
# asyncio.run(task())


def register(dp: Dispatcher):
    dp.register_callback_query_handler(approve_participation_second_nomination,
                                       lambda c: c.data in ["Короткие волосы_yes", "Короткие волосы_no"])
    dp.register_callback_query_handler(confirm_second_nomination,
                                       lambda c: c.data in ["cancel_Короткие волосы", "gg_Короткие волосы"])