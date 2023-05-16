from aiogram import Dispatcher, types
from keyboards import inline, reply


async def bot_start(msg: types.Message):
    await msg.answer("Доброго времени суток!\nРады, что вы стали частью такого масштабного проекта, как Онлайн "
                     "Чемпионат Наращивания Волос 2023! \nДля удобства проведения судейства и быстрого получения "
                     "результатов, мы создали этот чат-бот. Он поможет вам не упустить ни один из этапов участия в "
                     "Чемпионате.")
    await msg.answer("Введите телефон, который вы указали в анкете при регистрации на Чемпионат"
                     "\n\nИспользуйте формат 79123456789\n\n"
                     "Или просто нажмите на кнопку внизу экрана 'Отправить мой номер телефона'",
                     reply_markup=reply.contact())


def register(dp: Dispatcher):
    dp.register_message_handler(bot_start, commands='start', state='*')
