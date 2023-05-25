import asyncio

from database.connection import db, cur
import pandas as pd


# df = pd.read_excel('C:/Users/miros/Documents/PycharmProjects/hairtournament/database/Судьи Чемпионата.xlsx')
#
#
# for index, row in df.iterrows():
#     name = row.iloc[1]
#     phone = row.iloc[2]
#     status = row.iloc[3]
#     panel = row.iloc[4]
#
#     cur.execute("INSERT INTO referees (name, phone, status, panel) VALUES (%s, %s, %s, %s)", (name, phone, status, panel))
#     print(name, phone, status, panel)
#     db.commit()


async def get_phone_numbers():
    cur.execute("SELECT phone FROM referees")
    result = cur.fetchall()
    return result


async def get_all_tg_ids():
    cur.execute("SELECT tg_id FROM referees WHERE tg_id IS NOT NULL")
    result = cur.fetchall()
    return result


async def get_name_by_phone(phone):
    cur.execute("SELECT name, status, panel, panel_list FROM referees WHERE phone=%s", (phone,))
    result = cur.fetchone()
    return result


async def get_name_by_tg_id(tg_id):
    cur.execute("SELECT name, status FROM referees WHERE tg_id=%s", (tg_id,))
    result = cur.fetchone()
    return result


async def get_all_panel_referees(panel):
    cur.execute("SELECT name FROM referees WHERE panel=%s", (panel,))
    result = cur.fetchall()
    return result


async def add_tg_id(tg_id, phone):
    cur.execute("UPDATE referees SET tg_id = %s WHERE phone = %s", (tg_id, phone,))
    db.commit()


async def check_status(tg_id):
    cur.execute("SELECT name FROM referees WHERE tg_id = %s", (tg_id,))
    result = cur.fetchone()
    return result


async def select_all_referees_for_exact_participant(tg_id):
    cur.execute("SELECT teacher FROM participants WHERE tg_id=%s", (tg_id,))
    teachers = cur.fetchone()
    if teachers[0]:
        teachers_list = teachers[0].strip('{}').split(',')
        teachers_list = [teacher.strip('"') for teacher in teachers_list]
        cur.execute("SELECT panel FROM referees WHERE name IN %s", (tuple(teachers_list),))
        panels = cur.fetchall()
        panel_list = [panel[0] for panel in panels]
        cur.execute("SELECT name FROM referees WHERE panel NOT IN %s OR panel IS NULL", (tuple(panel_list),))
        names = cur.fetchall()
        names_list = [name[0] for name in names]
        return names_list
    else:
        referee_status = ['Судья', 'Главная судья']
        cur.execute("SELECT name FROM referees WHERE status IN %s", (tuple(referee_status),))
        names = cur.fetchall()
        names_list = [name[0] for name in names]
        return names_list


async def get_panel_from_name(name):
    cur.execute("SELECT panel FROM referees WHERE name=%s", (name,))
    panel = cur.fetchone()[0]
    cur.execute("SELECT name FROM referees WHERE panel=%s AND status=%s", (panel, "Судья"))
    result = cur.fetchall()
    return result
