from aiogram import Dispatcher, types
from keyboards import inline, reply
from handlers.registration import Phone
from database import participants, referees
from handlers.referee import nomination_referee

async def bot_start(msg: types.Message):
    user = await participants.check_status(msg.from_id)
    referee = await referees.check_status(msg.from_id)
    if user or referee:
        name = user[0] if user else referee[0]
        await msg.answer(f"Доброго времени суток, {name}!\nРады, что вы стали частью такого масштабного проекта, "
                         f"как Онлайн Чемпионат Наращивания Волос 2023! \nДля удобства проведения судейства "
                         f"и быстрого получения результатов, мы создали этот чат-бот. Он поможет вам не упустить"
                         f" ни один из этапов участия в Чемпионате. Вы уже прошли регистрацию, "
                         f"так что ожидайте сообщений от бота.", reply_markup=reply.kb_remove)

    else:
        await msg.answer("Доброго времени суток!\nРады, что вы стали частью такого масштабного проекта, как Онлайн "
                         "Чемпионат Наращивания Волос 2023! \nДля удобства проведения судейства и быстрого получения "
                         "результатов, мы создали этот чат-бот. Он поможет вам не упустить ни один из этапов участия в "
                         "Чемпионате.")
        await msg.answer("Введите телефон, который вы указали в анкете при регистрации на Чемпионат"
                         "\n\nИспользуйте формат 79123456789\n\n"
                         "Или просто нажмите на кнопку внизу экрана 'Отправить мой номер телефона'",
                         reply_markup=reply.contact())
        await Phone.phone.set()


def register(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands='start', state='*')
