import datetime

from aiogram import Dispatcher, types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from database import referees, works
from keyboards import inline


class Grades(StatesGroup):
    work = State()


async def select_work(msg: types.Message):
    all_referee_ids = [tg_id[0] for tg_id in await referees.get_all_tg_ids()]
    if msg.from_id in all_referee_ids:
        status = await referees.get_name_by_tg_id(msg.from_id)
        if status[1] != "Комитет по судейству":
            if datetime.datetime.now().date().strftime("%Y-%m-%d") in ["2023-05-30", "2023-05-31"]:
                nomination = "Редкие волосы"
            elif datetime.datetime.now().date().strftime("%Y-%m-%d") in ["2023-06-02", "2023-06-03"]:
                nomination = "Ровный срез"
            elif datetime.datetime.now().date().strftime("%Y-%m-%d") in ["2023-06-05", "2023-06-16"]:
                nomination = "Короткие волосы"
            else:
                nomination = None
                await msg.answer("Сегодня нет судейств")
            if nomination:
                await msg.answer(f"Номинация: {nomination}\n\nВыберите номер работы:")
            else:
                pass
        else:
            await msg.answer("Выберите номинацию, в которой хотите проверить работу",
                             reply_markup=inline.nomination_choice())
    else:
        await msg.answer("Эта команда предназначена только для судей!")


async def hh_nomination(call: types.CallbackQuery):
    referee_name = referees.get_name_by_tg_id(call.from_user.id)
    nomination = call.data.split(":")[1]
    works_list = works.get_works_by_referee(nomination, referee_name)
    if works_list:
    else:
        await call.message.edit_text(f"Номинация {nomination} еще не началась или вы уже проверили все работы по"
                                     f"этой номинации!")



def register(dp: Dispatcher):
    dp.register_message_handler(select_work, commands='rate', state='*')
    dp.register_callback_query_handler(hh_nomination, lambda c: c.data.startswith("hh"))
