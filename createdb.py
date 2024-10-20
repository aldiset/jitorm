import sqlite3

# Membuat koneksi ke database SQLite
# Jika file database tidak ada, SQLite akan membuatkan file baru
conn = sqlite3.connect('users.db')

# Membuat cursor untuk mengeksekusi perintah SQL
cursor = conn.cursor()

# Membuat tabel 'kw' dengan kolom-kolom yang sesuai
# Misalnya tabel kw memiliki id, keyword, dan deskripsi
cursor.execute('''
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT,
    name TEXT,
    address TEXT,
    email TEXT,
    job TEXT,
    birthdate TEXT,
    phone_number TEXT
)
''')

# Commit perubahan dan menutup koneksi
conn.commit()
conn.close()

print("Database dan tabel 'kw' berhasil dibuat.")
