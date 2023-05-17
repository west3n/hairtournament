from aiogram import Dispatcher, types
from database import users
from keyboards import inline


async def first_notification(msg: types.Message):
    user_name = await users.get_name_by_tg_id(msg.from_id)
    await msg.answer(f"Добрый день, {user_name[0]}! Уже через неделю пройдет первый день Чемпионата 2023. Вы готовы?"
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


async def second_notification(msg: types.Message):
    user_name = await users.get_name_by_tg_id(msg.from_id)
    await msg.answer(f"Прекрасного дня, {user_name[0]}! Вы не забыли, что уже через 3 дня пройдет первый день "
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


async def third_notification(msg: types.Message):
    user_name = await users.get_name_by_tg_id(msg.from_id)
    await msg.answer(f" Приветствуем вас, {user_name[0]}! Остались считанные часы до первого дня Чемпионата! "
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


async def fourth_notification(msg: types.Message):
    user_name = await users.get_name_by_tg_id(msg.from_id)
    await msg.answer(f"<b>{user_name[0]}</b>, сегодня первый день Чемпионата - номинация <b>”Редкие волосы”</b>, "
                     f"который пройдет в 10:00 по мск! \n\nУчаствуете ли вы в номинации <b>”Редкие волосы”</b>?",
                     reply_markup=inline.approve_nomination())


async def approve_participation_first_nomination(call: types.CallbackQuery):
    user_name = await users.get_name_by_tg_id(call.from_user.id)
    if call.data == "nomination_yes":
        await call.message.edit_text(f"{user_name[0]}, вы участвуете в номинации <b>“Редкие волосы”</b>. "
                                     f"Подтвердите свой выбор, нажав на кнопку ниже",
                                     reply_markup=inline.confirm_nomination("Редкие волосы"))
    else:
        await call.message.edit_text(f"Вы отклонили предложение участия в номинации <b>”Редкие волосы”!</b>\n"
                                     f"\nНоминация <b>“Ровный срез”</b> пройдет 1 июня в 10:00 по мск"
                                     f"\n\nНоминация <b>“Короткие волосы”</b> пройдет 4 июня в 10:00 по мск")


async def confirm_first_nomination(call: types.CallbackQuery):
    if call.data == "cancel_nomination":
        user_name = await users.get_name_by_tg_id(call.from_user.id)
        await call.message.edit_text(f"<b>{user_name[0]}</b>, сегодня первый день Чемпионата - номинация <b>”Редкие "
                                     f"волосы”</b>, "
                                     f"который пройдет в 10:00 по мск! \n\nУчаствуете ли вы в номинации <b>”Редкие "
                                     f"волосы”</b>?",
                                     reply_markup=inline.approve_nomination())
    else:
        nomination = call.data.split("_")[1]
        await users.add_nomination(call.from_user.id, f"[{nomination}];")
        await call.message.edit_text("Участие подтверждено. Ожидайте инструкцию в 9:30 по мск")


def register(dp: Dispatcher):
    dp.register_message_handler(fourth_notification, commands='hair', state="*")
    dp.register_callback_query_handler(approve_participation_first_nomination,
                                       lambda c: c.data in ["nomination_yes", "nomination_no"])
    dp.register_callback_query_handler(confirm_first_nomination,
                                       lambda c: c.data in ["cancel_nomination"] or c.data.startswith("gg"))
