import json
import psutil
import sqlite3

from faker import Faker
from memory_profiler import memory_usage

from orm.session import Session
from testing.models import Users, Followers, Posts, Likes, Comments

class SocialMediaTestCase:
    def __init__(self, db_name='socialmedia.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.session = Session(self.conn)
        self.faker = Faker()

    def load(self, json_file):
        with open(json_file, 'r') as f:
            data = json.load(f)
        return data

    def create(self, model, datas):
        for data in datas:
            self.session.add(model(**data))
        self.session.commit()
        
    def read(self, model, id):
        return self.session.query(model).filter(model.id==id).first()
    
    def update(self, model, filters, **kwargs):
        self.session.update(model, filters, **kwargs)
        self.session.commit()
    
    def delete(self, model, filters):
        self.session.delete(model, filters)

    def close_connection(self):
        self.conn.close()

    def monitor_performance(self):
        total_cpu_cores = psutil.cpu_count(logical=True) 
        total_ram = psutil.virtual_memory().total / (1024 ** 3)

        process = psutil.Process()
        cpu_usage_before = process.cpu_percent(interval=None)
        
        datas = self.load("dummy.json")
        mem_usage = memory_usage((self.create, (Users, datas["users"])), interval=0.1)

        cpu_usage_after = process.cpu_percent(interval=None)
        cpu_usage = cpu_usage_after - cpu_usage_before

        data={"ram_total": f"{total_ram:.2f}GB", "cpu_total_core": str(total_cpu_cores),
            "ram_total_usage": f"{max(mem_usage):.2f}MB", "cpu_total_usage_core": f"{cpu_usage}%"}
        print(data)
        return data

if __name__ == "__main__":
    test = SocialMediaTestCase()
    test.monitor_performance(num_records=10000)
    test.close_connection()
