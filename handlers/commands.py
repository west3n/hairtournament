import asyncio

import aiogram.utils.exceptions
from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State

from keyboards import reply, inline
from handlers.registration import Phone
from database import participants, referees, grades, works
from handlers import google_sheets


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
                         f"как Онлайн Чемпионат Наращивания Волос 2023!\n\nЧемпионат окончен, чтобы посмотреть "
                         f"результаты, нажмите /results", reply_markup=reply.kb_remove)
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


async def hesoyam(msg: types.Message):
    if msg.from_id in await referees.get_all_head_referees():
        await msg.answer("Введите номер работы:")
        await Hesoyam.text.set()
    else:
        await msg.delete()
        await msg.answer("Команда предназначена только для главных судей!")


async def handle_hesoyam(msg: types.Message, state: FSMContext):
    if msg.text.isdigit():
        async with state.proxy() as data:
            data['text'] = msg.text
        work = await works.get_all_works_by_id(int(data.get('text')))
        referee_name = await referees.get_name_by_tg_id(msg.from_id)
        referees_names_list = [name[0] for name in await referees.get_panel_from_name(referee_name[0])]
        for referee in referees_names_list:
            grades_ = await grades.get_all_grades_by_id_and_referee(int(data.get('text')), referee)
            if grades_:
                await msg.answer(f"{referee}"
                                 f"\n\nНоминация <b>“{work[2]}”</b>\n\nРабота № <b>{int(data.get('text'))}</b>"
                                 f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{grades_[3]}</b>"
                                 f"\n2. Техника капсуляции прядей - Пропитка: <b>{grades_[4]}</b>"
                                 f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                 f"<b> {grades_[5]}</b>"
                                 f"\n4. Соответствие и сложность в номинации: <b>{grades_[6]}</b>"
                                 f"\n5. Внешний вид работы - Форма и структура волос: <b>{grades_[7]}</b>"
                                 f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                 f"<b>{grades_[8]}</b>"
                                 f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                 f"<b>{grades_[9]}</b>"
                                 f"\n8. Внешний вид работы - Общий вид работы: <b> {grades_[10]}</b>"
                                 f"\n9. Внешний вид работы - Расстановка прядей: <b> {grades_[11]}</b>"
                                 f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                 f"{grades_[12]}</b>"
                                 f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                 f"{grades_[13]}</b>"
                                 f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                 f"{grades_[14]}</b>"
                                 f"\n13. Техника наращивания - Безопасность: <b> "
                                 f"{grades_[15]}</b>"
                                 f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                 f"{grades_[16]}</b>"
                                 f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                                 f"{grades_[17]}</b>"
                                 f"\n16. Техника наращивания - Симметрия прядей: <b> "
                                 f"{grades_[18]}</b>"
                                 f"\n17. Техника наращивания - Попадание цвета кератина в тон корней: <b> "
                                 f"{grades_[19]}</b>"
                                 f"\nШтрафной балл: <b>{grades_[20]}</b>"
                                 f"\n\n<b>Рекомендации:</b> {grades_[21]}")
            else:
                await msg.answer(f"{referee} еще не проверяла эту работу!")
        await state.finish()
    else:
        await msg.delete()
        await msg.answer("Введите только цифры работы")


async def handle_results_command(msg: types.Message):
    user = await participants.check_status(msg.from_id)
    await msg.answer(f"{user[0]}, выберите номинацию для выдачи результатов соревнования:",
                     reply_markup=inline.nomination_choice())


async def get_results(call: types.CallbackQuery):
    try:
        await call.message.delete()
    except aiogram.utils.exceptions.MessageToDeleteNotFound:
        pass
    user = await participants.check_status(call.from_user.id)
    nomination = call.data.split('_')[1]
    results = await google_sheets.reading_all_data(user[0], nomination)
    if results:
        for result in results:
            result[24] = 0 if result[24] == '' else result[24]
            text = f"<b>Номинация</b><em>“{nomination}”</em>\n<em>{user[0]}</em>" \
                   f"\n<b>Работа №</b> <em>{result[0]}</em>" \
                   f"\n<b>ВАШЕ МЕСТО В НОМИНАЦИИ:</b> <em>{result[5]}</em>" \
                   f"\n<b>Оценки: </b><em>{result[1]}</em>" \
                   f"\n\n<b>1. Техника капсуляции прядей - Геометрия:</b><em> {result[6]}</em>" \
                   f"\n<b>2. Техника капсуляции прядей - Пропитка:</b><em> {result[7]}</em>" \
                   f"\n<b>3. Техника капсуляции прядей - Равномерность распределения кератина:</b><em> {result[8]}</em>" \
                   f"\n<b>4. Соответствие и сложность в номинации:</b><em> {result[9]}</em>" \
                   f"\n<b>5. Внешний вид работы - Форма и структура волос:</b><em> {result[10]}</em>" \
                   f"\n<b>6. Внешний вид работы - Сложность подбора цвета волос:</b><em> {result[11]}</em>" \
                   f"\n<b>7. Внешний вид работы - Точность попадания в цвет волос:</b><em> {result[12]}</em>" \
                   f"\n<b>8. Внешний вид работы - Общий вид работы:</b><em> {result[13]}</em>" \
                   f"\n<b>9. Внешний вид работы - Расстановка прядей:</b><em> {result[14]}</em>" \
                   f"\n<b>10. Техника наращивания - Герметичность капсулы:</b><em> {result[15]}</em>" \
                   f"\n<b>11. Техника наращивания - Обтекаемость капсулы:</b><em> {result[16]}</em>" \
                   f"\n<b>12. Техника наращивания - Отсутствие затёков:</b><em> {result[17]}</em>" \
                   f"\n<b>13. Техника наращивания - Безопасность:</b><em> {result[18]}</em>" \
                   f"\n<b>14. Техника наращивания - Чистота выбранных рядов и базы:</b><em> {result[19]}</em>" \
                   f"\n<b>15. Техника наращивания - Незаметность капсул в открытом ряду:</b><em> {result[20]}</em>" \
                   f"\n<b>16. Техника наращивания - Симметрия прядей:</b><em> {result[21]}</em>" \
                   f"\n<b>17. Техника наращивания - Попадание цвета кератина в тон корней:</b><em> {result[22]}</em>" \
                   f"\n<b>Штрафной балл:</b><em> {result[23]}</em>" \
                   f"\n<b>Доп. Баллы Комитета по судейству:</b><em> {result[24]}</em>" \
                   f"\n<b>Сумма баллов судьи:</b><em> {result[25]}</em>" \
                   f"\n<b>Средний балл по коллегии:</b><em> {result[26]}</em>" \
                   f"\n\n<b>Рекомендации:</b><em> {result[27]}</em>"
            await call.bot.send_chat_action(call.message.chat.id, 'typing')
            await asyncio.sleep(2)
            await call.message.answer(text)
        await call.message.answer(f"{user[0]}, выберите номинацию для выдачи результатов соревнования:",
                                  reply_markup=inline.nomination_choice())
    else:
        await call.message.answer("Вы не участвовали в данной номинации! Выберете другую:",
                                  reply_markup=inline.nomination_choice())


def register(dp: Dispatcher):
    dp.register_message_handler(file_id, content_types=['photo', 'video'])
    dp.register_message_handler(bot_start, commands='start', state='*')
    dp.register_message_handler(hesoyam, commands='works', state='*')
    dp.register_message_handler(handle_hesoyam, state=Hesoyam.text)
    dp.register_message_handler(handle_results_command, commands='results')
    dp.register_callback_query_handler(get_results, lambda c: c.data.startswith("hh_"))
