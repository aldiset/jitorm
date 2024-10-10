import sqlite3

from faker import Faker
from memory_profiler import memory_usage

from orm.session import Session
from crud import CRUD
from generate_database import create_database
from testing.models import Users, Followers, Posts, Likes, Comments
crud = CRUD()
conn = sqlite3.connect("socialmedia.db")
session = Session(conn)
d = crud.get_by_id(db=session, model=Users, id=1)
breakpoint()
print(d.id)