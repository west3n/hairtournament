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




async def get_phone_numbers():
    cur.execute("SELECT phone FROM users")
    result = cur.fetchall()
    return result


async def get_name_by_phone(phone):
    cur.execute("SELECT name, status FROM users WHERE phone=%s", (phone,))
    result = cur.fetchone()
    return result


async def add_tg_id(tg_id, phone):
    cur.execute("UPDATE users SET tg_id = %s WHERE phone = %s", (tg_id, phone,))
    db.commit()

async def add_teacher(tg_id, teacher):
    cur.execute("UPDATE users SET teacher = %s WHERE tg_id = %s", (teacher, tg_id,))
    db.commit()