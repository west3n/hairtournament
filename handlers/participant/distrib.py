from aiogram import Dispatcher, types
from database import participants, works
from handlers.participant.first_nomination import Nomination
from handlers.participant.second_nomination import Nomination_second
from handlers.participant.third_nomination import Nomination_third


async def handle_participant_emoji(msg: types.Message):
    all_tg_ids_1 = [all_ids[0] for all_ids in await participants.all_nominations_ids("Редкие волосы")]
    all_tg_ids_2 = [all_ids[0] for all_ids in await participants.all_nominations_ids("Ровный срез")]
    all_tg_ids_3 = [all_ids[0] for all_ids in await participants.all_nominations_ids("Короткие волосы")]
    photo_path = 'media/first_example.jpg'
    user_data = await participants.get_name_by_tg_id(msg.from_id)
    with open(photo_path, 'rb') as photo:
        if msg.text == "👍" and msg.from_id in all_tg_ids_1:
            try:
                await works.add_new_work(user_data[0], "Редкие волосы")
                await msg.answer(
                    "Вы начали выполнять работу в номинации 'Редкие волосы'\nЖелаем вам победы в Чемпионате!")
                await msg.answer_photo(
                    photo=photo,
                    caption="Номинация: “Редкие волосы”\n\nЗагрузите фото №1. Для этого отправьте фото в этот чат"
                            "\n\n<b>Инструкция по съемке:</b>\nВ кадре находится модель по пояс, стоя лицом к камере."
                            "Волосы модели распущены и не убраны за уши, перекинуты вперед. В центре кадра плечевая"
                            " линия модели. Положение камеры перпендикулярно полу. Камера закреплена на штативе "
                            "или съемку производит третье лицо. Рекомендованное расстояние от камеры до модели - "
                            "до 2х метров.\n\n\nРедактировать фото запрещено❌")
                await Nomination.first_photo.set()
            except:
                await msg.answer("Вы уже загружали данные в этой номинации. Пожалуйста, ожидайте результата судейства.")
        elif msg.text == "🔥" and msg.from_id in all_tg_ids_2:
            try:
                await works.add_new_work(user_data[0], "Ровный срез")
                await msg.answer(
                    "Вы начали выполнять работу в номинации 'Ровный срез'\nЖелаем вам победы в Чемпионате!")
                await msg.answer_photo(
                    photo=photo,
                    caption="Номинация: “Ровный срез”\n\nЗагрузите фото №1. Для этого отправьте фото в этот чат"
                            "\n\n<b>Инструкция по съемке:</b>\nВ кадре находится модель по пояс, стоя лицом к камере."
                            "Волосы модели распущены и не убраны за уши, перекинуты вперед. В центре кадра плечевая"
                            " линия модели. Положение камеры перпендикулярно полу. Камера закреплена на штативе "
                            "или съемку производит третье лицо. Рекомендованное расстояние от камеры до модели - "
                            "до 2х метров.\n\n\nРедактировать фото запрещено❌")
                await Nomination_second.first_photo.set()
            except:
                await msg.answer("Вы уже загружали данные в этой номинации. Пожалуйста, ожидайте результата судейства.")
        elif msg.text == "❤️" and msg.from_id in all_tg_ids_3:
            try:
                await works.add_new_work(user_data[0], "Короткие волосы")
                await msg.answer(
                    "Вы начали выполнять работу в номинации 'Короткие волосы'\nЖелаем вам победы в Чемпионате!")
                await msg.answer_photo(
                    photo=photo,
                    caption="Номинация: “Короткие волосы”\n\nЗагрузите фото №1. Для этого отправьте фото в этот чат"
                            "\n\n<b>Инструкция по съемке:</b>\nВ кадре находится модель по пояс, стоя лицом к камере."
                            "Волосы модели распущены и не убраны за уши, перекинуты вперед. В центре кадра плечевая"
                            " линия модели. Положение камеры перпендикулярно полу. Камера закреплена на штативе "
                            "или съемку производит третье лицо. Рекомендованное расстояние от камеры до модели - "
                            "до 2х метров.\n\n\nРедактировать фото запрещено❌")
                await Nomination_third.first_photo.set()
            except:
                await msg.answer(
                    "Вы уже загружали данные в этой номинации. Пожалуйста, ожидайте результата судейства.")


def register(dp: Dispatcher):
    dp.register_message_handler(handle_participant_emoji, content_types=['text'])


