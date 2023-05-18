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
    start_datetime = datetime.datetime.now()
    cur.execute("INSERT INTO works (user_id, start_datetime, nomination) VALUES (%s, %s, %s)",
                (name, start_datetime, nomination,))
    db.commit()


async def get_work_id(name, nomination):
    cur.execute("SELECT id FROM works WHERE user_id=%s AND nomination=%s", (name, nomination,))
    result = cur.fetchone()
    return result


def add_media(name, nomination, data):
    end_datetime = datetime.datetime.now()
    update_values = [end_datetime]
    update_fields = []
    for i in range(1, 9):
        photo_key = f'photo{i}'
        video_key = f'video{i}'

        update_fields.extend([f'photo{i}', f'video{i}'])
        update_values.extend([data.get(photo_key), data.get(video_key)])
    update_fields.append('video9')
    update_values.append(data.get('ninth_video'))
    update_fields.append('user_id')
    update_values.append(name)
    update_fields.append('nomination')
    update_values.append(nomination)
    query = f"UPDATE works SET end_datetime = %s, " + ", ".join([f"{field} = %s" for field in update_fields]) + \
            " WHERE user_id = %s AND nomination = %s"
    cur.execute(query, tuple(update_values + [name, nomination]))
    db.commit()


