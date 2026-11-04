import sqlite3
conn = sqlite3.connect("Stay_Easy.db")
cursor = conn.cursor()
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ROOMS(
        room_no INT PRIMARY KEY,
        room_type TEXT,
        floor INT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CUSTOMERS(
        Mobile TEXT PRIMARY KEY,
        Name VARCHAR(20),
        Email TEXT
    )
    """)
    conn.commit()
def insert_room(room_no, room_type, floor):
    cursor.execute(
        "INSERT OR IGNORE INTO ROOMS VALUES(?,?,?)",
        (room_no, room_type, floor)
    )
    conn.commit()
def insert_customer(mobile, name, email):
    cursor.execute(
        "INSERT INTO CUSTOMERS VALUES(?,?,?)",
        (mobile, name, email)
    )
    conn.commit()