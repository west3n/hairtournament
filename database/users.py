from database.connection import db, cur
import pandas as pd

# df = pd.read_excel('C:/Users/miros/Documents/PycharmProjects/hairtournament/database/Участники Чемпионата.xls')
#
#
# for index, row in df.iterrows():
#     name = row.iloc[0]
#     phone = row.iloc[1]
#     status = row.iloc[2]
#
#     cur.execute("INSERT INTO users (name, phone, status) VALUES (%s, %s, %s)", (name, phone, status,))
#     print(name, phone, status)
#     db.commit()
# def create_table():
#     cur.execute(f"CREATE TABLE users ("
#                 f"name TEXT PRIMARY KEY,"
#                 f"phone TEXT,"
#                 f"status TEXT,"
#                 f"tg_id BIGINT NULL,"
#                 f"teacher TEXT NULL,"
#                 f"nomination TEXT NULL);")
#     db.commit()

async def get_phone_numbers():
    cur.execute("SELECT phone FROM users")
    result = cur.fetchall()
    return result


async def get_name_by_phone(phone):
    cur.execute("SELECT name, status FROM users WHERE phone=%s", (phone,))
    result = cur.fetchone()
    return result


async def get_name_by_tg_id(tg_id):
    cur.execute("SELECT name, status FROM users WHERE tg_id=%s", (tg_id,))
    result = cur.fetchone()
    return result


async def add_tg_id(tg_id, phone):
    cur.execute("UPDATE users SET tg_id = %s WHERE phone = %s", (tg_id, phone,))
    db.commit()


async def add_teacher(tg_id, teacher):
    cur.execute("UPDATE users SET teacher = %s WHERE tg_id = %s", (teacher, tg_id,))
    db.commit()


async def check_status(tg_id):
    cur.execute("SELECT name FROM users WHERE tg_id = %s", (tg_id,))
    result = cur.fetchone()
    return result


async def add_nomination(tg_id, new_nomination):
    cur.execute("SELECT nomination FROM users WHERE tg_id = %s", (tg_id,))
    status = cur.fetchone()
    if status[0]:
        cur.execute("UPDATE users SET nomination = %s || %s WHERE tg_id = %s", (status[0], new_nomination, tg_id,))
        db.commit()
    else:
        cur.execute("UPDATE users SET nomination=%s WHERE tg_id = %s", (new_nomination, tg_id,))
        db.commit()


async def all_nominations_ids(nomination):
    cur.execute("SELECT tg_id FROM users WHERE nomination LIKE %s", ('%' + nomination + '%',))
    tg_ids = cur.fetchall()
    return tg_ids
