import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database import referees, works, grades, participants
from keyboards import inline
from handlers import google_sheets


class Grades(StatesGroup):
    work = State()
    grades1 = State()
    grades2 = State()
    grades3 = State()
    grades3_1 = State()
    grades4 = State()
    grades4_1 = State()
    grades5 = State()
    grades5_1 = State()
    grades6 = State()
    grades6_1 = State()
    grades7 = State()
    grades7_1 = State()
    grades8 = State()
    grades8_1 = State()
    grades9 = State()
    grades9_1 = State()
    grades10 = State()
    grades10_1 = State()
    grades11 = State()
    grades11_1 = State()
    grades12 = State()
    grades12_1 = State()
    grades13 = State()
    grades13_1 = State()
    grades14 = State()
    grades14_1 = State()
    grades15 = State()
    grades15_1 = State()
    grades16 = State()
    grades16_1 = State()
    grades17 = State()
    grades17_1 = State()
    penalty = State()
    penalty_ = State()
    advice = State()
    advice_ = State()
    advice_2 = State()
    finish = State()
    all_grades = State()
    change_grade = State()
    last_state = State()
    back_state = State()
    check = State()


async def get_media_list(work):
    media = {}
    for i in range(5, 13):
        media[f'photo{i - 4}'] = types.InputMediaPhoto(work[i])
    for i in range(13, 22):
        media[f'video{i - 12}'] = types.InputMediaVideo(work[i])
    return media


async def select_work(msg: types.Message):
    all_referee_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    if msg.from_id in all_referee_ids:
        status = await referees.get_name_by_tg_id(msg.from_id)
        if status[1] != "Комитет по судейству":
            if datetime.datetime.now().date().strftime("%Y-%m-%d") in ["2023-05-29", "2023-05-31"]:
                nomination = "Редкие волосы"
            elif datetime.datetime.now().date().strftime("%Y-%m-%d") in ["2023-05-30", "2023-05-27"]:
                nomination = "Ровный срез"
            elif datetime.datetime.now().date().strftime("%Y-%m-%d") in ["2023-06-05", "2023-06-16"]:
                nomination = "Короткие волосы"
            else:
                nomination = None
                await msg.answer("Сегодня нет судейств!")
            referee_name = await referees.get_name_by_tg_id(msg.from_user.id)
            works_list = works.get_works_by_referee(nomination, referee_name[0])
            if nomination:
                if works_list:
                    await msg.answer(f"Номинация: {nomination}\n\nВыберите номер работы:",
                                     reply_markup=await inline.all_nomination_referee_works(nomination, status[0],
                                                                                            status[1]))
                    await Grades.work.set()
                else:
                    await msg.answer(f"Номинация <b>“{nomination}“</b>\n\nРабот для судейства нет.")
            else:
                pass
        else:
            await msg.answer("Выберите номинацию, в которой хотите проверить работу",
                             reply_markup=inline.nomination_choice())
    else:
        await msg.answer("Эта команда предназначена только для судей!")


async def hh_nomination(call: types.CallbackQuery):
    referee_name = await referees.get_name_by_tg_id(call.from_user.id)
    nomination = call.data.split("_")[1]
    works_list = works.get_works_by_referee(nomination, referee_name[0])
    status = await referees.get_name_by_tg_id(call.from_user.id)
    if works_list:
        await call.message.edit_text(f"Номинация: “{nomination}“\n\nВыберите номер работы:",
                                     reply_markup=await inline.all_nomination_referee_works(
                                         nomination, referee_name[0], status[1]))
        await Grades.work.set()
    else:
        await call.message.edit_text(f"Номинация '{nomination}' еще не началась!",
                                     reply_markup=inline.back_button())
        await Grades.work.set()


async def first_grade(call: types.CallbackQuery, state: FSMContext):
    status = await referees.get_name_by_tg_id(call.from_user.id)
    if call.data == 'back' and status[1] == "Комитет по судейству":
        await state.finish()
        await call.message.edit_text("Выберите номинацию, в которой хотите проверить работу",
                                     reply_markup=inline.nomination_choice())
    else:
        async with state.proxy() as data:
            data['work'] = int(call.data)
        status = await referees.get_name_by_tg_id(call.from_user.id)
        work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        if status[1] in ["Судья", 'Главная судья']:
            media_list = [media['photo3'], media['video3']]
            await call.message.delete()
            await call.message.answer_media_group(media=media_list)
            await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота <b>№ {data.get('work')}</b>"
                                      "\n\nКритерий: техника капсуляции прядей.\nОцените <b>геометрию</b>",
                                      reply_markup=inline.grades_kb())
            await Grades.next()
        elif status[1] == "Комитет по судейству":
            first_list = [media['video3'], media['photo3'],
                          media['video1'], media['photo1'],
                          media['video2'], media['photo2'],
                          media['video6'], media['photo7']]
            second_list = [media['video7'], media['photo8'], media['video8'], media['video5'], media['video9'],
                           media['video4'], media['photo4'], media['photo6'], media['photo5']]
            await call.message.delete()
            await call.message.answer_media_group(media=first_list)
            await call.message.answer_media_group(media=second_list)
            await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота <b>№ {data.get('work')}</b>",
                                      reply_markup=inline.back_to_work())
            await state.set_state(Grades.back_state.state)


async def back_button_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'back_nominations':
        await state.finish()
        await call.message.edit_text("Выберите номинацию, в которой хотите проверить работу",
                                     reply_markup=inline.nomination_choice())
    if call.data == 'back_work':
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        await state.finish()
        call.data = f'hh_{work[2]}'
        await hh_nomination(call)


async def first_grade_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        await state.finish()
        status = await referees.get_name_by_tg_id(call.from_user.id)
        if datetime.datetime.now().date().strftime("%Y-%m-%d") in ["2023-05-21", "2023-05-24"]:
            nomination = "Редкие волосы"
        elif datetime.datetime.now().date().strftime("%Y-%m-%d") in ["2023-05-23", "2023-06-03"]:
            nomination = "Ровный срез"
        elif datetime.datetime.now().date().strftime("%Y-%m-%d") in ["2023-06-05", "2023-06-16"]:
            nomination = "Короткие волосы"
        else:
            nomination = None
            print(True)
            await call.message.edit_text("Сегодня нет судейств")
        if nomination:
            await call.message.edit_text(f"Номинация: “{nomination}“\n\nВыберите номер работы:",
                                         reply_markup=await inline.all_nomination_referee_works(nomination, status[0],
                                                                                                status[1]))
            await Grades.work.set()
    else:
        async with state.proxy() as data:
            data['grades1'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def second_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['photo3'], media['video3']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n\nКритерий: техника капсуляции прядей.\nОцените <b>пропитку</b>",
                                  reply_markup=inline.grades_kb())
        await Grades.next()
    else:
        await state.set_state(Grades.work.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота <b>№ {data.get('work')}</b>"
                                     "\n\nКритерий: техника капсуляции прядей.\nОцените <b>геометрию</b>",
                                     reply_markup=inline.grades_kb())
        await Grades.next()


async def second_grade_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота <b>№ {data.get('work')}</b>"
                                     "\n\nКритерий: техника капсуляции прядей.\nОцените <b>геометрию</b>",
                                     reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades1.state)
    else:
        async with state.proxy() as data:
            data['grades2'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def third_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['photo3'], media['video3']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  "\n\nКритерий: техника капсуляции прядей."
                                  "\nОцените <b>равномерность распределения кератина</b>",
                                  reply_markup=inline.grades_kb())
        await Grades.next()
    else:
        await state.set_state(Grades.grades2.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                         f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                         f"\n\nКритерий: техника капсуляции прядей.\nОцените <b>пропитку</b>",
                                         reply_markup=inline.grades_kb())
            await Grades.next()


async def third_grade_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n\nКритерий: техника капсуляции прядей.\nОцените <b>пропитку</b>",
                                     reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades3.state)
    else:
        async with state.proxy() as data:
            data['grades3'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>",
                                     reply_markup=inline.change_grade())

        await Grades.next()


async def fourth_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video1'], media['photo1'],
                      media['video2'], media['photo2']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\nОцените <b>соответствие и сложность в номинации</b>",
                                  reply_markup=inline.grades10_kb())
        await Grades.next()
    else:
        await state.set_state(Grades.grades3_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                         f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                         f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                         f"\nОцените <b>равномерность распределения кератина</b>",
                                         reply_markup=inline.grades_kb())
            await Grades.next()


async def fourth_grade_handler(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['photo3'], media['video3']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\nОцените <b>равномерность распределения кератина</b>",
                                  reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades4.state)
    else:
        async with state.proxy() as data:
            data['grades4'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>",
                                     reply_markup=inline.change_grade())

        await Grades.next()


async def fifth_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video6'], media['video7'],
                      media['photo7'], media['video8'], media['photo8']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n\nКритерий: внешний вид работы"
                                  f"\nОцените <b>форму и структуру волос</b>",
                                  reply_markup=inline.grades_kb())

        await Grades.next()
    else:
        await state.set_state(Grades.grades4_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                         f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                         f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                         f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                         f"<b> {data.get('grades3')}</b>"
                                         f"\nОцените <b>соответствие и сложность в номинации</b>",
                                         reply_markup=inline.grades10_kb())

            await Grades.next()


async def fifth_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video1'], media['photo1'],
                      media['video2'], media['photo2']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\nОцените <b>соответствие и сложность в номинации</b>",
                                  reply_markup=inline.grades10_kb())
        await state.set_state(Grades.grades5.state)
    else:
        async with state.proxy() as data:
            data['grades5'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>",
                                     reply_markup=inline.change_grade())

        await Grades.next()


async def sixth_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video6'], media['video7'],
                      media['photo7'], media['video8'], media['photo8']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n\nКритерий: внешний вид работы"
                                  f"\nОцените <b>сложность подбора цвета волос</b>",
                                  reply_markup=inline.grades_kb())

        await Grades.next()
    else:
        await state.set_state(Grades.grades5_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                         f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                         f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                         f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                         f"<b> {data.get('grades3')}</b>"
                                         f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                         f"\n\nКритерий: внешний вид работы"
                                         f"\nОцените <b>форму и структуру волос</b>",
                                         reply_markup=inline.grades_kb())

            await Grades.next()


async def sixth_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video6'], media['video7'],
                      media['photo7'], media['video8'], media['photo8']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n\nКритерий: внешний вид работы"
                                  f"\nОцените <b>форму и структуру волос</b>",
                                  reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades6.state)
    else:
        async with state.proxy() as data:
            data['grades6'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def seven_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video6'], media['video7'],
                      media['photo7'], media['video8'], media['photo8']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n\nКритерий: внешний вид работы"
                                  f"\nОцените <b>точность попадания в цвет волос</b>",
                                  reply_markup=inline.grades_kb())

        await Grades.next()
    else:
        await state.set_state(Grades.grades6_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                         f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                         f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                         f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                         f"<b> {data.get('grades3')}</b>"
                                         f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                         f"\n5. Внешний вид работы - Форма и структура волос:"
                                         f" <b>{data.get('grades5')}</b>"
                                         f"\n\nКритерий: внешний вид работы"
                                         f"\nОцените <b>сложность подбора цвета волос</b>",
                                         reply_markup=inline.grades_kb())

            await Grades.next()


async def seven_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video6'], media['video7'],
                      media['photo7'], media['video8'], media['photo8']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос:"
            f" <b>{data.get('grades5')}</b>"
            f"\n\nКритерий: внешний вид работы"
            f"\nОцените <b>сложность подбора цвета волос</b>",
            reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades7.state)
    else:
        async with state.proxy() as data:
            data['grades7'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def eighth_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video6'], media['video7'],
                      media['photo7'], media['video8'], media['photo8']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n\nКритерий: внешний вид работы"
                                  f"\nОцените <b>общий вид работы</b>",
                                  reply_markup=inline.grades10_kb())

        await Grades.next()
    else:
        await state.set_state(Grades.grades7_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                         f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                         f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                         f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                         f"<b> {data.get('grades3')}</b>"
                                         f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                         f"\n5. Внешний вид работы - Форма и структура волос:"
                                         f" <b>{data.get('grades5')}</b>"
                                         f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                         f"<b>{data.get('grades6')}</b>"
                                         f"\n\nКритерий: внешний вид работы"
                                         f"\nОцените <b>точность попадания в цвет волос</b>",
                                         reply_markup=inline.grades_kb())

            await Grades.next()


async def eight_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video6'], media['video7'],
                      media['photo7'], media['video8'], media['photo8']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос:"
            f" <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n\nКритерий: внешний вид работы"
            f"\nОцените <b>точность попадания в цвет волос</b>",
            reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades8.state)
    else:
        async with state.proxy() as data:
            data['grades8'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def ninth_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video9']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                  f"\n\nКритерий: внешний вид работы"
                                  f"\nОцените <b>расстановку прядей</b>",
                                  reply_markup=inline.grades_kb())

        await Grades.next()
    else:
        await state.set_state(Grades.grades8_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                         f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                         f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                         f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                         f"<b> {data.get('grades3')}</b>"
                                         f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                         f"\n5. Внешний вид работы - Форма и структура волос: "
                                         f"<b>{data.get('grades5')}</b>"
                                         f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                         f"<b>{data.get('grades6')}</b>"
                                         f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                         f"<b>{data.get('grades7')}</b>"
                                         f"\n\nКритерий: внешний вид работы"
                                         f"\nОцените <b>общий вид работы</b>",
                                         reply_markup=inline.grades10_kb())

            await Grades.next()


async def ninth_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video6'], media['video7'],
                      media['photo7'], media['video8'], media['photo8']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
            f"<b>{data.get('grades7')}</b>"
            f"\n\nКритерий: внешний вид работы"
            f"\nОцените <b>общий вид работы</b>",
            reply_markup=inline.grades10_kb())
        await state.set_state(Grades.grades9.state)
    else:
        async with state.proxy() as data:
            data['grades9'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def ten_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video4'], media['photo4']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                  f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                  f"\n\nКритерий: техника наращивания"
                                  f"\nОцените <b>герметичность капсулы</b>",
                                  reply_markup=inline.grades_kb())
        await Grades.next()
    else:
        await state.set_state(Grades.grades9_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(
                f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                f"<b> {data.get('grades3')}</b>"
                f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                f"<b>{data.get('grades6')}</b>"
                f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                f"<b>{data.get('grades7')}</b>"
                f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                f"\n\nКритерий: внешний вид работы"
                f"\nОцените <b>расстановку прядей</b>",
                reply_markup=inline.grades_kb())

            await Grades.next()


async def ten_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video9']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
            f"<b>{data.get('grades7')}</b>"
            f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
            f"\n\nКритерий: внешний вид работы"
            f"\nОцените <b>расстановку прядей</b>",
            reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades10.state)
    else:
        async with state.proxy() as data:
            data['grades10'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                     f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                     f"{data.get('grades10')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def eleven_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video4'], media['photo4']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                  f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                  f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                  f"{data.get('grades10')}</b>"
                                  f"\n\nКритерий: техника наращивания"
                                  f"\nОцените <b>обтекаемость капсулы</b>",
                                  reply_markup=inline.grades_kb())

        await Grades.next()
    else:
        await state.set_state(Grades.grades10_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(
                f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                f"<b> {data.get('grades3')}</b>"
                f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                f"<b>{data.get('grades6')}</b>"
                f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                f"<b>{data.get('grades7')}</b>"
                f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                f"\n\nКритерий: техника наращивания"
                f"\nОцените <b>герметичность капсулы</b>",
                reply_markup=inline.grades_kb())

            await Grades.next()


async def eleven_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video4'], media['photo4']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
            f"<b>{data.get('grades7')}</b>"
            f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
            f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
            f"\n\nКритерий: техника наращивания"
            f"\nОцените <b>герметичность капсулы</b>",
            reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades11.state)
    else:
        async with state.proxy() as data:
            data['grades11'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                     f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                     f"{data.get('grades10')}</b>"
                                     f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                     f"{data.get('grades11')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def twelve_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video4'], media['photo4']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                  f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                  f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                  f"{data.get('grades10')}</b>"
                                  f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                  f"{data.get('grades11')}</b>"
                                  f"\n\nКритерий: техника наращивания"
                                  f"\nОцените <b>отсутствие затёков</b>",
                                  reply_markup=inline.grades_kb())

        await Grades.next()
    else:
        await state.set_state(Grades.grades11_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(
                f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                f"<b> {data.get('grades3')}</b>"
                f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                f"<b>{data.get('grades6')}</b>"
                f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                f"<b>{data.get('grades7')}</b>"
                f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                f"{data.get('grades10')}</b>"
                f"\n\nКритерий: техника наращивания"
                f"\nОцените <b>обтекаемость капсулы</b>",
                reply_markup=inline.grades_kb())

            await Grades.next()


async def twelve_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video4'], media['photo4']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
            f"<b>{data.get('grades7')}</b>"
            f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
            f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
            f"\n10. Техника наращивания - Герметичность капсулы: <b> "
            f"{data.get('grades10')}</b>"
            f"\n\nКритерий: техника наращивания"
            f"\nОцените <b>обтекаемость капсулы</b>",
            reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades12.state)
    else:
        async with state.proxy() as data:
            data['grades12'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                     f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                     f"{data.get('grades10')}</b>"
                                     f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                     f"{data.get('grades11')}</b>"
                                     f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                     f"{data.get('grades12')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def thirteen_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video4'], media['photo4']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                  f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                  f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                  f"{data.get('grades10')}</b>"
                                  f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                  f"{data.get('grades11')}</b>"
                                  f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                  f"{data.get('grades12')}</b>"
                                  f"\n\nКритерий: техника наращивания"
                                  f"\nОцените <b>безопасность</b>",
                                  reply_markup=inline.grades_kb())

        await Grades.next()
    else:
        await state.set_state(Grades.grades12_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(
                f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                f"<b> {data.get('grades3')}</b>"
                f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                f"<b>{data.get('grades6')}</b>"
                f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                f"<b>{data.get('grades7')}</b>"
                f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                f"{data.get('grades10')}</b>"
                f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                f"{data.get('grades11')}</b>"
                f"\n\nКритерий: техника наращивания"
                f"\nОцените <b>отсутствие затёков</b>",
                reply_markup=inline.grades_kb())

            await Grades.next()


async def thirteen_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video4'], media['photo4']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
            f"<b>{data.get('grades7')}</b>"
            f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
            f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
            f"\n10. Техника наращивания - Герметичность капсулы: <b> "
            f"{data.get('grades10')}</b>"
            f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
            f"{data.get('grades11')}</b>"
            f"\n\nКритерий: техника наращивания"
            f"\nОцените <b>отсутствие затёков</b>",
            reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades13.state)
    else:
        async with state.proxy() as data:
            data['grades13'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                     f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                     f"{data.get('grades10')}</b>"
                                     f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                     f"{data.get('grades11')}</b>"
                                     f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                     f"{data.get('grades12')}</b>"
                                     f"\n13. Техника наращивания - Безопасность: <b> "
                                     f"{data.get('grades13')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def fourteen_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video5'], media['photo5'], media['photo6']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                  f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                  f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                  f"{data.get('grades10')}</b>"
                                  f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                  f"{data.get('grades11')}</b>"
                                  f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                  f"{data.get('grades12')}</b>"
                                  f"\n13. Техника наращивания - Безопасность: <b> "
                                  f"{data.get('grades13')}</b>"
                                  f"\n\nКритерий: техника наращивания"
                                  f"\nОцените <b>чистоту выбранных рядов и базы</b>",
                                  reply_markup=inline.grades_kb())

        await Grades.next()
    else:
        await state.set_state(Grades.grades13_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(
                f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                f"<b> {data.get('grades3')}</b>"
                f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                f"<b>{data.get('grades6')}</b>"
                f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                f"<b>{data.get('grades7')}</b>"
                f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                f"{data.get('grades10')}</b>"
                f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                f"{data.get('grades11')}</b>"
                f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                f"{data.get('grades12')}</b>"
                f"\n\nКритерий: техника наращивания"
                f"\nОцените <b>безопасность</b>",
                reply_markup=inline.grades_kb())

            await Grades.next()


async def fourteen_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video4'], media['photo4']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
            f"<b>{data.get('grades7')}</b>"
            f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
            f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
            f"\n10. Техника наращивания - Герметичность капсулы: <b> "
            f"{data.get('grades10')}</b>"
            f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
            f"{data.get('grades11')}</b>"
            f"\n12. Техника наращивания - Отсутствие затёков: <b> "
            f"{data.get('grades12')}</b>"
            f"\n\nКритерий: техника наращивания"
            f"\nОцените <b>безопасность</b>",
            reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades14.state)
    else:
        async with state.proxy() as data:
            data['grades14'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                     f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                     f"{data.get('grades10')}</b>"
                                     f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                     f"{data.get('grades11')}</b>"
                                     f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                     f"{data.get('grades12')}</b>"
                                     f"\n13. Техника наращивания - Безопасность: <b> "
                                     f"{data.get('grades13')}</b>"
                                     f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                     f"{data.get('grades14')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def fifteen_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video5'], media['photo5'], media['photo6']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                  f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                  f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                  f"{data.get('grades10')}</b>"
                                  f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                  f"{data.get('grades11')}</b>"
                                  f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                  f"{data.get('grades12')}</b>"
                                  f"\n13. Техника наращивания - Безопасность: <b> "
                                  f"{data.get('grades13')}</b>"
                                  f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                  f"{data.get('grades14')}</b>"
                                  f"\n\nКритерий: техника наращивания"
                                  f"\nОцените <b>незаметность капсул в открытом ряду</b>",
                                  reply_markup=inline.grades10_kb())

        await Grades.next()
    else:
        await state.set_state(Grades.grades14_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(
                f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                f"<b> {data.get('grades3')}</b>"
                f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                f"<b>{data.get('grades6')}</b>"
                f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                f"<b>{data.get('grades7')}</b>"
                f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                f"{data.get('grades10')}</b>"
                f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                f"{data.get('grades11')}</b>"
                f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                f"{data.get('grades12')}</b>"
                f"\n13. Техника наращивания - Безопасность: <b> "
                f"{data.get('grades13')}</b>"
                f"\n\nКритерий: техника наращивания"
                f"\nОцените <b>чистоту выбранных рядов и базы</b>",
                reply_markup=inline.grades_kb())
            await Grades.next()


async def fifteen_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video5'], media['photo5'], media['photo6']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
            f"<b>{data.get('grades7')}</b>"
            f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
            f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
            f"\n10. Техника наращивания - Герметичность капсулы: <b> "
            f"{data.get('grades10')}</b>"
            f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
            f"{data.get('grades11')}</b>"
            f"\n12. Техника наращивания - Отсутствие затёков: <b> "
            f"{data.get('grades12')}</b>"
            f"\n13. Техника наращивания - Безопасность: <b> "
            f"{data.get('grades13')}</b>"
            f"\n\nКритерий: техника наращивания"
            f"\nОцените <b>чистоту выбранных рядов и базы</b>",
            reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades14.state)
    else:
        async with state.proxy() as data:
            data['grades15'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                     f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                     f"{data.get('grades10')}</b>"
                                     f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                     f"{data.get('grades11')}</b>"
                                     f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                     f"{data.get('grades12')}</b>"
                                     f"\n13. Техника наращивания - Безопасность: <b> "
                                     f"{data.get('grades13')}</b>"
                                     f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                     f"{data.get('grades14')}</b>"
                                     f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                                     f"{data.get('grades15')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def sixteen_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video5'], media['photo5'], media['photo6']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                  f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                  f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                  f"{data.get('grades10')}</b>"
                                  f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                  f"{data.get('grades11')}</b>"
                                  f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                  f"{data.get('grades12')}</b>"
                                  f"\n13. Техника наращивания - Безопасность: <b> "
                                  f"{data.get('grades13')}</b>"
                                  f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                  f"{data.get('grades14')}</b>"
                                  f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                                  f"{data.get('grades15')}</b>"
                                  f"\n\nКритерий: техника наращивания"
                                  f"\nОцените <b>симметрию прядей</b>",
                                  reply_markup=inline.grades_kb())
        await Grades.next()
    else:
        await state.set_state(Grades.grades15_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(
                f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                f"<b> {data.get('grades3')}</b>"
                f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                f"<b>{data.get('grades6')}</b>"
                f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                f"<b>{data.get('grades7')}</b>"
                f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                f"{data.get('grades10')}</b>"
                f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                f"{data.get('grades11')}</b>"
                f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                f"{data.get('grades12')}</b>"
                f"\n13. Техника наращивания - Безопасность: <b> "
                f"{data.get('grades13')}</b>"
                f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                f"{data.get('grades14')}</b>"
                f"\n\nКритерий: техника наращивания"
                f"\nОцените <b>незаметность капсул в открытом ряду</b>",
                reply_markup=inline.grades10_kb())
            await Grades.next()


async def sixteen_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video5'], media['photo5'], media['photo6']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
            f"<b>{data.get('grades7')}</b>"
            f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
            f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
            f"\n10. Техника наращивания - Герметичность капсулы: <b> "
            f"{data.get('grades10')}</b>"
            f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
            f"{data.get('grades11')}</b>"
            f"\n12. Техника наращивания - Отсутствие затёков: <b> "
            f"{data.get('grades12')}</b>"
            f"\n13. Техника наращивания - Безопасность: <b> "
            f"{data.get('grades13')}</b>"
            f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
            f"{data.get('grades14')}</b>"
            f"\n\nКритерий: техника наращивания"
            f"\nОцените <b>незаметность капсул в открытом ряду</b>",
            reply_markup=inline.grades10_kb())
        await state.set_state(Grades.grades15.state)
    else:
        async with state.proxy() as data:
            data['grades16'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                     f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                     f"{data.get('grades10')}</b>"
                                     f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                     f"{data.get('grades11')}</b>"
                                     f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                     f"{data.get('grades12')}</b>"
                                     f"\n13. Техника наращивания - Безопасность: <b> "
                                     f"{data.get('grades13')}</b>"
                                     f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                     f"{data.get('grades14')}</b>"
                                     f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                                     f"{data.get('grades15')}</b>"
                                     f"\n16. Техника наращивания - Симметрия прядей: <b> "
                                     f"{data.get('grades16')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def seventeen_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video5'], media['photo5'], media['photo6']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                  f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                  f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                  f"{data.get('grades10')}</b>"
                                  f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                  f"{data.get('grades11')}</b>"
                                  f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                  f"{data.get('grades12')}</b>"
                                  f"\n13. Техника наращивания - Безопасность: <b> "
                                  f"{data.get('grades13')}</b>"
                                  f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                  f"{data.get('grades14')}</b>"
                                  f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                                  f"{data.get('grades15')}</b>"
                                  f"\n16. Техника наращивания - Симметрия прядей: <b> "
                                  f"{data.get('grades16')}</b>"
                                  f"\n\nКритерий: техника наращивания"
                                  f"\nОцените <b>попадание цвета кератина в тон корней</b>",
                                  reply_markup=inline.grades_kb())
        await Grades.next()
    else:
        await state.set_state(Grades.grades16_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(
                f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                f"<b> {data.get('grades3')}</b>"
                f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                f"<b>{data.get('grades6')}</b>"
                f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                f"<b>{data.get('grades7')}</b>"
                f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                f"{data.get('grades10')}</b>"
                f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                f"{data.get('grades11')}</b>"
                f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                f"{data.get('grades12')}</b>"
                f"\n13. Техника наращивания - Безопасность: <b> "
                f"{data.get('grades13')}</b>"
                f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                f"{data.get('grades14')}</b>"
                f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                f"{data.get('grades15')}</b>"
                f"\n\nКритерий: техника наращивания"
                f"\nОцените <b>симметрию прядей</b>",
                reply_markup=inline.grades_kb())
            await Grades.next()


async def seventeen_grade_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video5'], media['photo5'], media['photo6']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
            f"<b>{data.get('grades7')}</b>"
            f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
            f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
            f"\n10. Техника наращивания - Герметичность капсулы: <b> "
            f"{data.get('grades10')}</b>"
            f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
            f"{data.get('grades11')}</b>"
            f"\n12. Техника наращивания - Отсутствие затёков: <b> "
            f"{data.get('grades12')}</b>"
            f"\n13. Техника наращивания - Безопасность: <b> "
            f"{data.get('grades13')}</b>"
            f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
            f"{data.get('grades14')}</b>"
            f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
            f"{data.get('grades15')}</b>"
            f"\n\nКритерий: техника наращивания"
            f"\nОцените <b>симметрию прядей</b>",
            reply_markup=inline.grades_kb())
        await state.set_state(Grades.grades16.state)
    else:
        async with state.proxy() as data:
            data['grades17'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                     f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                     f"{data.get('grades10')}</b>"
                                     f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                     f"{data.get('grades11')}</b>"
                                     f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                     f"{data.get('grades12')}</b>"
                                     f"\n13. Техника наращивания - Безопасность: <b> "
                                     f"{data.get('grades13')}</b>"
                                     f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                     f"{data.get('grades14')}</b>"
                                     f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                                     f"{data.get('grades15')}</b>"
                                     f"\n16. Техника наращивания - Симметрия прядей: <b> "
                                     f"{data.get('grades16')}</b>"
                                     f"\n17. Техника наращивания - Попадание цвета кератина в тон корней: <b> "
                                     f"{data.get('grades17')}</b>",
                                     reply_markup=inline.change_grade())
        await Grades.next()


async def penalty_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_reply_markup()
        await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                  f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                  f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                  f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                  f"<b> {data.get('grades3')}</b>"
                                  f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                  f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                  f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                  f"<b>{data.get('grades6')}</b>"
                                  f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                  f"<b>{data.get('grades7')}</b>"
                                  f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                  f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                  f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                  f"{data.get('grades10')}</b>"
                                  f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                  f"{data.get('grades11')}</b>"
                                  f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                  f"{data.get('grades12')}</b>"
                                  f"\n13. Техника наращивания - Безопасность: <b> "
                                  f"{data.get('grades13')}</b>"
                                  f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                  f"{data.get('grades14')}</b>"
                                  f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                                  f"{data.get('grades15')}</b>"
                                  f"\n16. Техника наращивания - Симметрия прядей: <b> "
                                  f"{data.get('grades16')}</b>"
                                  f"\n17. Техника наращивания - Попадание цвета кератина в тон корней: <b> "
                                  f"{data.get('grades17')}</b>"
                                  f"\nПроставьте <b>штрафные баллы</b>",
                                  reply_markup=inline.grades_kb())
        await Grades.next()
    else:
        await state.set_state(Grades.grades17_1.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(
                f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                f"<b> {data.get('grades3')}</b>"
                f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                f"<b>{data.get('grades6')}</b>"
                f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                f"<b>{data.get('grades7')}</b>"
                f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                f"{data.get('grades10')}</b>"
                f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                f"{data.get('grades11')}</b>"
                f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                f"{data.get('grades12')}</b>"
                f"\n13. Техника наращивания - Безопасность: <b> "
                f"{data.get('grades13')}</b>"
                f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                f"{data.get('grades14')}</b>"
                f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                f"{data.get('grades15')}</b>"
                f"\n16. Техника наращивания - Симметрия прядей: <b> "
                f"{data.get('grades16')}</b>"
                f"\n\nКритерий: техника наращивания"
                f"\nОцените <b>попадание цвета кератина в тон корней</b>",
                reply_markup=inline.grades_kb())
            await Grades.next()


async def penalty_grades_handle(call: types.CallbackQuery, state: FSMContext):
    if call.data == "back_grades":
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        media_list = [media['video5'], media['photo5'], media['photo6']]
        await call.message.edit_reply_markup()
        await call.message.answer_media_group(media=media_list)
        await call.message.answer(
            f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
            f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
            f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
            f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
            f"<b> {data.get('grades3')}</b>"
            f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
            f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
            f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
            f"<b>{data.get('grades6')}</b>"
            f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
            f"<b>{data.get('grades7')}</b>"
            f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
            f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
            f"\n10. Техника наращивания - Герметичность капсулы: <b> "
            f"{data.get('grades10')}</b>"
            f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
            f"{data.get('grades11')}</b>"
            f"\n12. Техника наращивания - Отсутствие затёков: <b> "
            f"{data.get('grades12')}</b>"
            f"\n13. Техника наращивания - Безопасность: <b> "
            f"{data.get('grades13')}</b>"
            f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
            f"{data.get('grades14')}</b>"
            f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
            f"{data.get('grades15')}</b>"
            f"\n16. Техника наращивания - Симметрия прядей: <b> "
            f"{data.get('grades16')}</b>"
            f"\n\nКритерий: техника наращивания"
            f"\nОцените <b>попадание цвета кератина в тон корней</b>",
            reply_markup=inline.grades_kb())
        await state.set_state(Grades.penalty.state)
    else:
        async with state.proxy() as data:
            data['penalty'] = call.data
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                     f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                     f"{data.get('grades10')}</b>"
                                     f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                     f"{data.get('grades11')}</b>"
                                     f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                     f"{data.get('grades12')}</b>"
                                     f"\n13. Техника наращивания - Безопасность: <b> "
                                     f"{data.get('grades13')}</b>"
                                     f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                     f"{data.get('grades14')}</b>"
                                     f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                                     f"{data.get('grades15')}</b>"
                                     f"\n16. Техника наращивания - Симметрия прядей: <b> "
                                     f"{data.get('grades16')}</b>"
                                     f"\n17. Техника наращивания - Попадание цвета кератина в тон корней: <b> "
                                     f"{data.get('grades17')}</b>"
                                     f"\nШтрафной балл: <b>{data.get('penalty')}</b>",
                                     reply_markup=inline.change_grade_())
        await Grades.next()


async def advice_grade(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_grade":
        await call.message.edit_text(f"Чтобы отправить ваши советы участнику, напишите текстовое сообщение"
                                     f"\n\nЕсли поставили 5 или 9-10 баллов - похвалите участницу."
                                     f"Если 3 и ниже или 1-5 баллов - объясните ошибки и дайте рекомендации"
                                     f"\n\nКол-во символов не ограничено")
        await Grades.next()
    else:
        await state.set_state(Grades.penalty_.state)
        async with state.proxy() as data:
            work = await works.get_all_works_by_id(int(data.get("work")))
            await call.message.edit_text(
                f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                f"<b> {data.get('grades3')}</b>"
                f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                f"<b>{data.get('grades6')}</b>"
                f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                f"<b>{data.get('grades7')}</b>"
                f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                f"{data.get('grades10')}</b>"
                f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                f"{data.get('grades11')}</b>"
                f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                f"{data.get('grades12')}</b>"
                f"\n13. Техника наращивания - Безопасность: <b> "
                f"{data.get('grades13')}</b>"
                f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                f"{data.get('grades14')}</b>"
                f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                f"{data.get('grades15')}</b>"
                f"\n16. Техника наращивания - Симметрия прядей: <b> "
                f"{data.get('grades16')}</b>"
                f"\n17. Техника наращивания - Попадание цвета кератина в тон корней: <b> "
                f"{data.get('grades17')}</b>"
                f"\nПроставьте <b>штрафные баллы</b>",
                reply_markup=inline.grades_kb())
            await Grades.next()


async def advice_grade_handle(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['advice'] = msg.text
        work = await works.get_all_works_by_id(int(data.get("work")))
        status = await referees.get_name_by_tg_id(msg.from_user.id)
        markup = inline.grade_confirmation()
        if status[1] == "Главная судья":
            markup = inline.grade_confirmation_()
        await msg.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                         f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                         f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                         f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                         f"<b> {data.get('grades3')}</b>"
                         f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                         f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                         f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                         f"<b>{data.get('grades6')}</b>"
                         f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                         f"<b>{data.get('grades7')}</b>"
                         f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                         f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                         f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                         f"{data.get('grades10')}</b>"
                         f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                         f"{data.get('grades11')}</b>"
                         f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                         f"{data.get('grades12')}</b>"
                         f"\n13. Техника наращивания - Безопасность: <b> "
                         f"{data.get('grades13')}</b>"
                         f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                         f"{data.get('grades14')}</b>"
                         f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                         f"{data.get('grades15')}</b>"
                         f"\n16. Техника наращивания - Симметрия прядей: <b> "
                         f"{data.get('grades16')}</b>"
                         f"\n17. Техника наращивания - Попадание цвета кератина в тон корней: <b> "
                         f"{data.get('grades17')}</b>"
                         f"\nШтрафной балл: <b>{data.get('penalty')}</b>"
                         f"\n\n<b>Рекомендации:</b> {data.get('advice')}",
                         reply_markup=markup)
        await Grades.next()


async def grade_confirmation_handler(call: types.CallbackQuery, state: FSMContext):
    referee_name = await referees.get_name_by_tg_id(call.from_user.id)
    status = await referees.get_name_by_tg_id(call.from_user.id)
    if call.data == 'finish_grade':
        async with state.proxy() as data:
            data['referee'] = referee_name[0]
            work = await works.get_all_works_by_id(int(data.get("work")))
        grades.add_grades(data)
        category = await participants.get_category_from_name(work[1])
        await google_sheets.write_answers_to_sheet(data, work, category[0])
        works.delete_referee_from_list(data.get('work'), referee_name[0])
        if status[1] == "Главная судья":
            await call.message.edit_text(
                f"Спасибо! Ваши оценки учтены!"
                f"\n\nДля судейства следующей работы в номинации “{work[2]}” нажмите команду /next"
                f"\n\nСпасибо! Для просмотра баллов по этой работе нажмите на команду /check")
            await state.set_state(Grades.check.state)
        else:
            await call.message.edit_text(
                f"Спасибо! Ваши оценки учтены и отправлены главной судьи"
                f"\n\nДля судейства следующей работы в номинации “{work[2]}” нажмите команду /next")
            await state.finish()
    else:
        await call.message.edit_text("Выберите критерий, в которым вы хотите поставить другую оценку",
                                     reply_markup=inline.all_grades())
        await Grades.next()


async def change_all_grades_handler(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        work = await works.get_all_works_by_id(int(data.get("work")))
        media = await get_media_list(work)
        if call.data.startswith('grade_'):
            markup = inline.new_5_grades()
            grade = int(call.data.split("_")[1])
            if grade in [1, 2, 3]:
                media_list = [media['photo3'], media['video3']]
            elif grade == 4:
                media_list = [media['video1'], media['photo1'], media['video2'], media['photo2']]
            elif grade in [5, 6, 7, 8]:
                media_list = [media['video6'], media['video7'], media['photo7'], media['video8'], media['photo8']]
            elif grade == 9:
                media_list = [media['video9']]
            elif grade in [10, 11, 12, 13]:
                media_list = [media['video4'], media['photo4']]
            elif grade in [14, 15, 16, 17]:
                media_list = [media['video5'], media['photo5'], media['photo6']]
            if grade == 1:
                text = "Критерий: техника капсуляции прядей.\nОцените <b>геометрию</b>"
            elif grade == 2:
                text = "Критерий: техника капсуляции прядей.\nОцените <b>пропитку</b>"
            elif grade == 3:
                text = "Критерий: техника капсуляции прядей.\nОцените <b>равномерность распределения кератина</b>"
            elif grade == 4:
                text = "Оцените <b>соответствие и сложность в номинации</b>"
                markup = inline.new_10_grades()
            elif grade == 5:
                text = "Критерий: внешний вид работы\nОцените <b>форму и структуру волос</b>"
            elif grade == 6:
                text = "Критерий: внешний вид работы\nОцените <b>сложность подбора цвета волос</b>"
            elif grade == 7:
                text = "Критерий: внешний вид работы\nОцените <b>точность попадания в цвет волос</b>"
            elif grade == 8:
                text = "Критерий: внешний вид работы\nОцените <b>общий вид работы</b>"
                markup = inline.new_10_grades()
            elif grade == 9:
                text = "Критерий: внешний вид работы\nОцените <b>расстановку прядей</b>"
            elif grade == 10:
                text = "Критерий: техника наращивания\nОцените <b>герметичность капсулы</b>"
            elif grade == 11:
                text = "Критерий: техника наращивания\nОцените <b>обтекаемость капсулы</b>"
            elif grade == 12:
                text = "Критерий: техника наращивания\nОцените <b>отсутствие затёков</b>"
            elif grade == 13:
                text = "Критерий: техника наращивания\nОцените <b>безопасность</b>"
            elif grade == 14:
                text = "Критерий: техника наращивания\nОцените <b>чистоту выбранных рядов и базы</b>"
            elif grade == 15:
                text = "Критерий: техника наращивания\nОцените <b>незаметность капсул в открытом ряду</b>"
                markup = inline.new_10_grades()
            elif grade == 16:
                text = "Критерий: техника наращивания\nОцените <b>симметрию прядей</b>"
            elif grade == 17:
                text = "Критерий: техника наращивания\nОцените <b>попадание цвета кератина в тон корней</b>"
            await call.message.answer_media_group(media=media_list)
            await call.message.answer(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                      f"\n\n{text}", reply_markup=markup)
            data['all_grades'] = call.data.split("_")[1]
            await Grades.next()
        else:
            text = "Проставьте <b>штрафные баллы</b>"
            await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                         f"\n\n{text}", reply_markup=inline.new_5_grades())
            data['all_grades'] = call.data
            await Grades.next()


async def change_data(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        if data.get('all_grades') == "penalty":
            await state.update_data({f"penalty": f"{call.data}"})
            await call.message.edit_text(f"""Подтвердите изменение оценки с """
                                         f"""{data.get('penalty')} на {call.data}""",
                                         reply_markup=inline.new_grade_confirmation())
        else:
            await state.update_data({f"grades{data.get('all_grades')}": f"{call.data}"})
            await call.message.edit_text(f"""Подтвердите изменение оценки с """
                                         f"""{data.get(f"grades{data.get('all_grades')}")} на {call.data}""",
                                         reply_markup=inline.new_grade_confirmation())
        await Grades.next()


async def yet_another_grade_function(call: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        work = await works.get_all_works_by_id(int(data.get("work")))
        await call.message.edit_text(f"Номинация <b>“{work[2]}”</b>\n\nРабота № <b>{data.get('work')}</b>"
                                     f"\n\n1. Техника капсуляции прядей - Геометрия: <b>{data.get('grades1')}</b>"
                                     f"\n2. Техника капсуляции прядей - Пропитка: <b>{data.get('grades2')}</b>"
                                     f"\n3. Техника капсуляции прядей - Равномерность распределения кератина:"
                                     f"<b> {data.get('grades3')}</b>"
                                     f"\n4. Соответствие и сложность в номинации: <b>{data.get('grades4')}</b>"
                                     f"\n5. Внешний вид работы - Форма и структура волос: <b>{data.get('grades5')}</b>"
                                     f"\n6. Внешний вид работы - Сложность подбора цвета волос: "
                                     f"<b>{data.get('grades6')}</b>"
                                     f"\n7. Внешний вид работы - Точность попадания в цвет волос: "
                                     f"<b>{data.get('grades7')}</b>"
                                     f"\n8. Внешний вид работы - Общий вид работы: <b> {data.get('grades8')}</b>"
                                     f"\n9. Внешний вид работы - Расстановка прядей: <b> {data.get('grades9')}</b>"
                                     f"\n10. Техника наращивания - Герметичность капсулы: <b> "
                                     f"{data.get('grades10')}</b>"
                                     f"\n11. Техника наращивания - Обтекаемость капсулы: <b> "
                                     f"{data.get('grades11')}</b>"
                                     f"\n12. Техника наращивания - Отсутствие затёков: <b> "
                                     f"{data.get('grades12')}</b>"
                                     f"\n13. Техника наращивания - Безопасность: <b> "
                                     f"{data.get('grades13')}</b>"
                                     f"\n14. Техника наращивания - Чистота выбранных рядов и базы: <b> "
                                     f"{data.get('grades14')}</b>"
                                     f"\n15. Техника наращивания - Незаметность капсул в открытом ряду: <b> "
                                     f"{data.get('grades15')}</b>"
                                     f"\n16. Техника наращивания - Симметрия прядей: <b> "
                                     f"{data.get('grades16')}</b>"
                                     f"\n17. Техника наращивания - Попадание цвета кератина в тон корней: <b> "
                                     f"{data.get('grades17')}</b>"
                                     f"\nШтрафной балл: <b>{data.get('penalty')}</b>"
                                     f"\n\n<b>Рекомендации:</b> {data.get('advice')}",
                                     reply_markup=inline.grade_confirmation())
        await state.set_state(Grades.finish.state)


async def handle_check_command(msg: types.Message, state: FSMContext):
    async with state.proxy() as data:
        work_id = int(data.get('work'))
        work = await works.get_all_works_by_id(work_id)
    referee_name = await referees.get_name_by_tg_id(msg.from_id)
    referees_names_list = [name[0] for name in await referees.get_panel_from_name(referee_name[0])]
    for referee in referees_names_list:
        grades_ = await grades.get_all_grades_by_id_and_referee(work_id, referee)
        if grades_:
            await msg.answer(f"{referee}"
                             f"\n\nНоминация <b>“{work[2]}”</b>\n\nРабота № <b>{work_id}</b>"
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
    await msg.answer(f"Для судейства следующей работы в номинации “{work[2]}” нажмите команду /next")
    await state.finish()


def register(dp: Dispatcher):
    dp.register_message_handler(select_work, commands=['rate', 'next'], state='*')
    dp.register_callback_query_handler(hh_nomination, lambda c: c.data.startswith("hh"))
    dp.register_callback_query_handler(first_grade, state=Grades.work)
    dp.register_callback_query_handler(back_button_handler, state=Grades.back_state)
    dp.register_callback_query_handler(first_grade_handler, state=Grades.grades1)
    dp.register_callback_query_handler(second_grade, state=Grades.grades2)
    dp.register_callback_query_handler(second_grade_handler, state=Grades.grades3)
    dp.register_callback_query_handler(third_grade, state=Grades.grades3_1)
    dp.register_callback_query_handler(third_grade_handler, state=Grades.grades4)
    dp.register_callback_query_handler(fourth_grade, state=Grades.grades4_1)
    dp.register_callback_query_handler(fourth_grade_handler, state=Grades.grades5)
    dp.register_callback_query_handler(fifth_grade, state=Grades.grades5_1)
    dp.register_callback_query_handler(fifth_grade_handle, state=Grades.grades6)
    dp.register_callback_query_handler(sixth_grade, state=Grades.grades6_1)
    dp.register_callback_query_handler(sixth_grade_handle, state=Grades.grades7)
    dp.register_callback_query_handler(seven_grade, state=Grades.grades7_1)
    dp.register_callback_query_handler(seven_grade_handle, state=Grades.grades8)
    dp.register_callback_query_handler(eighth_grade, state=Grades.grades8_1)
    dp.register_callback_query_handler(eight_grade_handle, state=Grades.grades9)
    dp.register_callback_query_handler(ninth_grade, state=Grades.grades9_1)
    dp.register_callback_query_handler(ninth_grade_handle, state=Grades.grades10)
    dp.register_callback_query_handler(ten_grade, state=Grades.grades10_1)
    dp.register_callback_query_handler(ten_grade_handle, state=Grades.grades11)
    dp.register_callback_query_handler(eleven_grade, state=Grades.grades11_1)
    dp.register_callback_query_handler(eleven_grade_handle, state=Grades.grades12)
    dp.register_callback_query_handler(twelve_grade, state=Grades.grades12_1)
    dp.register_callback_query_handler(twelve_grade_handle, state=Grades.grades13)
    dp.register_callback_query_handler(thirteen_grade, state=Grades.grades13_1)
    dp.register_callback_query_handler(thirteen_grade_handle, state=Grades.grades14)
    dp.register_callback_query_handler(fourteen_grade, state=Grades.grades14_1)
    dp.register_callback_query_handler(fourteen_grade_handle, state=Grades.grades15)
    dp.register_callback_query_handler(fifteen_grade, state=Grades.grades15_1)
    dp.register_callback_query_handler(fifteen_grade_handle, state=Grades.grades16)
    dp.register_callback_query_handler(sixteen_grade, state=Grades.grades16_1)
    dp.register_callback_query_handler(sixteen_grade_handle, state=Grades.grades17)
    dp.register_callback_query_handler(seventeen_grade, state=Grades.grades17_1)
    dp.register_callback_query_handler(seventeen_grade_handle, state=Grades.penalty)
    dp.register_callback_query_handler(penalty_grade, state=Grades.penalty_)
    dp.register_callback_query_handler(penalty_grades_handle, state=Grades.advice)
    dp.register_callback_query_handler(advice_grade, state=Grades.advice_)
    dp.register_message_handler(advice_grade_handle, state=Grades.advice_2)
    dp.register_callback_query_handler(grade_confirmation_handler, state=Grades.finish)
    dp.register_callback_query_handler(change_all_grades_handler, state=Grades.all_grades)
    dp.register_callback_query_handler(change_data, state=Grades.change_grade)
    dp.register_callback_query_handler(yet_another_grade_function, state=Grades.last_state)
    dp.register_message_handler(handle_check_command, state=Grades.check)
