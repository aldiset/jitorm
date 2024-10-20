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
            return crud.create(db=db, model=Users, data=data)
    
    def bulk_create(self, datas):
        with Session(connection) as db:
            return crud.bulk_create(db=db, model=Users, data=datas)
    
    def bulk_update(self, model, updates):
        with Session(connection) as db:
            return crud.bulk_update(db=db, model=model, updates=updates)
    
    def get_list(self):
        with Session(connection) as db:
            return crud.get_list(db=db, model=Users)
    
    def get_by_id(self, id: int):
        with Session(connection) as db:
            return crud.get_by_id(db=db, model=Users, id=id)
    
    def update(self, id:int, **data):
        with Session(connection) as db:
            return crud.update(db, Users, {"id":id}, **data)
    
    def delete(self, id: int):
        with Session(connection) as db:
            return crud.delete(db, Users, {"id":id})


if __name__=='__main__':
    test = Test()
    user = {"username":"admin"}
    test.create(user)
    test.bulk_create(users)
    
    records = test.get_list()
    for record in records:
        record.address = record.address+" updated by" if record.address else "updated by"
    test.bulk_update(Users, updates=records)
    
    test.get_by_id(id=10000)
    test.delete(id=1001)
    test.get_by_id(id=1001)