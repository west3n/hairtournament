import datetime

from database.connection import connect


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
    db, cur = connect()
    try:
        start_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        cur.execute("INSERT INTO works (user_id, start_datetime, nomination) VALUES (%s, %s, %s)",
                    (name, start_datetime, nomination,))
        db.commit()
    finally:
        db.close()
        cur.close()


async def get_work_id(name, nomination):
    db, cur = connect()
    try:
        cur.execute("SELECT id FROM works WHERE user_id=%s AND nomination=%s", (name, nomination,))
        result = cur.fetchone()
        return result
    finally:
        db.close()
        cur.close()


async def add_media(name, nomination, data, referees_list, panel):
    db, cur = connect()
    try:
        end_datetime = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
        cur.execute(f"UPDATE works SET end_datetime = %s, photo1 = %s, photo2 = %s, photo3 = %s, photo4 = %s, "
                    f"photo5 = %s, photo6 = %s, photo7 = %s, photo8 = %s, video1 = %s, video2 = %s, "
                    f"video3 = %s, video4 = %s, video5 = %s, video6 = %s, video7 = %s, video8 = %s, video9 = %s, "
                    f"referees_list = %s, panel = %s WHERE user_id = %s AND nomination = %s RETURNING id",
                    (end_datetime, data.get('first_photo'), data.get('second_photo'), data.get('third_photo'),
                     data.get('fourth_photo'), data.get('fifth_photo'), data.get('sixth_photo'),
                     data.get('seventh_photo'), data.get('eighth_photo'), data.get('first_video'),
                     data.get('second_video'), data.get('third_video'), data.get('fourth_video'),
                     data.get('fifth_video'), data.get('sixth_video'), data.get('seventh_video'),
                     data.get('eighth_video'), data.get('ninth_video'), referees_list, panel, name, nomination,))
        db.commit()
        return cur.fetchone()
    finally:
        db.close()
        cur.close()


def get_works_by_referee(nomination, referee_name):
    db, cur = connect()
    try:
        cur.execute("SELECT id FROM works WHERE "
                    "nomination = %s AND %s = ANY(referees_list::text[])", (nomination, referee_name,))
        result = cur.fetchall()
        return result
    finally:
        db.close()
        cur.close()


def delete_referee_from_list(work_id, referee_name):
    db, cur = connect()
    try:
        cur.execute("UPDATE works SET referees_list = array_remove(referees_list, %s::text) "
                    "WHERE id = %s", (referee_name, work_id))
        db.commit()
    finally:
        db.close()
        cur.close()


async def get_all_works_by_id(_id):
    db, cur = connect()
    try:
        cur.execute("SELECT * FROM works WHERE id=%s", (_id,))
        return cur.fetchone()
    finally:
        db.close()
        cur.close()
