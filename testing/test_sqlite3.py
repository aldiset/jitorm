import psutil
import sqlite3

from faker import Faker
from memory_profiler import memory_usage

from ..orm.session import Session
from .models import Users, Followers, Posts, Likes, Comments

class SocialMediaTestCase:
    def __init__(self, db_name='socialmedia.db'):
        self.db_name = db_name
        self.conn = sqlite3.connect(self.db_name)
        self.cursor = self.conn.cursor()
        self.session = Session(self.conn)
        self.faker = Faker()

    def insert(self, num_records):
        for _ in range(num_records):
            email= self.faker.email()
            username= self.faker.user_name()
            text= self.faker.text(max_nb_chars=200)
            password= self.faker.password(length=30)
            image_url= self.faker.image_url()
            random_int= self.faker.random_int(min=1, max=num_records)
    
            self.session.add(Users(username=username, email=email, password=password, biography=text))
            self.session.add(Followers(user_id=random_int, follower_id=random_int))
            self.session.add(Posts(user_id=random_int, content=text, image_url=image_url))
            self.session.add(Likes(post_id=random_int, user_id=random_int))
            self.session.add(Comments(post_id=random_int, user_id=random_int, comment=text))

        self.session.commit()

    def close_connection(self):
        self.conn.close()

    def monitor_performance(self, num_records):
        total_cpu_cores = psutil.cpu_count(logical=True) 
        total_ram = psutil.virtual_memory().total / (1024 ** 3)

        process = psutil.Process()
        cpu_usage_before = process.cpu_percent(interval=None)
        
        mem_usage = memory_usage((self.insert, (num_records,)), interval=0.1)

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
