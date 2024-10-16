from fastapi import FastAPI

from object import get_list
from test_sqlalchemy import get_all_users

app = FastAPI()

@app.get("/jitorm")
def get_by_jitorm():
    return get_list()

@app.get("/sqlalchemy")
def get_by_sqlalchemy():
    return get_all_users()

