from database.connection import cur, db



# def create_table_grades():
#     cur.execute("""
#         CREATE TABLE grades (
#             id SERIAL PRIMARY KEY,
#             work_id INT,
#             referee TEXT,
#             grade_1 INT,
#             grade_2 INT,
#             grade_3 INT,
#             grade_4 INT,
#             grade_5 INT,
#             grade_6 INT,
#             grade_7 INT,
#             grade_8 INT,
#             grade_9 INT,
#             grade_10 INT,
#             grade_11 INT,
#             grade_12 INT,
#             grade_13 INT,
#             grade_14 INT,
#             grade_15 INT,
#             grade_16 INT,
#             grade_17 INT,
#             penalty INT,
#             advice TEXT
#         );
#     """)
#     db.commit()


def add_grades(data):
    cur.execute("INSERT INTO grades (work_id, referee, grade_1, grade_2, grade_3, grade_4, grade_5, grade_6, grade_7,"
                "grade_8, grade_9, grade_10, grade_11, grade_12, grade_13, grade_14, grade_15, grade_16, grade_17,"
                "penalty, advice) VALUES "
                "(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (int(data.get('work')), (data.get('referee')), int(data.get('grades1')), int(data.get('grades2')),
                 int(data.get('grades3')), int(data.get('grades4')), int(data.get('grades5')), int(data.get('grades6')),
                 int(data.get('grades7')), int(data.get('grades8')), int(data.get('grades9')),
                 int(data.get('grades10')), int(data.get('grades11')), int(data.get('grades12')),
                 int(data.get('grades13')), int(data.get('grades14')), int(data.get('grades15')),
                 int(data.get('grades16')), int(data.get('grades17')), int(data.get('penalty')), data.get('advice')),)
    db.commit()


async def get_all_grades_by_id_and_referee(work, referee):
    cur.execute("SELECT * FROM grades WHERE work_id=%s AND referee=%s", (work, referee))
    return cur.fetchone()
