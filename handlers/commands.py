from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards import reply
from handlers.registration import Phone
from database import participants, referees, grades, works


class Hesoyam(StatesGroup):
    text = State()


async def file_id(msg: types.Message):
    if msg.from_id == 15362825:
        if msg.photo:
            await msg.answer(msg.photo[-1].file_id)
        elif msg.video:
            await msg.answer(msg.video.file_id)


async def bot_start(msg: types.Message, state: FSMContext):
    await state.finish()
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
    dp.register_message_handler(file_id, content_types=['photo', 'video'])
    dp.register_message_handler(bot_start, commands='start', state='*')
    dp.register_message_handler(hesoyam, commands='works', state='*')
    dp.register_message_handler(handle_hesoyam, state=Hesoyam.text)
