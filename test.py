import json

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
        pass
    
    def create(self, data):
        with Session(connection) as db:
            crud.create(db=db, model=Users, data=data)
        return
    
    def bulk_create(self, datas):
        with Session(connection) as db:
            crud.bulk_create(db=db, model=Users, data=datas)
        return
    
    def bulk_update(self, model, updates):
        with Session(connection) as db:
            crud.bulk_update(db=db, model=model, updates=updates)
        return
    
    def get_list(self):
        with Session(connection) as db:
            records = crud.get_list(db=db, model=Users)
        return records
    
    def get_by_id(self, id: int):
        with Session(connection) as db:
            record = crud.get_by_id(db=db, model=Users, id=id)
            print(record)
        return record
    
    def update(self, id:int, **data):
        with Session(connection) as db:
            crud.update(db, Users, {"id":id}, **data)
        return
    
    def delete(self, id: int):
        with Session(connection) as db:
            crud.delete(db, Users, {"id":id})
        return


if __name__=='__main__':
    test = Test()
    records = test.get_list()
    print("dapat")
    updates = []
    for record in records[:100]:
        record.address = "update uhuyyyy"
    print("selesai set")
    test.bulk_update(Users, records)