import asyncio
import datetime
import decouple

from aiogram import Dispatcher, types, Bot
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.utils.exceptions import BotBlocked

from database import participants, works, referees
from keyboards import inline

bot = Bot(decouple.config('BOT_TOKEN'), parse_mode="HTML")


class Nomination_second(StatesGroup):
    first_photo = State()
    second_photo = State()
    first_video = State()
    second_video = State()
    third_video = State()
    third_photo = State()
    fourth_video = State()
    fourth_photo = State()
    fifth_video = State()
    fifth_photo = State()
    sixth_photo = State()
    sixth_video = State()
    seventh_video = State()
    eighth_video = State()
    ninth_video = State()
    seventh_photo = State()
    eighth_photo = State()


async def start_nomination(msg: types.Message):
    all_tg_ids = [all_ids[0] for all_ids in await participants.all_nominations_ids("Ровный срез")]
    for tg_id in all_tg_ids:
        user_data = await participants.get_name_by_tg_id(tg_id)
        session = await bot.get_session()
        try:
            if user_data[1] == "Champ2023|Econom":
                await bot.send_message(
                    tg_id,
                    f"<b>{user_data[0]}</b>, вы участвуете в номинации “Ровный срез”"
                    "\n\nВаш тариф участия: <b>Econom</b>"
                    "\n\n<b>В ваш тариф входит участие в 1 номинации.</b>"
                    "\n\nЗайдите в конференцию ZOOM с того устройства, который <b>НЕ нужен</b> "
                    "для съемки работы, ожидайте официального начала Чемпионата"
                    "\n\nВаша ссылка на подключение к конференции ZOOM "
                    "https://us06web.zoom.us/j/89140506499?pwd=ZjBobUZRckp3ckxtUGMvdWpwaDJJZz09")
            elif user_data[1] == "Champ2023|Premium":
                await bot.send_message(
                    tg_id,
                    f"<b>{user_data[0]}</b>, вы участвуете в номинации “Ровный срез”"
                    "\n\nВаш тариф участия: <b>Premium</b>"
                    "\n\n<b>В ваш тариф входит участие в 2 номинациях.</b>"
                    "\n\nЗайдите в конференцию ZOOM с того устройства, который <b>НЕ нужен</b> "
                    "для съемки работы, ожидайте официального начала Чемпионата"
                    "\n\nВаша ссылка на подключение к конференции ZOOM "
                    "https://us06web.zoom.us/j/89140506499?pwd=ZjBobUZRckp3ckxtUGMvdWpwaDJJZz09")
            elif user_data[1] == "Champ2023|Vip":
                await bot.send_message(
                    tg_id,
                    f"<b>{user_data[0]}</b>, вы участвуете в номинации “Ровный срез”"
                    "\n\nВаш тариф участия: <b>Vip</b>"
                    "\n\n<b>В ваш тариф входит участие в 3 номинациях.</b>"
                    "\n\nЗайдите в конференцию ZOOM с того устройства, который <b>НЕ нужен</b> "
                    "для съемки работы, ожидайте официального начала Чемпионата"
                    "\n\nВаша ссылка на подключение к конференции ZOOM "
                    "https://us06web.zoom.us/j/89140506499?pwd=ZjBobUZRckp3ckxtUGMvdWpwaDJJZz09")
            await bot.send_message(tg_id, "Ожидайте команду от ведущего в ZOOM, чтобы начать выполнять работу")
            await session.close()
        except BotBlocked:
            print(f"Bot was blocked by user {tg_id}")


async def handle_first_photo(msg: types.Message, state: FSMContext):
    if msg.video:
        await msg.delete()
        await msg.answer("Необходимо отправить фото, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить фото в виде фото, а не а виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Фото модели по ракурсу “№1” загружено", reply_markup=inline.confirm_angle_photo())
        async with state.proxy() as data:
            data["first_photo"] = msg.photo[-1].file_id


async def change_media_first(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        photo = decouple.config("PHOTO_2_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: “Ровный срез”"
                    "\n\nЗагрузите фото №2. Для этого отправьте фото в этот чат\n\n<b>Инструкция по съемке:</b>\n"
                    "В кадре находится модель по пояс, стоя лицом к камере. Волосы модели распущены и не убраны "
                    "за уши, перекинуты на спину. В центре кадра плечевая линия модели. Положение камеры "
                    "перпендикулярно полу. Камера закреплена на штативе или съемку производит третье лицо."
                    "Рекомендованное расстояние от камеры до модели - до 2х метров."
                    "\n\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()
    else:
        await state.finish()
        photo = decouple.config("PHOTO_1_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: “Ровный срез”\n\nЗагрузите фото №1. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nВ кадре находится модель по пояс, стоя лицом к камере."
                    "Волосы модели распущены и не убраны за уши, перекинуты вперед. В центре кадра плечевая"
                    " линия модели. Положение камеры перпендикулярно полу. Камера закреплена на штативе "
                    "или съемку производит третье лицо. Рекомендованное расстояние от камеры до модели - "
                    "до 2х метров.\n\n\nРедактировать фото запрещено❌")
        await Nomination_second.first_photo.set()


async def handle_second_photo(msg: types.Message, state: FSMContext):
    if msg.video:
        await msg.delete()
        await msg.answer("Необходимо отправить фото, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить фото в виде фото, а не а виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Фото модели по ракурсу “№2” загружено", reply_markup=inline.confirm_angle_photo())
        async with state.proxy() as data:
            data["second_photo"] = msg.photo[-1].file_id


async def change_media_second(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        video = decouple.config("VIDEO_1_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: “Ровный срез”"
                    "\n\nЗагрузите видео №1. Для этого отправьте видео в этот чат\n\n<b>Инструкция по съемке:</b>"
                    "\nМодель стоит ровно на фоне белой или однотонной стены, лицом к камере. Волосы распущены, "
                    "не убраны за уши. Модель смотрит прямо в камеру и поворачивается на 360 градусов. "
                    "В кадре - по пояс. Центр кадра находится на уровне плечевой линии модели. Камеру держим в "
                    "перпендикулярном положении относительно пола. Камера закреплена на штативе или съемка "
                    "производится третьим лицом. Рекомендованное расстояние от камеры до модели - "
                    "до 2х метров. Длительность видео до 15 секунд. !Снимается одним непрерывным дублем!"
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.first_photo.state)
        photo = decouple.config("PHOTO_2_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: “Ровный срез”"
                    "\n\nЗагрузите фото №2. Для этого отправьте фото в этот чат\n\n<b>Инструкция по съемке:</b>\n"
                    "В кадре находится модель по пояс, стоя лицом к камере. Волосы модели распущены и не убраны "
                    "за уши, перекинуты на спину. В центре кадра плечевая линия модели. Положение камеры "
                    "перпендикулярно полу. Камера закреплена на штативе или съемку производит третье лицо."
                    "Рекомендованное расстояние от камеры до модели - до 2х метров."
                    "\n\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()


async def handle_first_video(msg: types.Message, state: FSMContext):
    if msg.photo:
        await msg.delete()
        await msg.answer("Необходимо отправить видео, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить видео в виде видео, а не в виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Видео модели по ракурсу “№1” загружено", reply_markup=inline.confirm_angle_video())
        async with state.proxy() as data:
            data["first_video"] = msg.video.file_id


async def change_media_third(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        video = decouple.config("VIDEO_2_STRAIGHT")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'"
                    "\n\nЗагрузите видео №2. Для этого отправьте видео в этот чат"
                    "\n\n<b>Инструкция по съемке:</b> "
                    "\nМодель сидит в кресле с прямой спиной. Волосы распущены и не убраны за уши. "
                    "Демонстрируется густота и плотность ровного края стрижки в зоне затылка со спины "
                    "в распущенном виде. Далее участник демонстрирует густоту кончиков путем собирания"
                    " волос модели в низкий жгут. В центра кадра - демонстрируемая зона. "
                    "После этого находится наивысшая точка головы, и выделяется прямой ряд параллельный "
                    "полу на расстоянии 5-6 см ниже этой зоны. Кончики кладутся на белый лист бумаги. "
                    "В центре кадра фиксируется густота концов и ровность среза. Камеру держим в "
                    "перпендикулярном положении относительно пола. Камера закреплена на штативе или "
                    "съемка производится третьим лицом. Рекомендованное расстояние от камеры до модели до 50 см."
                    " Длительность видео до 40 секунд. Снимается одним непрерывным дублем."
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.second_photo.state)
        video = decouple.config("VIDEO_1_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: “Ровный срез”"
                    "\n\nЗагрузите видео №1. Для этого отправьте видео в этот чат\n\n<b>Инструкция по съемке:</b>"
                    "\nМодель стоит ровно на фоне белой или однотонной стены, лицом к камере. Волосы распущены, "
                    "не убраны за уши. Модель смотрит прямо в камеру и поворачивается на 360 градусов. "
                    "В кадре - по пояс. Центр кадра находится на уровне плечевой линии модели. Камеру держим в "
                    "перпендикулярном положении относительно пола. Камера закреплена на штативе или съемка "
                    "производится третьим лицом. Рекомендованное расстояние от камеры до модели - "
                    "до 2х метров. Длительность видео до 15 секунд. !Снимается одним непрерывным дублем!"
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()


async def handle_second_video(msg: types.Message, state: FSMContext):
    if msg.photo:
        await msg.delete()
        await msg.answer("Необходимо отправить видео, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить видео в виде видео, а не в виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Видео модели по ракурсу “№2” загружено", reply_markup=inline.confirm_angle_video())
        async with state.proxy() as data:
            data["second_video"] = msg.video.file_id


async def change_media_fourth(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        video = decouple.config("VIDEO_3_SHORT_STRAIGHT")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'"
                    "\n\nЗагрузите видео №3. Для этого отправьте видео в этот чат\n\n<b>Инструкция по съемке:</b> "
                    "\nВ начале съемки фиксируется лицо участника чемпионата, далее приближается камера и "
                    "снимается процесс капсуляции: 3 микро и 3 стандартных прядей поштучно (перекапсуляция "
                    "готовых прядей). Демонстрируется техника работы. Далее закапсулированные пряди "
                    "демонстрируются поочередно со всех сторон на фоне белого листа бумаги. Камера держится "
                    "таким образом, чтобы руки и щипцы не мешали разглядеть капсулу (для правшей - камера слева, "
                    "для левшей - справа). В центре кадра находится капсулируемая прядь. Камеру держим либо в "
                    "перпендикулярном положении относительно пола, либо с небольшим наклоном в сторону "
                    "демонстрируемой зоны. Камера закреплена на штативе либо съемку производит третье лицо. "
                    "Рекомендованное расстояние от камеры до капсулы до 30 см. В центре кадра находится "
                    "демонстрируемая капсула. Общая длительность видео до 7 минут. "
                    "Снимается одним непрерывным дублем.\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.first_video.state)
        video = decouple.config("VIDEO_2_STRAIGHT")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'"
                    "\n\nЗагрузите видео №2. Для этого отправьте видео в этот чат"
                    "\n\n<b>Инструкция по съемке:</b> "
                    "\nМодель сидит в кресле с прямой спиной. Волосы распущены и не убраны за уши. "
                    "Демонстрируется густота и плотность ровного края стрижки в зоне затылка со спины "
                    "в распущенном виде. Далее участник демонстрирует густоту кончиков путем собирания"
                    " волос модели в низкий жгут. В центра кадра - демонстрируемая зона. "
                    "После этого находится наивысшая точка головы, и выделяется прямой ряд параллельный "
                    "полу на расстоянии 5-6 см ниже этой зоны. Кончики кладутся на белый лист бумаги. "
                    "В центре кадра фиксируется густота концов и ровность среза. Камеру держим в "
                    "перпендикулярном положении относительно пола. Камера закреплена на штативе или "
                    "съемка производится третьим лицом. Рекомендованное расстояние от камеры до модели до 50 см."
                    " Длительность видео до 40 секунд. Снимается одним непрерывным дублем."
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()


async def handle_third_video(msg: types.Message, state: FSMContext):
    if msg.photo:
        await msg.delete()
        await msg.answer("Необходимо отправить видео, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить видео в виде видео, а не в виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Видео модели по ракурсу “№3” загружено", reply_markup=inline.confirm_angle_video())
        async with state.proxy() as data:
            data["third_video"] = msg.video.file_id


async def change_media_fifth(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        photo = decouple.config("PHOTO_3_SHORT_STRAIGHT")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'"
                    "\n\nЗагрузите фото №3. Для этого отправьте фото в этот чат\n\n<b>Инструкция по съемке:</b> "
                    "\nНа белый лист бумаги выкладывается 6 прядей (3 микро и 3 стандартных). "
                    "В центре кадра крупным планом находятся 6 закапсулируемых "
                    "прядей (не длина прядей, а именно капсулы). Положение камеры параллельно демонстрируемых "
                    "прядей. Камера закреплена на штативе или съемка производится третьим лицом. "
                    "Рекомендованное расстояние от камеры до капсул до 20 см.\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.second_video.state)
        video = decouple.config("VIDEO_3_SHORT_STRAIGHT")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'"
                    "\n\nЗагрузите видео №3. Для этого отправьте видео в этот чат\n\n<b>Инструкция по съемке:</b> "
                    "\nВ начале съемки фиксируется лицо участника чемпионата, далее приближается камера и снимается"
                    " процесс капсуляции: 3 микро и 3 стандартных прядей поштучно (перекапсуляция готовых прядей). "
                    "Демонстрируется техника работы. Далее закапсулированные пряди демонстрируются поочередно со "
                    "всех сторон на фоне белого листа бумаги. Камера держится таким образом, чтобы руки и "
                    "щипцы не мешали разглядеть капсулу (для правшей - камера слева, для левшей - справа). В "
                    "центре кадра находится капсулируемая прядь. Камеру держим либо в перпендикулярном положении "
                    "относительно пола, либо с небольшим наклоном в сторону демонстрируемой зоны. Камера "
                    "закреплена на штативе либо съемку производит третье лицо. Рекомендованное расстояние "
                    "от камеры до капсулы до 30 см. В центре кадра находится демонстрируемая капсула."
                    "Общая длительность видео до 7 минут. Снимается одним непрерывным дублем."
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()


async def handle_third_photo(msg: types.Message, state: FSMContext):
    if msg.video:
        await msg.delete()
        await msg.answer("Необходимо отправить фото, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить фото в виде фото, а не а виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Фото модели по ракурсу “№3” загружено", reply_markup=inline.confirm_angle_photo())
        async with state.proxy() as data:
            data["third_photo"] = msg.photo[-1].file_id


async def change_media_sixth(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        video = decouple.config("VIDEO_4_ALL")
        await call.message.delete()
        await call.message.answer_video(video=video)
        await call.message.answer(
            "Номинация: 'Ровный срез'"
            "\n\nЗагрузите видео №4. Для этого отправьте видео в этот чат\n\n<b>Инструкция по съемке:</b> "
            "\nВ начале съемки фиксируется лицо участника чемпионата, далее демонстрируется техника "
            "наращивания. Для демонстрации используются закапсулированные 6 прядей (сделанные при "
            "демонстрации техники капсуляции, 3 микро и 3 стандартные пряди). Пушковые и короткие волосы, "
            "мешающие демонстрации, хорошо подколоты. В центре кадра находится наращиваемая прядь. Камеру "
            "держим в перпендикулярном положении относительно пола либо с небольшим наклоном к демонстрируемой"
            " зоне. Если вы правша - камера находится слева. Если левша, то справа. Камера закреплена на "
            "штативе либо съемку производит третье лицо. Рекомендованное расстояние от камеры до капсулы "
            "до 50 см. Далее наращенные пряди демонстрируются на фоне белого листа бумаги (подкладывается "
            "под ряд). В центре кадра находятся демонстрируемые капсулы. Камеру держим в перпендикулярном "
            "положении относительно пола. Камера закреплена на штативе либо съемку производит третье лицо. "
            "Рекомендованное расстояние от камеры до капсулы до 30 см. Общая длительность видео до 7 минут. "
            "Снимается одним непрерывным дублем.\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.third_video.state)
        photo = decouple.config("PHOTO_3_SHORT_STRAIGHT")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'"
                    "\n\nЗагрузите фото №3. Для этого отправьте фото в этот чат\n\n<b>Инструкция по съемке:</b> "
                    "\nНа белый лист бумаги выкладывается 6 прядей (3 микро и 3 стандартных). "
                    "В центре кадра крупным планом находятся 6 закапсулируемых "
                    "прядей (не длина прядей, а именно капсулы). Положение камеры параллельно демонстрируемых "
                    "прядей. Камера закреплена на штативе или съемка производится третьим лицом. "
                    "Рекомендованное расстояние от камеры до капсул до 20 см.\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()


async def handle_fourth_video(msg: types.Message, state: FSMContext):
    if msg.photo:
        await msg.delete()
        await msg.answer("Необходимо отправить видео, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить видео в виде видео, а не в виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Видео модели по ракурсу “№4” загружено", reply_markup=inline.confirm_angle_video())
        async with state.proxy() as data:
            data["fourth_video"] = msg.video.file_id


async def change_media_seventh(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        photo = decouple.config("PHOTO_4_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите фото №4. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b> \nПод наращенные 6 капсул подкладывают белый лист бумаги. "
                    "В центре кадра КРУПНО находятся 6 наращенных прядей. Положение камеры параллельно "
                    "демонстрируемых прядей. Рекомендованное расстояние от камеры до капсул до 20 см."
                    "\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.third_photo.state)
        video = decouple.config("VIDEO_4_ALL")
        await call.message.delete()
        await call.message.answer_video(video=video)
        await call.message.answer(
            "Номинация: 'Ровный срез'"
            "\n\nЗагрузите видео №4. Для этого отправьте видео в этот чат\n\n<b>Инструкция по съемке:</b> "
            "\nВ начале съемки фиксируется лицо участника чемпионата, далее демонстрируется техника "
            "наращивания. Для демонстрации используются закапсулированные 6 прядей (сделанные при "
            "демонстрации техники капсуляции, 3 микро и 3 стандартные пряди). Пушковые и короткие волосы, "
            "мешающие демонстрации, хорошо подколоты. В центре кадра находится наращиваемая прядь. Камеру "
            "держим в перпендикулярном положении относительно пола либо с небольшим наклоном к демонстрируемой"
            " зоне. Если вы правша - камера находится слева. Если левша, то справа. Камера закреплена на "
            "штативе либо съемку производит третье лицо. Рекомендованное расстояние от камеры до капсулы "
            "до 50 см. Далее наращенные пряди демонстрируются на фоне белого листа бумаги (подкладывается "
            "под ряд). В центре кадра находятся демонстрируемые капсулы. Камеру держим в перпендикулярном "
            "положении относительно пола. Камера закреплена на штативе либо съемку производит третье лицо. "
            "Рекомендованное расстояние от камеры до капсулы до 30 см. Общая длительность видео до 7 минут. "
            "Снимается одним непрерывным дублем.\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()


async def handle_fourth_photo(msg: types.Message, state: FSMContext):
    if msg.video:
        await msg.delete()
        await msg.answer("Необходимо отправить фото, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить фото в виде фото, а не а виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Фото модели по ракурсу “№4” загружено", reply_markup=inline.confirm_angle_photo())
        async with state.proxy() as data:
            data["fourth_photo"] = msg.photo[-1].file_id


async def change_media_eight(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        video = decouple.config("VIDEO_5_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите видео №5. Для этого отправьте видео в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nСнимается готовый наращенный ряд (от уха до уха) на "
                    "затылочной части 15-20 прядей. Пушковые и короткие волосы, мешающие демонстрации, хорошо "
                    "подколоты. В центре кадра находится демонстрируемая зона. Камеру держим в перпендикулярном "
                    "положении относительно пола. Рекомендованное расстояние от камеры до капсулы до 20 см. "
                    "Длительность видео до 20 секунд. Снимается одним непрерывным дублем."
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.fourth_video.state)
        photo = decouple.config("PHOTO_4_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите фото №4. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b> \nПод наращенные 6 капсул подкладывают белый лист бумаги. "
                    "В центре кадра КРУПНО находятся 6 наращенных прядей. Положение камеры параллельно "
                    "демонстрируемых прядей. Рекомендованное расстояние от камеры до капсул до 20 см."
                    "\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()


async def handle_fifth_video(msg: types.Message, state: FSMContext):
    if msg.photo:
        await msg.delete()
        await msg.answer("Необходимо отправить видео, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить видео в виде видео, а не в виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Видео модели по ракурсу “№5” загружено", reply_markup=inline.confirm_angle_video())
        async with state.proxy() as data:
            data["fifth_video"] = msg.video.file_id


async def change_media_ninth(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        photo = decouple.config("PHOTO_5_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите фото №5. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b> \nВ центре кадра КРУПНО находятся демонстрируемые капсулы, "
                    "расположенные левее центра головы (то есть левая половина ряда). Положение камеры параллельно"
                    " демонстрируемым прядям. Рекомендованное расстояние от камеры до капсул до 20 см."
                    "\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.fourth_photo.state)
        video = decouple.config("VIDEO_5_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите видео №5. Для этого отправьте видео в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nСнимается готовый наращенный ряд (от уха до уха) на "
                    "затылочной части 15-20 прядей. Пушковые и короткие волосы, мешающие демонстрации, хорошо "
                    "подколоты. В центре кадра находится демонстрируемая зона. Камеру держим в перпендикулярном "
                    "положении относительно пола. Рекомендованное расстояние от камеры до капсулы до 20 см. "
                    "Длительность видео до 20 секунд. Снимается одним непрерывным дублем."
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()


async def handle_fifth_photo(msg: types.Message, state: FSMContext):
    if msg.video:
        await msg.delete()
        await msg.answer("Необходимо отправить фото, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить фото в виде фото, а не а виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Фото модели по ракурсу “№5” загружено", reply_markup=inline.confirm_angle_photo())
        async with state.proxy() as data:
            data["fifth_photo"] = msg.photo[-1].file_id


async def change_media_tenth(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        photo = decouple.config("PHOTO_6_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите фото №6. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nВ центре кадра КРУПНО находятся демонстрируемые капсулы, "
                    "расположенные правее центра головы (то есть правая половина ряда). Положение камеры "
                    "параллельно демонстрируемым прядям. Рекомендованное расстояние от камеры до капсул до 20 см."
                    "\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.fifth_video.state)
        photo = decouple.config("PHOTO_5_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите фото №5. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b> \nВ центре кадра КРУПНО находятся демонстрируемые капсулы, "
                    "расположенные левее центра головы (то есть левая половина ряда). Положение камеры параллельно"
                    " демонстрируемым прядям. Рекомендованное расстояние от камеры до капсул до 20 см."
                    "\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()


async def handle_sixth_photo(msg: types.Message, state: FSMContext):
    if msg.video:
        await msg.delete()
        await msg.answer("Необходимо отправить фото, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить фото в виде фото, а не а виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Фото модели по ракурсу “№6” загружено", reply_markup=inline.confirm_angle_photo())
        async with state.proxy() as data:
            data["sixth_photo"] = msg.photo[-1].file_id


async def change_media_eleventh(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        video = decouple.config("VIDEO_6_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите видео №6. Для этого отправьте видео в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nМодель стоит ровно на фоне белой или однотонной стены, "
                    "лицом к камере. В кадре - по пояс. Волосы распущены и не убраны за уши. Модель смотрит прямо"
                    " в камеру и поворачивается на 360 градусов. Центр кадра находится на уровне плечевой линии "
                    "модели. Камеру держим в перпендикулярном положении относительно пола. Рекомендованное "
                    "расстояние от камеры до модели - до 2х метров. Длительность видео до 20 секунд. "
                    "Снимается одним непрерывным дублем.\n\nВНИМАНИЕ! Демонстрируется готовое наращивание без "
                    "укладки и средств стайлинга. Допускается слегка смочить волосы водой из пульверизатора и "
                    "высушить феном при помощи рук, без применения брашинга и других расчесок. Допускается "
                    "стрижка концов для придания прическе итоговой формы без стрижки волос модели."
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.fifth_photo.state)
        photo = decouple.config("PHOTO_6_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите фото №6. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nВ центре кадра КРУПНО находятся демонстрируемые капсулы, "
                    "расположенные правее центра головы (то есть правая половина ряда). Положение камеры "
                    "параллельно демонстрируемым прядям. Рекомендованное расстояние от камеры до капсул до 20 см."
                    "\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()


async def handle_sixth_video(msg: types.Message, state: FSMContext):
    if msg.photo:
        await msg.delete()
        await msg.answer("Необходимо отправить видео, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить видео в виде видео, а не в виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Видео модели по ракурсу “№6” загружено", reply_markup=inline.confirm_angle_video())
        async with state.proxy() as data:
            data["sixth_video"] = msg.video.file_id


async def change_media_twelfth(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        video = decouple.config("VIDEO_7_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите видео №7. Для этого отправьте видео в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nМодель стоит ровно на фоне белой или однотонной стены, "
                    "лицом к камере. Волосы распущены и не убраны за уши. Модель поворачивается на 180 градусов "
                    "спиной к камере. И делает 3-5 встряхивающих движений (голова интенсивно поворачивается влево "
                    "и вправо, модель как бы «вертит» головой из стороны в сторону). В кадре - по пояс. Камеру "
                    "держим в перпендикулярном положении относительно пола. Рекомендованное расстояние от камеры до"
                    " модели - до 2х метров. Длительность видео до 20 секунд. Снимается одним непрерывным дублем."
                    "\n\nВНИМАНИЕ! Демонстрируется готовое наращивание без укладки и средств стайлинга. "
                    "Допускается слегка смочить волосы водой из пульверизатора и высушить феном при помощи рук, "
                    "без применения брашинга и других расчесок. Допускается стрижка концов для придания прическе "
                    "итоговой формы без стрижки волос модели.\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.sixth_photo.state)
        video = decouple.config("VIDEO_6_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите видео №6. Для этого отправьте видео в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nМодель стоит ровно на фоне белой или однотонной стены, "
                    "лицом к камере. В кадре - по пояс. Волосы распущены и не убраны за уши. Модель смотрит прямо"
                    " в камеру и поворачивается на 360 градусов. Центр кадра находится на уровне плечевой линии "
                    "модели. Камеру держим в перпендикулярном положении относительно пола. Рекомендованное "
                    "расстояние от камеры до модели - до 2х метров. Длительность видео до 20 секунд. "
                    "Снимается одним непрерывным дублем.\n\nВНИМАНИЕ! Демонстрируется готовое наращивание без "
                    "укладки и средств стайлинга. Допускается слегка смочить волосы водой из пульверизатора и "
                    "высушить феном при помощи рук, без применения брашинга и других расчесок. Допускается "
                    "стрижка концов для придания прическе итоговой формы без стрижки волос модели."
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()


async def handle_seventh_video(msg: types.Message, state: FSMContext):
    if msg.photo:
        await msg.delete()
        await msg.answer("Необходимо отправить видео, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить видео в виде видео, а не в виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Видео модели по ракурсу “№7” загружено", reply_markup=inline.confirm_angle_video())
        async with state.proxy() as data:
            data["seventh_video"] = msg.video.file_id


async def change_media_thirteenth(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        video = decouple.config("VIDEO_8_ALL")
        await call.message.delete()
        await call.message.answer_video(video=video)
        await call.message.answer(
            "Номинация: 'Ровный срез'\n\nЗагрузите видео №8. Для этого отправьте видео в этот чат"
            "\n\n<b>Инструкция по съемке:</b> \nМодель стоит ровно на фоне белой или однотонной стены, "
            "лицом к камере. В кадре - по пояс. Волосы распущены. Модель самостоятельно собирает все волосы в "
            "хвост, допустимо применение расчески. Высота основания хвоста должна находиться не ниже уровня "
            "кончика носа модели. Хвост собирается при помощи резинки и фиксируется таким образом, чтобы "
            "краевая линия роста волос клиента была хорошо видна по всей поверхности при будущей демонстрации. "
            "Камеру держим в перпендикулярном положении относительно пола. Рекомендованное расстояние от камеры до"
            " модели до 2х метров. После того, как модель собрала хвост, зафиксировала его резинкой и опустила "
            "руки, камера приближается к модели. Поочередно демонстрируется краевая линия левой височной зоны, "
            "затем затылка и после правой височной зоны. В центре кадра находится демонстрируемая зона. Камеру "
            "держим в перпендикулярном положении относительно пола. Рекомендованное расстояние от камеры до модели"
            " - до 40 см. Длительность видео до 2 минут. Снимается одним непрерывным дублем.\n\nВНИМАНИЕ! "
            "Демонстрируется готовое наращивание без укладки и средств стайлинга. Допускается слегка смочить волосы"
            " водой из пульверизатора и высушить феном при помощи рук, без применения брашинга и других расчесок. "
            "Допускается стрижка концов для придания прическе итоговой формы без стрижки волос модели."
            "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.sixth_video.state)
        video = decouple.config("VIDEO_7_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите видео №7. Для этого отправьте видео в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nМодель стоит ровно на фоне белой или однотонной стены, "
                    "лицом к камере. Волосы распущены и не убраны за уши. Модель поворачивается на 180 градусов "
                    "спиной к камере. И делает 3-5 встряхивающих движений (голова интенсивно поворачивается влево "
                    "и вправо, модель как бы «вертит» головой из стороны в сторону). В кадре - по пояс. Камеру "
                    "держим в перпендикулярном положении относительно пола. Рекомендованное расстояние от камеры до"
                    " модели - до 2х метров. Длительность видео до 20 секунд. Снимается одним непрерывным дублем."
                    "\n\nВНИМАНИЕ! Демонстрируется готовое наращивание без укладки и средств стайлинга. "
                    "Допускается слегка смочить волосы водой из пульверизатора и высушить феном при помощи рук, "
                    "без применения брашинга и других расчесок. Допускается стрижка концов для придания прическе "
                    "итоговой формы без стрижки волос модели.\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()


async def handle_eighth_video(msg: types.Message, state: FSMContext):
    if msg.photo:
        await msg.delete()
        await msg.answer("Необходимо отправить видео, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить видео в виде видео, а не в виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Видео модели по ракурсу “№8” загружено", reply_markup=inline.confirm_angle_video())
        async with state.proxy() as data:
            data["eighth_video"] = msg.video.file_id


async def change_media_fourteenth(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        video = decouple.config("VIDEO_9_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите видео №9. Для этого отправьте видео в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nМодель сидит в кресле с ровной спиной. В кадре - чуть ниже "
                    "плеч. Отделяются височные зоны и перекидываются вперед. Участник демонстрирует расстановку "
                    "прядей по рядам, начиная с нижних, поднимаясь выше. После этого переходит на демонстрацию "
                    "височных зон аналогичным образом, начиная снизу и поднимаясь вверх. В центре кадра "
                    "демонстрируемая зона. Камеру держим в перпендикулярном положении относительно пола. "
                    "Рекомендованное расстояние от камеры до модели - до 50 см. Длительность видео до 90 секунд. "
                    "Снимается одним непрерывным дублем.\n\nВНИМАНИЕ! Демонстрируется готовое наращивание без "
                    "укладки и средств стайлинга. Допускается слегка смочить волосы водой из пульверизатора и "
                    "высушить феном при помощи рук, без применения брашинга и других расчесок. Допускается стрижка"
                    " концов для придания прическе итоговой формы без стрижки волос модели."
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.seventh_video.state)
        video = decouple.config("VIDEO_8_ALL")
        await call.message.delete()
        await call.message.answer_video(video=video)
        await call.message.answer(
            "Номинация: 'Ровный срез'\n\nЗагрузите видео №8. Для этого отправьте видео в этот чат"
            "\n\n<b>Инструкция по съемке:</b> \nМодель стоит ровно на фоне белой или однотонной стены, "
            "лицом к камере. В кадре - по пояс. Волосы распущены. Модель самостоятельно собирает все волосы в "
            "хвост, допустимо применение расчески. Высота основания хвоста должна находиться не ниже уровня "
            "кончика носа модели. Хвост собирается при помощи резинки и фиксируется таким образом, чтобы "
            "краевая линия роста волос клиента была хорошо видна по всей поверхности при будущей демонстрации. "
            "Камеру держим в перпендикулярном положении относительно пола. Рекомендованное расстояние от камеры до"
            " модели до 2х метров. После того, как модель собрала хвост, зафиксировала его резинкой и опустила "
            "руки, камера приближается к модели. Поочередно демонстрируется краевая линия левой височной зоны, "
            "затем затылка и после правой височной зоны. В центре кадра находится демонстрируемая зона. Камеру "
            "держим в перпендикулярном положении относительно пола. Рекомендованное расстояние от камеры до модели"
            " - до 40 см. Длительность видео до 2 минут. Снимается одним непрерывным дублем.\n\nВНИМАНИЕ! "
            "Демонстрируется готовое наращивание без укладки и средств стайлинга. Допускается слегка смочить волосы"
            " водой из пульверизатора и высушить феном при помощи рук, без применения брашинга и других расчесок. "
            "Допускается стрижка концов для придания прическе итоговой формы без стрижки волос модели."
            "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()


async def handle_ninth_video(msg: types.Message, state: FSMContext):
    if msg.photo:
        await msg.delete()
        await msg.answer("Необходимо отправить видео, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить видео в виде видео, а не в виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Видео модели по ракурсу “№9” загружено", reply_markup=inline.confirm_angle_video())
        async with state.proxy() as data:
            data["ninth_video"] = msg.video.file_id


async def change_media_fifteenth(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        photo = decouple.config("PHOTO_7_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите фото №7. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nВ кадре находится модель по пояс, стоя лицом к камере. "
                    "Волосы модели распущены и не убраны за уши, перекинуты вперед. Положение камеры "
                    "перпендикулярно полу. В центре кадра плечевая линия модели. Рекомендованное расстояние от "
                    "камеры до модели до 2 метров.\n\nВНИМАНИЕ! Демонстрируется готовое наращивание без укладки "
                    "и средств стайлинга. Допускается слегка смочить волосы водой из пульверизатора и высушить "
                    "феном при помощи рук, без применения брашинга и других расчесок. Допускается стрижка концов "
                    "для придания прическе итоговой формы без стрижки волос модели."
                    "\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.eighth_video.state)
        video = decouple.config("VIDEO_9_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=video,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите видео №9. Для этого отправьте видео в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nМодель сидит в кресле с ровной спиной. В кадре - чуть ниже "
                    "плеч. Отделяются височные зоны и перекидываются вперед. Участник демонстрирует расстановку "
                    "прядей по рядам, начиная с нижних, поднимаясь выше. После этого переходит на демонстрацию "
                    "височных зон аналогичным образом, начиная снизу и поднимаясь вверх. В центре кадра "
                    "демонстрируемая зона. Камеру держим в перпендикулярном положении относительно пола. "
                    "Рекомендованное расстояние от камеры до модели - до 50 см. Длительность видео до 90 секунд. "
                    "Снимается одним непрерывным дублем.\n\nВНИМАНИЕ! Демонстрируется готовое наращивание без "
                    "укладки и средств стайлинга. Допускается слегка смочить волосы водой из пульверизатора и "
                    "высушить феном при помощи рук, без применения брашинга и других расчесок. Допускается стрижка"
                    " концов для придания прическе итоговой формы без стрижки волос модели."
                    "\n\nРедактировать видео запрещено❌")
        await Nomination_second.next()


async def handle_seventh_photo(msg: types.Message, state: FSMContext):
    if msg.video:
        await msg.delete()
        await msg.answer("Необходимо отправить фото, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить фото в виде фото, а не а виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Фото модели по ракурсу “№7” загружено", reply_markup=inline.confirm_angle_photo())
        async with state.proxy() as data:
            data["seventh_photo"] = msg.photo[-1].file_id


async def change_media_sixteenth(call: types.CallbackQuery, state: FSMContext):
    if call.data == "next_angle":
        photo = decouple.config("PHOTO_8_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите фото №8. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nВ кадре находится модель по пояс, стоя спиной к камере. "
                    "Волосы модели распущены и не убраны за уши, перекинуты на спину. В центре кадра плечевая линия"
                    " модели. Положение камеры перпендикулярно полу. Рекомендованное расстояние от камеры до модели"
                    " до 2 метров.\n\nВНИМАНИЕ! Демонстрируется готовое наращивание без укладки и средств "
                    "стайлинга. Допускается слегка смочить волосы водой из пульверизатора и высушить феном при "
                    "помощи рук, без применения брашинга и других расчесок. Допускается стрижка концов для придания"
                    " прическе итоговой формы без стрижки волос модели.\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()
    else:
        await state.set_state(Nomination_second.ninth_video.state)
        photo = decouple.config("PHOTO_7_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите фото №7. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nВ кадре находится модель по пояс, стоя лицом к камере. "
                    "Волосы модели распущены и не убраны за уши, перекинуты вперед. Положение камеры "
                    "перпендикулярно полу. В центре кадра плечевая линия модели. Рекомендованное расстояние от "
                    "камеры до модели до 2 метров.\n\nВНИМАНИЕ! Демонстрируется готовое наращивание без укладки "
                    "и средств стайлинга. Допускается слегка смочить волосы водой из пульверизатора и высушить "
                    "феном при помощи рук, без применения брашинга и других расчесок. Допускается стрижка концов "
                    "для придания прическе итоговой формы без стрижки волос модели."
                    "\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()


async def handle_eighth_photo(msg: types.Message, state: FSMContext):
    if msg.video:
        await msg.delete()
        await msg.answer("Необходимо отправить фото, попробуйте еще раз!")
    elif msg.document:
        await msg.delete()
        await msg.answer("Необходимо отправить фото в виде фото, а не а виде документа, попробуйте еще раз!")
    else:
        await msg.answer("Фото модели по ракурсу “№8” загружено", reply_markup=inline.confirm_angle_finish())
        async with state.proxy() as data:
            data["eighth_photo"] = msg.photo[-1].file_id


async def finish_nomination(call: types.CallbackQuery, state: FSMContext):
    if call.data == "finish_nominations":
        await call.message.edit_text("Поздравляем! Ваша работа в номинации “Ровный срез” сдана! "
                                     "Судьи уже оценивают работы")
        async with state.proxy() as data:
            user_data = await participants.get_name_by_tg_id(call.from_user.id)
            panel, referees_list = await referees.select_all_referees_for_exact_participant(call.from_user.id)
            work_id = await works.add_media(user_data[0], 'Ровный срез', data, referees_list, panel)
            photos = [
                data.get('first_photo'), data.get('second_photo'), data.get('third_photo'), data.get('fourth_photo'),
                data.get('fifth_photo'), data.get('sixth_photo'), data.get('seventh_photo'), data.get('eighth_photo')
            ]
            videos = [
                data.get('first_video'), data.get('second_video'), data.get('third_video'), data.get('fourth_video'),
                data.get('fifth_video'), data.get('sixth_video'), data.get('seventh_video'), data.get('eighth_video'),
                data.get('ninth_video')
            ]
            photo_list = [types.InputMediaPhoto(photo) for photo in photos]
            video_list = [types.InputMediaVideo(video) for video in videos]
            message_id = await call.bot.send_media_group(chat_id=decouple.config('GROUP_ID'), media=photo_list)
            await call.bot.send_media_group(chat_id=decouple.config('GROUP_ID'), media=video_list)
            await call.bot.send_message(chat_id=decouple.config('GROUP_ID'),
                                        reply_to_message_id=message_id[0].message_id,
                                        text=f"Фотографии и видеозаписи участницы {user_data[0]}"
                                             f"\n\nНоминация: Ровный срез"
                                             f"\n\nНомер работы: {work_id[0]}")
            await state.finish()
    else:
        await state.set_state(Nomination_second.seventh_photo.state)
        photo = decouple.config("PHOTO_8_ALL")
        await call.message.delete()
        await call.message.answer_video(
            video=photo,
            caption="Номинация: 'Ровный срез'\n\nЗагрузите фото №8. Для этого отправьте фото в этот чат"
                    "\n\n<b>Инструкция по съемке:</b>\nВ кадре находится модель по пояс, стоя спиной к камере. "
                    "Волосы модели распущены и не убраны за уши, перекинуты на спину. В центре кадра плечевая линия"
                    " модели. Положение камеры перпендикулярно полу. Рекомендованное расстояние от камеры до модели"
                    " до 2 метров.\n\nВНИМАНИЕ! Демонстрируется готовое наращивание без укладки и средств "
                    "стайлинга. Допускается слегка смочить волосы водой из пульверизатора и высушить феном при "
                    "помощи рук, без применения брашинга и других расчесок. Допускается стрижка концов для придания"
                    " прическе итоговой формы без стрижки волос модели.\n\nРедактировать фото запрещено❌")
        await Nomination_second.next()


# async def task():
#     date = datetime.datetime.now()
#     if date.hour == 17:
#         await start_nomination()
#
# asyncio.run(task())


def register(dp: Dispatcher):
    dp.register_message_handler(start_nomination, commands=['straight'], state='*')
    dp.register_message_handler(handle_first_photo, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.first_photo)
    dp.register_callback_query_handler(change_media_first, state=Nomination_second.first_photo)
    dp.register_message_handler(handle_second_photo, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.second_photo)
    dp.register_callback_query_handler(change_media_second, state=Nomination_second.second_photo)
    dp.register_message_handler(handle_first_video, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.first_video)
    dp.register_callback_query_handler(change_media_third, state=Nomination_second.first_video)
    dp.register_message_handler(handle_second_video, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.second_video)
    dp.register_callback_query_handler(change_media_fourth, state=Nomination_second.second_video)
    dp.register_message_handler(handle_third_video, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.third_video)
    dp.register_callback_query_handler(change_media_fifth, state=Nomination_second.third_video)
    dp.register_message_handler(handle_third_photo, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.third_photo)
    dp.register_callback_query_handler(change_media_sixth, state=Nomination_second.third_photo)
    dp.register_message_handler(handle_fourth_video, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.fourth_video)
    dp.register_callback_query_handler(change_media_seventh, state=Nomination_second.fourth_video)
    dp.register_message_handler(handle_fourth_photo, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.fourth_photo)
    dp.register_callback_query_handler(change_media_eight, state=Nomination_second.fourth_photo)
    dp.register_message_handler(handle_fifth_video, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.fifth_video)
    dp.register_callback_query_handler(change_media_ninth, state=Nomination_second.fifth_video)
    dp.register_message_handler(handle_fifth_photo, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.fifth_photo)
    dp.register_callback_query_handler(change_media_tenth, state=Nomination_second.fifth_photo)
    dp.register_message_handler(handle_sixth_photo, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.sixth_photo)
    dp.register_callback_query_handler(change_media_eleventh, state=Nomination_second.sixth_photo)
    dp.register_message_handler(handle_sixth_video, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.sixth_video)
    dp.register_callback_query_handler(change_media_twelfth, state=Nomination_second.sixth_video)
    dp.register_message_handler(handle_seventh_video, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.seventh_video)
    dp.register_callback_query_handler(change_media_thirteenth, state=Nomination_second.seventh_video)
    dp.register_message_handler(handle_eighth_video, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.eighth_video)
    dp.register_callback_query_handler(change_media_fourteenth, state=Nomination_second.eighth_video)
    dp.register_message_handler(handle_ninth_video, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.ninth_video)
    dp.register_callback_query_handler(change_media_fifteenth, state=Nomination_second.ninth_video)
    dp.register_message_handler(handle_seventh_photo, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.seventh_photo)
    dp.register_callback_query_handler(change_media_sixteenth, state=Nomination_second.seventh_photo)
    dp.register_message_handler(handle_eighth_photo, content_types=['photo', 'video', 'document'],
                                state=Nomination_second.eighth_photo)
    dp.register_callback_query_handler(finish_nomination, state=Nomination_second.eighth_photo)
