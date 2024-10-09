import sqlite3
from orm.session import Session
# Fungsi untuk membuat tabel-tabel di database
def create_database():
    conn = sqlite3.connect("socialmedia.db")
    session = Session(conn)
    
    # Membuat tabel Users
    session.storage.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            biography TEXT
        );
    ''')

    # Membuat tabel Followers
    session.storage.execute('''
        CREATE TABLE IF NOT EXISTS followers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            follower_id INTEGER NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (follower_id) REFERENCES users(id)
        );
    ''')

    # Membuat tabel Posts
    session.storage.execute('''
        CREATE TABLE IF NOT EXISTS posts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            content TEXT NOT NULL,
            image_url TEXT,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

    # Membuat tabel Likes
    session.storage.execute('''
        CREATE TABLE IF NOT EXISTS likes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

    # Membuat tabel Comments
    session.storage.execute('''
        CREATE TABLE IF NOT EXISTS comments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            post_id INTEGER NOT NULL,
            user_id INTEGER NOT NULL,
            comment TEXT NOT NULL,
            FOREIGN KEY (post_id) REFERENCES posts(id),
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
    ''')

    # Commit perubahan
    session.commit()

    print("Database and tables created successfully.")

if __name__ == "__main__":
    create_database()
