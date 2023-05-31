import asyncio

from database.connection import connect
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
#     cur.execute("INSERT INTO referees (name, phone, status, panel)
#     VALUES (%s, %s, %s, %s)", (name, phone, status, panel))
#     print(name, phone, status, panel)
#     db.commit()


async def get_phone_numbers():
    db, cur = connect()
    try:
        cur.execute("SELECT phone FROM referees")
        result = cur.fetchall()
        return result
    finally:
        db.close()
        cur.close()


async def get_all_tg_ids():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id FROM referees WHERE tg_id IS NOT NULL")
        result = cur.fetchall()
        return result
    finally:
        db.close()
        cur.close()


async def get_name_by_phone(phone):
    db, cur = connect()
    try:
        cur.execute("SELECT name, status, panel, panel_list FROM referees WHERE phone=%s", (phone,))
        result = cur.fetchone()
        return result
    finally:
        db.close()
        cur.close()


async def get_name_by_tg_id(tg_id):
    db, cur = connect()
    try:
        cur.execute("SELECT name, status FROM referees WHERE tg_id=%s", (tg_id,))
        result = cur.fetchone()
        return result
    finally:
        db.close()
        cur.close()


async def get_all_panel_referees(panel):
    db, cur = connect()
    try:
        cur.execute("SELECT name FROM referees WHERE panel=%s", (panel,))
        result = cur.fetchall()
        return result
    finally:
        db.close()
        cur.close()


async def add_tg_id(tg_id, phone):
    db, cur = connect()
    try:
        cur.execute("UPDATE referees SET tg_id = %s WHERE phone = %s", (tg_id, phone,))
        db.commit()
    finally:
        db.close()
        cur.close()


async def check_status(tg_id):
    db, cur = connect()
    try:
        cur.execute("SELECT name FROM referees WHERE tg_id = %s", (tg_id,))
        result = cur.fetchone()
        return result
    finally:
        db.close()
        cur.close()


async def select_all_referees_for_exact_participant(tg_id):
    db, cur = connect()
    try:
        panel_list = ['1 коллегия', '2 коллегия', '3 коллегия', '4 коллегия', '5 коллегия', '6 коллегия', '7 коллегия']
        cur.execute("SELECT teacher FROM participants WHERE tg_id=%s", (tg_id,))
        teachers = cur.fetchone()
        if teachers[0]:
            teachers_list = teachers[0].replace('"', '').strip('{}').split(", ")
            cur.execute("SELECT panel FROM referees WHERE name IN %s ORDER BY panel", (tuple(teachers_list),))
            panels = cur.fetchall()
            panel = [panel[0] for panel in panels]
            result_list = [item for item in panel_list if item not in panel]
        else:
            result_list = panel_list
        len_result = []
        for result in result_list:
            cur.execute("SELECT COUNT(*) FROM works WHERE collegium=%s AND nomination=%s", (result, "Ровный срез",))
            x = cur.fetchone()
            if x:
                len_result.append(int(x[0]))
            else:
                len_result.append(0)
        result_dict = dict(zip(result_list, len_result))
        count = 0
        y = None
        while count <= max(len_result):
            for x in len_result:
                if x == count:
                    y = next((key for key, value in result_dict.items() if value == x), None)
                    break
            if y is not None:
                break
            count += 1
        cur.execute("SELECT name FROM referees WHERE panel=%s", (y,))
        referee_list = [referee[0] for referee in cur.fetchall()]
        print(y, referee_list)
        return y, referee_list
    finally:
        db.close()
        cur.close()


async def get_panel_from_name(name):
    cur.execute("SELECT panel FROM referees WHERE name=%s", (name,))
    panel = cur.fetchone()[0]
    cur.execute("SELECT name FROM referees WHERE panel=%s AND status=%s", (panel, "Судья"))
    result = cur.fetchall()
    return result


async def get_all_head_referees():
    db, cur = connect()
    try:
        cur.execute("SELECT tg_id FROM referees WHERE status=%s", ("Главная судья",))
        return [tg_id[0] for tg_id in cur.fetchall()]
    finally:
        db.close()
        cur.close()

