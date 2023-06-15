import asyncio

from database.connection import connect
import pandas as pd


# df = pd.read_excel('C:/Users/miros/Documents/PycharmProjects/hairtournament/Участники_Чемпионата.xls')
#
#
# for index, row in df.iterrows():
#     db, cur = connect()
#     try:
#         name = row.iloc[0]
#         phone = row.iloc[1]
#         status = row.iloc[2]
#
#         cur.execute("INSERT INTO participants (name, phone, status) VALUES (%s, %s, %s)", (name, phone, status,))
#         print(name, phone, status)
#         db.commit()
#     finally:
#         db.close()
#         cur.close()


async def get_phone_numbers():
    db, cur = connect()
    try:
        cur.execute("SELECT phone FROM participants")
        result = cur.fetchall()
        return result
    finally:
        db.close()
        cur.close()


async def get_name_by_phone(phone):
    db, cur = connect()
    try:
        cur.execute("SELECT name, status FROM participants WHERE phone=%s", (phone,))
        result = cur.fetchone()
        return result
    finally:
        db.close()
        cur.close()


async def get_name_by_tg_id(tg_id):
    db, cur = connect()
    try:
        cur.execute("SELECT name, status FROM participants WHERE tg_id=%s", (tg_id,))
        result = cur.fetchone()
        return result
    finally:
        db.close()
        cur.close()


async def add_tg_id(tg_id, phone):
    db, cur = connect()
    try:
        cur.execute("UPDATE participants SET tg_id = %s WHERE phone = %s", (tg_id, phone,))
        db.commit()
    finally:
        db.close()
        cur.close()


async def add_teacher(tg_id, teacher, category):
    db, cur = connect()
    try:
        cur.execute("UPDATE participants SET teacher = %s, category = %s WHERE tg_id = %s", (teacher, category, tg_id,))
        db.commit()
    finally:
        db.close()
        cur.close()


async def check_status(tg_id):
    db, cur = connect()
    try:
        cur.execute("SELECT name FROM participants WHERE tg_id = %s", (tg_id,))
        result = cur.fetchone()
        return result
    finally:
        db.close()
        cur.close()


async def add_nomination(tg_id, new_nomination):
    db, cur = connect()
    try:
        cur.execute("SELECT nomination FROM participants WHERE tg_id = %s", (tg_id,))
        status = cur.fetchone()
        if status[0]:
            cur.execute("UPDATE participants SET nomination = %s || %s WHERE tg_id = %s", (status[0], new_nomination, tg_id,))
            db.commit()
        else:
            cur.execute("UPDATE participants SET nomination=%s WHERE tg_id = %s", (new_nomination, tg_id,))
            db.commit()
    finally:
        db.close()
        cur.close()


async def all_nominations_ids(nomination):
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id FROM participants WHERE nomination LIKE %s", ('%' + nomination + '%',))
        tg_ids = cur.fetchall()
        return tg_ids
    finally:
        db.close()
        cur.close()


async def get_all_participants_tg_id():
    db, cur = connect()
    try:
        cur.execute(
            "SELECT tg_id FROM participants WHERE status IN ('Champ2023|Econom', 'Champ2023|Premium', 'Champ2023|Vip')"
            " AND tg_id IS NOT NULL")
        results = cur.fetchall()
        return results
    finally:
        db.close()
        cur.close()


async def get_all_second_nominations_tg_id():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id FROM participants WHERE (status IN ('Champ2023|Premium', 'Champ2023|Vip') AND tg_id IS NOT NULL)"
                    " OR (status = 'Champ2023|Econom' AND nomination IS NULL AND tg_id IS NOT NULL)")
        results = cur.fetchall()
        return results
    finally:
        db.close()
        cur.close()


async def get_all_third_nominations_tg_id():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id FROM participants WHERE (status = 'Champ2023|Vip' AND tg_id IS NOT NULL) "
                    "OR (status = 'Champ2023|Econom' AND nomination IS NULL AND tg_id IS NOT NULL) "
                    "OR (status = 'Champ2023|Premium' AND (SELECT COUNT(*) FROM unnest(regexp_split_to_array"
                    "(nomination, ';')) WHERE TRIM(unnest) <> '') < 2 AND tg_id IS NOT NULL)")

        results = cur.fetchall()
        return results
    finally:
        db.close()
        cur.close()


async def get_category_from_name(name):
    db, cur = connect()
    try:
        cur.execute("SELECT category FROM participants WHERE name = %s", (name,))
        return cur.fetchone()
    finally:
        db.close()
        cur.close()
