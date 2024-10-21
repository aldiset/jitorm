import json
import time
import psutil
import pandas as pd
from orm.session import Session
from orm.sqlite import DatabaseConnection
from crud import CRUD
from model import Users

connection = DatabaseConnection("users.db")

with open('users.json', 'r') as json_file:
    users = json.load(json_file)
    

crud = CRUD()

class Test:
    def __init__(self) -> None:
        self.results = []  # Untuk menyimpan hasil performa setiap fungsi
    
    def measure_resources(func):
        def wrapper(self, *args, **kwargs):
            # Mendapatkan proses yang sedang berjalan
            process = psutil.Process()
            
            # Mengukur penggunaan CPU dan Memori sebelum eksekusi fungsi
            cpu_before = process.cpu_percent(interval=None)
            mem_before = process.memory_info().rss
            
            # Mengukur waktu mulai
            start_time = time.time()
            
            # Eksekusi fungsi
            result = func(self, *args, **kwargs)
            
            # Mengukur waktu selesai
            end_time = time.time()
            
            # Mengukur penggunaan CPU dan Memori setelah eksekusi fungsi
            cpu_after = process.cpu_percent(interval=None)
            mem_after = process.memory_info().rss
            
            # Menghitung hasil
            cpu_usage = cpu_after - cpu_before
            mem_usage = (mem_after - mem_before) / (1024 * 1024)  # Convert to MB
            exec_time = end_time - start_time
            
            # Simpan hasil ke dalam list
            self.results.append({
                "Function": func.__name__,
                "Response Time (seconds)": exec_time,
                "CPU Usage (%)": cpu_usage,
                "Memory Usage (MB)": mem_usage
            })
            
            return result
        return wrapper
    
    @measure_resources
    def create(self, data):
        with Session(connection) as db:
            return crud.create(db=db, model=Users, data=data)
    
    @measure_resources
    def bulk_create(self, datas):
        with Session(connection) as db:
            return crud.bulk_create(db=db, model=Users, data=datas)
    
    @measure_resources
    def bulk_update(self, model, updates):
        with Session(connection) as db:
            return crud.bulk_update(db=db, model=model, updates=updates)
    
    @measure_resources
    def get_list(self):
        with Session(connection) as db:
            return crud.get_list(db=db, model=Users)
    
    @measure_resources
    def get_by_id(self, id: int):
        with Session(connection) as db:
            return crud.get_by_id(db=db, model=Users, id=id)
    
    @measure_resources
    def update(self, id:int, **data):
        with Session(connection) as db:
            return crud.update(db, Users, {"id":id}, **data)
    
    @measure_resources
    def delete(self, id: int):
        with Session(connection) as db:
            return crud.delete(db, Users, {"id":id})
    
    def show_results(self):
        # Menampilkan hasil dalam bentuk tabel menggunakan pandas
        df = pd.DataFrame(self.results)
        print(df)

if __name__=='__main__':
    test = Test()
    
    # Mengukur response time, penggunaan CPU, dan Memori untuk create
    test.create(users[1])
    
    # Mengukur response time, penggunaan CPU, dan Memori untuk bulk_create
    test.bulk_create(users)
    
    # Mengukur response time, penggunaan CPU, dan Memori untuk get_list
    records = test.get_list()
    
    # Mengukur response time, penggunaan CPU, dan Memori untuk get_by_id
    test.get_by_id(id=10000)
    
    # Mengukur response time, penggunaan CPU, dan Memori untuk delete
    test.delete(id=1001)
    
    # Menampilkan hasil dalam bentuk tabel
    test.show_results()
