import datetime

from database.connection import db, cur


# def create_table():
#     cur.execute(f"CREATE TABLE works ("
#                 f"id SERIAL PRIMARY KEY,"
#                 f"user_id TEXT REFERENCES users(name),"
#                 f"nomination TEXT,"
#                 f"start_datetime TEXT,"
#                 f"end_datetime TEXT NULL,"
#                 f"photo1 TEXT NULL,"
#                 f"photo2 TEXT NULL,"
#                 f"photo3 TEXT NULL,"
#                 f"photo4 TEXT NULL,"
#                 f"photo5 TEXT NULL,"
#                 f"photo6 TEXT NULL,"
#                 f"photo7 TEXT NULL,"
#                 f"photo8 TEXT NULL,"
#                 f"video1 TEXT NULL,"
#                 f"video2 TEXT NULL,"
#                 f"video3 TEXT NULL,"
#                 f"video4 TEXT NULL,"
#                 f"video5 TEXT NULL,"
#                 f"video6 TEXT NULL,"
#                 f"video7 TEXT NULL,"
#                 f"video8 TEXT NULL,"
#                 f"video9 TEXT NULL);")
#
#     db.commit()
#
# def add_unique_constraint():
#     cur.execute("CREATE UNIQUE INDEX unique_user_nomination ON works (user_id, nomination);")
#     db.commit()


async def add_new_work(name, nomination):
    start_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    cur.execute("INSERT INTO works (user_id, start_datetime, nomination) VALUES (%s, %s, %s)",
                (name, start_datetime, nomination,))
    db.commit()


async def get_work_id(name, nomination):
    cur.execute("SELECT id FROM works WHERE user_id=%s AND nomination=%s", (name, nomination,))
    result = cur.fetchone()
    return result


async def add_media(name, nomination, data, referees_list):
    end_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    cur.execute(
        f"UPDATE works SET "
        f"end_datetime = %s, "
        f"photo1 = %s, "
        f"photo2 = %s, "
        f"photo3 = %s, "
        f"photo4 = %s, "
        f"photo5 = %s, "
        f"photo6 = %s, "
        f"photo7 = %s, "
        f"photo8 = %s, "
        f"video1 = %s, "
        f"video2 = %s, "
        f"video3 = %s, "
        f"video4 = %s, "
        f"video5 = %s, "
        f"video6 = %s, "
        f"video7 = %s, "
        f"video8 = %s, "
        f"video9 = %s, "
        f"referees_list = %s "
        f"WHERE user_id = %s AND nomination = %s",
        (
            end_datetime,
            data.get('first_photo'),
            data.get('second_photo'),
            data.get('third_photo'),
            data.get('fourth_photo'),
            data.get('fifth_photo'),
            data.get('sixth_photo'),
            data.get('seventh_photo'),
            data.get('eighth_photo'),
            data.get('first_video'),
            data.get('second_video'),
            data.get('third_video'),
            data.get('fourth_video'),
            data.get('fifth_video'),
            data.get('sixth_video'),
            data.get('seventh_video'),
            data.get('eighth_video'),
            data.get('ninth_video'),
            referees_list,
            name,
            nomination,
        )
    )
    db.commit()

