import sqlite3
from crud import CRUD
from models import Users
from orm.session import Session

# Dependency untuk mendapatkan session per request
def get_db():
    conn = sqlite3.connect('users.db', check_same_thread=False)
    try:
        yield Session(conn)
    finally:
        conn.close()

def get_list():
    with sqlite3.connect('users.db', check_same_thread=False) as conn:
        session = Session(conn)
        records = CRUD.get_list(db=session, model=Users)
        return records
