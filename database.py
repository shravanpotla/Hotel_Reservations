from exceptions import room_Unavailable
import sqlite3
conn = sqlite3.connect("Stay_Easy.db")
cursor = conn.cursor()
cursor.execute("Select * from CUSTOMERS")
for i in cursor.fetchall():
    print(i)
# cursor.execute("DROP TABLE CUSTOMERS")
def create_tables():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ROOMS(
        room_no INT PRIMARY KEY,
        room_type TEXT,
        floor INT,
        Available INT
    )
    """)
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS CUSTOMERS(
        Mobile TEXT PRIMARY KEY,
        Name VARCHAR(20),
        Email TEXT,
        Visits INT
    )
    """)
    conn.commit()
def insert_room(room_no, room_type, floor,availability):
    cursor.execute(
        "INSERT OR IGNORE INTO ROOMS VALUES(?,?,?,?)",
        (room_no, room_type, floor,availability)
    )
    conn.commit()
def insert_customer(mobile, name, email):
    Existing=cursor.execute("select Mobile from CUSTOMERS where Mobile=?",(mobile,)).fetchone()
    if Existing:
        cursor.execute(
            """UPDATE CUSTOMERS SET Visits=Visits+1 WHERE Mobile=?""",(mobile,)
        )
    else:
        cursor.execute(
            "INSERT INTO CUSTOMERS VALUES(?,?,?,?)",
            (mobile, name, email,1)
        )
    conn.commit()
def Availability(type):
    cursor.execute("""
                    SELECT COUNT(room_no)
                    FROM ROOMS
                    WHERE room_type = ? AND Available = 1;""",(type.capitalize(),)
                )
    count=cursor.fetchone()[0]
    return count
def create_booking_table():
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS BOOKINGS(
        Booking_ID INTEGER PRIMARY KEY AUTOINCREMENT,
        Mobile TEXT,
        Room_No INT,
        Check_In TEXT,
        Check_Out TEXT,
        Guests INT,
        Status TEXT,
        FOREIGN KEY(Mobile) REFERENCES CUSTOMERS(Mobile),
        FOREIGN KEY(Room_No) REFERENCES ROOMS(room_no)
    )
    """)
    conn.commit()
def allocate_room(room_type, check_in, check_out):
    cursor.execute("""
        SELECT room_no
        FROM ROOMS
        WHERE LOWER(room_type) = ?
        AND NOT EXISTS (
            SELECT 1
            FROM BOOKINGS
            WHERE BOOKINGS.Room_No = ROOMS.room_no
            AND BOOKINGS.Status IN ('CONFIRMED', 'CHECKED_IN')
            AND BOOKINGS.Check_In < ?
            AND BOOKINGS.Check_Out > ?
        )
        ORDER BY room_no ASC
        LIMIT 1
    """, (room_type, check_out, check_in))

    room = cursor.fetchone()

    if room is None:
        raise room_Unavailable(f"No {room_type} rooms available for these dates.")

    return room[0]
def insert_booking(mobile, room_no, check_in, check_out, guests):
    cursor.execute("""
        INSERT INTO BOOKINGS
        (Mobile, Room_No, Check_In, Check_Out, Guests, Status)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (mobile, room_no, check_in, check_out, guests, "CONFIRMED"))
    conn.commit()
    return cursor.lastrowid