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

