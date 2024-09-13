import sqlite3

def initialize_database():
    conn = sqlite3.connect('dulieu.db')
    cursor = conn.cursor()

    # Tạo bảng nếu chưa tồn tại
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS data (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        Linhvuc NOT NULL,
        Tukhoa TEXT NOT NULL
    )
    ''')

    conn.commit()
    conn.close()

initialize_database()
