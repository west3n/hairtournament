import asyncio
from datetime import datetime

import decouple
from aiogram import Dispatcher, types, Bot
from aiogram.utils.exceptions import BotBlocked

from database import users
from keyboards import inline

bot = Bot(decouple.config('BOT_TOKEN'), parse_mode="HTML")


async def fifth_notification():
    all_tg_ids = [tg_id[0] for tg_id in await users.get_all_second_nominations_tg_id()]
    for tg_id in all_tg_ids:
        try:
            video_path = 'media/shooting_instruction.mp4'
            with open(video_path, 'rb') as video:
                session = await bot.get_session()
                user_name = await users.get_name_by_tg_id(tg_id)
                await bot.send_message(
                    chat_id=tg_id,
                    text=f"Приветствуем вас, {user_name[0]}! Осталось 24 часа до второго дня Чемпионата!"
                         "\n\nРасписание:\n<b>Номинация “Ровный срез”</b> пройдет 1 июня в 10:00 по мск"
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


async def sixth_notification():
    all_tg_ids = [tg_id[0] for tg_id in await users.get_all_second_nominations_tg_id()]
    for tg_id in all_tg_ids:
        try:
            session = await bot.get_session()
            user_name = await users.get_name_by_tg_id(tg_id)
            await bot.send_message(
                chat_id=tg_id,
                text=f"<b>{user_name[0]}</b>, сегодня второй день Чемпионата - номинация <b>”Ровный срез”</b>, "
                     f"который пройдет в 10:00 по мск! \n\nУчаствуете ли вы в номинации <b>”Ровный срез”</b>?",
                reply_markup=inline.approve_nomination("Ровный срез"))
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def approve_participation_second_nomination(call: types.CallbackQuery):
    user_name = await users.get_name_by_tg_id(call.from_user.id)
    if call.data == "Ровный срез_yes":
        await call.message.edit_text(f"{user_name[0]}, вы участвуете в номинации <b>“Ровный срез”</b>. "
                                     f"Подтвердите свой выбор, нажав на кнопку ниже",
                                     reply_markup=inline.confirm_nomination("Ровный срез"))
    else:
        await call.message.edit_text(f"Вы отклонили предложение участия в номинации <b>”Ровный срез”!</b>\n"
                                     f"\n\nНоминация <b>“Короткие волосы”</b> пройдет 4 июня в 10:00 по мск")


async def confirm_second_nomination(call: types.CallbackQuery):
    if call.data == "cancel_Ровный срез":
        user_name = await users.get_name_by_tg_id(call.from_user.id)
        await call.message.edit_text(f"<b>{user_name[0]}</b>, сегодня второй день Чемпионата - номинация <b>”Ровный"
                                     f" срез”</b>, "
                                     f"который пройдет в 10:00 по мск! \n\nУчаствуете ли вы в номинации <b>”Ровный"
                                     f" срез”</b>?",
                                     reply_markup=inline.approve_nomination("Ровный срез"))
    else:
        nomination = call.data.split("_")[1]
        await users.add_nomination(call.from_user.id, f"[{nomination}];")
        await call.message.edit_text("Участие подтверждено. Ожидайте инструкцию в 9:30 по мск")

#
# async def task():
#     date = datetime.now()
#     if date.hour == 17:
#         await sixth_notification()
#
#
# asyncio.run(task())


def register(dp: Dispatcher):
    dp.register_callback_query_handler(approve_participation_second_nomination,
                                       lambda c: c.data in ["Ровный срез_yes", "Ровный срез_no"])
    dp.register_callback_query_handler(confirm_second_nomination,
                                       lambda c: c.data in ["cancel_Ровный срез", "gg_Ровный срез"])
