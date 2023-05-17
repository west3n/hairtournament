from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton
from keyboards import inline, reply
from database import users


class Phone(StatesGroup):
    phone = State()


class Teachers(StatesGroup):
    teacher = State()
    finish = State()


async def registration_phone(msg: types.Message, state: FSMContext):
    if msg.contact:
        phone_number = msg.contact.phone_number
    else:
        phone_number = msg.text
    if phone_number.startswith("+"):
        phone_number = phone_number.replace("+", "")
    if phone_number.isdigit():
        all_numbers = await users.get_phone_numbers()
        all_numbers_list = [number[0] for number in all_numbers]
        user_data = await users.get_name_by_phone(phone_number)
        if user_data:
            await users.add_tg_id(msg.from_id, phone_number)
            if phone_number in all_numbers_list:
                if user_data[1] == "Champ2023|Econom":
                    await msg.answer(f"<b>{user_data[0]}</b>, вы успешно зарегистрированы! "
                                     f"\n\nВаш тариф участия: Econom"
                                     f"\n\nВ ваш тариф входит участие в 1 номинации.",
                                     reply_markup=reply.kb_remove)
                elif user_data[1] == "Champ2023|Premium":
                    await msg.answer(f"<b>{user_data[0]}</b>, вы успешно зарегистрированы! "
                                     f"\n\nВаш тариф участия: Premium"
                                     f"\n\nВ ваш тариф входит участие в 2 номинациях.",
                                     reply_markup=reply.kb_remove)
                elif user_data[1] == "Champ2023|Vip":
                    await msg.answer(f"<b>{user_data[0]}</b>, вы успешно зарегистрированы! "
                                     f"\n\nВаш тариф участия: Vip"
                                     f"\n\nВ ваш тариф входит участие в 3 номинациях.",
                                     reply_markup=reply.kb_remove)
                await msg.answer("<b>Номинация “Редкие волосы”</b> пройдет 29 мая в 10:00 по мск"
                                 "\n\n<b>Номинация “Ровный срез”</b> пройдет 1 июня в 10:00 по мск "
                                 "\n\n<b>Номинация “Короткие волосы”</b> пройдет 4 июня в 10:00 по мск")
                await msg.answer("Подтвердите, верно ли указаны ваши данные",
                                 reply_markup=inline.yesno_reg())
                await state.finish()
        else:
            await msg.answer("К сожалению, мы не видим ваш номер в списке участников Чемпионата. "
                             "Попробуйте ввести верный номер в формате "
                             "<b>79123456789</b> или свяжитесь с менеджером",
                             reply_markup=inline.wrong_number())
    else:
        await msg.delete()
        await msg.answer("Попробуйте ввести номер в формате <b>79123456789</b>")


async def contact_manager(call: types.CallbackQuery):
    await call.message.edit_text("Ещё раз отправьте свой номер в формате <b>79123456789:</b>")


async def teachers_choice(call: types.CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("Вы успешно зарегистрированы в чат-боте Чемпионата"
                                 "\n\nВыберите, у кого из списка преподавателей вы проходили обучение "
                                 "(можно выбрать несколько вариантов)",
                                 reply_markup=inline.teachers_list())
    await Teachers.teacher.set()


async def teacher_choice(call: types.CallbackQuery, state: FSMContext):
    await call.answer()
    selected_teacher = call.data
    message_id = call.message.message_id
    inline_message_id = call.inline_message_id
    keyboard = call.message.reply_markup
    for row in keyboard.inline_keyboard:
        for button in row:
            if button.callback_data == call.data:
                if "✅" not in button.text:
                    button.text = f"{selected_teacher} ✅"
                    async with state.proxy() as data:
                        selected_teachers = data.get('selected_teachers', [])
                        selected_teachers.append(selected_teacher)
                        await state.update_data(selected_teachers=selected_teachers)
                elif "✅" in button.text:
                    button.text = selected_teachers
                    async with state.proxy() as data:
                        selected_teachers = data.get('selected_teachers', [])
                        selected_teachers.remove(selected_teacher)
                        await state.update_data(selected_teachers=selected_teachers)
    done_button_added = False
    for row in keyboard.inline_keyboard:
        for button in row:
            if button.callback_data == "done":
                done_button_added = True

    if not done_button_added:
        done_button = InlineKeyboardButton("Завершить выбор", callback_data="done")
        keyboard.add(done_button)
    if selected_teacher not in call.message.text:
        await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=message_id,
                                                 inline_message_id=inline_message_id, reply_markup=keyboard)
    else:
        await call.bot.edit_message_reply_markup(chat_id=call.message.chat.id, message_id=message_id,
                                                 inline_message_id=inline_message_id, reply_markup=keyboard)


async def teachers_done(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'none_of_them':
        await users.add_teacher(call.from_user.id, "")
        await call.message.edit_text(
            f"Спасибо, принято, ожидайте начала Чемпионата!")
    else:
        async with state.proxy() as data:
            selected_teachers = data.get('selected_teachers', [])
            await state.update_data(selected_teachers=selected_teachers)
            await state.update_data({'selected_teachers': []})
            async with state.proxy() as data:
                data['teacher'] = selected_teachers
                await users.add_teacher(call.from_user.id, data.get('teacher'))
            await call.message.edit_text(
                f"Спасибо, принято, ожидайте начала Чемпионата!")
            await state.finish()


def register(dp: Dispatcher):
    dp.register_message_handler(registration_phone, content_types=['text', 'contact'], state=Phone.phone)
    dp.register_callback_query_handler(contact_manager, text='send_my_number', state=Phone.phone)
    dp.register_callback_query_handler(teachers_choice, text='yes_reg')
    dp.register_callback_query_handler(teacher_choice, lambda c: c.data in inline.teacher_names,
                                       state=Teachers.teacher)
    dp.register_callback_query_handler(teachers_done, lambda c: c.data in ["done", "none_of_them"],
                                       state=Teachers.teacher)
