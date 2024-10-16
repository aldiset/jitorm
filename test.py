import json
import time
import psutil
import sqlite3
from memory_profiler import memory_usage

from orm.session import Session

from crud import CRUD
from models import Users, Followers, Posts, Likes, Comments

# CRUD operations class
class ORMOperations:
    def __init__(self, session):
        self.session = session

    # Create all data from the dummy JSON file
    def create_all(self, data):
        def create_operation():
            for user in data["users"]:
                record = CRUD.create(db=self.session, model=Users, data=user)
            # for follower in data["followers"]:
            #     CRUD.create(db=self.session, model=Followers, data=follower)
            # for post in data["posts"]:
            #     CRUD.create(db=self.session, model=Posts, data=post)
            # for like in data["likes"]:
            #     CRUD.create(db=self.session, model=Likes, data=like)
            # for comment in data["comments"]:
                # CRUD.create(db=self.session, model=Comments, data=comment)
        monitor_performance(create_operation, "Create all records")

    def get_all(self, model, description):
        def get_all_operation():
            records = CRUD.get_list(db=self.session, model=model)
        monitor_performance(get_all_operation, description)
    
    # Massive updates
    def massive_update(self, model, update_data, description):
        def update_operation():
            records = CRUD.get_list(db=self.session, model=model)
            for record in records:
                CRUD.update(db=self.session, model=model, filters={"id": record.id}, **update_data(record))
        monitor_performance(update_operation, description)

    # Massive deletions
    def massive_delete(self, model, description):
        def delete_operation():
            records = CRUD.get_list(db=self.session, model=model)
            for record in records:
                print(record.id)
                CRUD.delete(db=self.session, model=model, filters={"id": record.id})
        monitor_performance(delete_operation, description)

# Session setup class for flexibility across databases
class SessionSetup:
    def __init__(self, db_type, db_name=None, user=None, password=None, host=None):
        self.db_type = db_type
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host

    def setup_session(self):
        if self.db_type == "sqlite":
            conn = sqlite3.connect(self.db_name or 'socialmedia.db')
        # elif self.db_type == "postgresql":
        #     conn = psycopg2.connect(
        #         dbname=self.db_name, user=self.user, password=self.password, host=self.host
        #     )
        # elif self.db_type == "mysql":
        #     conn = mysql.connector.connect(
        #         user=self.user, password=self.password, host=self.host, database=self.db_name
        #     )
        else:
            raise ValueError("Unsupported database type")
        return Session(conn)

# Performance monitoring function
def monitor_performance(operation_func, description="Operation"):
    process = psutil.Process()
    cpu_before = process.cpu_percent(interval=None)
    mem_before = memory_usage()
    start_time = time.time()

    # Execute the operation
    operation_func()

    # Collect performance metrics
    cpu_after = process.cpu_percent(interval=None)
    mem_after = memory_usage()
    end_time = time.time()

    cpu_usage = cpu_after - cpu_before
    mem_usage = max(mem_after) - min(mem_before)
    time_taken = end_time - start_time

    # Output performance stats
    print(f"{description} - CPU usage: {cpu_usage:.2f}%")
    print(f"{description} - Memory usage: {mem_usage:.2f} MB")
    print(f"{description} - Time taken: {time_taken:.2f} seconds")

# Load dummy data from JSON file
def load_dummy_data(json_file='dummy.json'):
    with open(json_file, 'r') as f:
        return json.load(f)

# Massive testing
def run(session, data):
    orm_ops = ORMOperations(session)

    # orm_ops.create_all(data)
    
    orm_ops.get_all(Users, "GET ALL")
    # Massive updates
    # orm_ops.massive_update(Users, lambda record: {"email": f"updated_{record.email}_update"}, "Massive update users")
    # orm_ops.massive_update(Followers, lambda record: {"user_id": record.user_id + 1}, "Massive update followers")
    # orm_ops.massive_update(Posts, lambda record: {"content": f"Updated content {record.id}"}, "Massive update posts")
    # orm_ops.massive_update(Likes, lambda record: {"post_id": record.post_id + 1}, "Massive update likes")
    # orm_ops.massive_update(Comments, lambda record: {"comment": f"Updated comment {record.id}"}, "Massive update comments")
    
    # Massive deletions
    # orm_ops.massive_delete(Comments, "Massive delete comments")
    # orm_ops.massive_delete(Posts, "Massive delete posts")
    # orm_ops.massive_delete(Likes, "Massive delete likes")
    # orm_ops.massive_delete(Followers, "Massive delete followers")
    # orm_ops.massive_delete(Users, "Massive delete users")

# Main execution
if __name__ == '__main__':
    # Setup session based on database type
    db_type = "sqlite"  # Choose from: "sqlite", "postgresql", "mysql"
    session_setup = SessionSetup(db_type=db_type, db_name="users.db")
    session = session_setup.setup_session()

    # Load dummy data
    # dummy_data = load_dummy_data()

    # Run massive tests
    run(session, data={})
