import psycopg2
from decouple import config

db = psycopg2.connect(
    host=config("DB_HOST"),
    database=config("DB_NAME"),
    user=config("DB_USER"),
    password=config("DB_PASS")
)

cur = db.cursor()


# def create_table():
#     cur.execute(f"CREATE TABLE users ("
#                 f"name TEXT PRIMARY KEY,"
#                 f"phone TEXT,"
#                 f"status TEXT,"
#                 f"tg_id BIGINT NULL,"
#                 f"teacher TEXT NULL,"
#                 f"nomination TEXT NULL);")
#     cur.execute(f"CREATE TABLE work ("
#                 f"id SERIAL PRIMARY KEY,"
#                 f"user_id TEXT REFERENCES users(name),"
#                 f"file TEXT,"
#                 f"nomination TEXT);")
#     db.commit()
