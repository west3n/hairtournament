from database.connection import cur, db
#
# def create_table_grades():
#     cur.execute("""
#         CREATE TABLE grades (
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
#             advice TEXT,
#             FOREIGN KEY (work_id) REFERENCES works (id),
#             FOREIGN KEY (referee) REFERENCES users (name),
#             CONSTRAINT unique_work_referee UNIQUE (work_id, referee)
#         );
#     """)
#     db.commit()

import psycopg2


def add_grades(data):
    sql = """
        INSERT INTO grades (
            work_id,
            referee,
            grade_1,
            grade_2,
            grade_3,
            grade_4,
            grade_5,
            grade_6,
            grade_7,
            grade_8,
            grade_9,
            grade_10,
            grade_11,
            grade_12,
            grade_13,
            grade_14,
            grade_15,
            grade_16,
            grade_17,
            penalty,
            advice
        )
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    values = (
        int(data.get('work')),
        int(data.get('referee')),
        int(data.get('grades1')),
        int(data.get('grades2')),
        int(data.get('grades3')),
        int(data.get('grades4')),
        int(data.get('grades5')),
        int(data.get('grades6')),
        int(data.get('grades7')),
        int(data.get('grades8')),
        int(data.get('grades9')),
        int(data.get('grades10')),
        int(data.get('grades11')),
        int(data.get('grades12')),
        int(data.get('grades13')),
        int(data.get('grades14')),
        int(data.get('grades15')),
        int(data.get('grades16')),
        int(data.get('grades17')),
        int(data.get('penalty')),
        data.get('advice')
    )

    cur.execute(sql, values)
    db.commit()
