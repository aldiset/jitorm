import json
import psutil
import sqlite3

from faker import Faker
from memory_profiler import memory_usage

from orm.session import Session
from crud import CRUD
from generate_database import create_database
from testing.models import Users, Followers, Posts, Likes, Comments

crud = CRUD()
class SocialMediaTestCase:
    def __init__(self, db_name='socialmedia.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.session = Session(self.conn)
        self.faker = Faker()

    def load(self, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data
    
    def create(self, x, records: list):
        for record in records:
            crud.create(db=self.session, model=Users, data=record)
    def get_list(self):
        return crud.get_list(db=self.session, model=Users)

    def monitor_performance(self):
        records = crud.get_list(db=self.session, model=Users)
        print(records)
        

if __name__ == "__main__":
    test = SocialMediaTestCase()
    test.monitor_performance()