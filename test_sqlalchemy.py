from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import sessionmaker
import time
import psutil
from memory_profiler import memory_usage
Base = declarative_base()

# Define a sample Users model
class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    biography = Column(String)
    is_active = Column(Boolean, default=True)

# Define a function to create the engine and session
def setup_database():
    engine = create_engine('sqlite:///users.db')  # Or use another database URI
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

# Function to get all records
def get_all_users():
    session = setup_database()
    users = session.query(Users).all()
    return users

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
    
if __name__ == "__main__":
    monitor_performance(get_all_users, "GET ALL")
