import sqlite3
from exceptions import room_Unavailable
conn = sqlite3.connect("Stay_Easy.db")
conn.execute("PRAGMA foreign_keys = ON")
cursor = conn.cursor()
# cursor.execute("DROP TABLE BOOKINGS")
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
        Room_Type TEXT,
        Final_Amount INT,
        FOREIGN KEY(Mobile) REFERENCES CUSTOMERS(Mobile),
        FOREIGN KEY(Room_No) REFERENCES ROOMS(room_no)
    )
    """)
    conn.commit()
def insert_room(room_no, room_type, floor, availability):
    cursor.execute(
        "INSERT OR IGNORE INTO ROOMS VALUES(?,?,?,?)",
        (int(room_no), room_type.capitalize(), int(floor), availability)
    )
    conn.commit()
def insert_customer(mobile, name, email):
    existing = cursor.execute(
        "SELECT Mobile FROM CUSTOMERS WHERE Mobile=?", (mobile,)
    ).fetchone()

    if existing:
        cursor.execute(
            "UPDATE CUSTOMERS SET Name=?, Email=? WHERE Mobile=?",
            (name, email, mobile)
        )
    else:
        cursor.execute(
            "INSERT INTO CUSTOMERS VALUES(?,?,?,?)",
            (mobile, name, email, 0)
        )
    conn.commit()
def Availability(room_type, check_in=None, check_out=None):
    if check_in is None or check_out is None:
        cursor.execute("""
            SELECT COUNT(room_no)
            FROM ROOMS
            WHERE LOWER(room_type)=LOWER(?) AND Available=1
        """, (room_type,))
    else:
        cursor.execute("""
            SELECT COUNT(room_no) 
            FROM ROOMS 
            WHERE LOWER(ROOMS.room_type)=LOWER(?)
            AND Available=1
            AND NOT EXISTS(
                SELECT 1 
                FROM BOOKINGS
                WHERE (ROOMS.room_no)=(BOOKINGS.Room_No)
                AND BOOKINGS.Status IN("CHECKED_IN","CONFIRMED")
                AND Check_In<?
                AND Check_Out>?)
        """, (room_type, check_out, check_in))
    return cursor.fetchone()[0]
def allocate_room(room_type, check_in, check_out):
    cursor.execute("""
        SELECT room_no
        FROM ROOMS
        WHERE LOWER(room_type)=LOWER(?)
        AND Available=1
        AND NOT EXISTS (
            SELECT 1
            FROM BOOKINGS
            WHERE BOOKINGS.Room_No=ROOMS.room_no
            AND BOOKINGS.Status IN ('CONFIRMED', 'CHECKED_IN')
            AND BOOKINGS.Check_In < ?
            AND BOOKINGS.Check_Out > ?
        )
        ORDER BY room_no
        LIMIT 1
    """, (room_type, check_out, check_in))
    room = cursor.fetchone()
    if room is None:
        raise room_Unavailable(
            f"No {room_type} rooms available for these dates."
        )
    return room[0]
def insert_booking(mobile, room_no, check_in, check_out, guests,room_type,final_amount):
    try:
        cursor.execute("""
            INSERT INTO BOOKINGS
            (Mobile, Room_No, Check_In, Check_Out, Guests, Status,Room_Type,Final_Amount)
            VALUES (?, ?, ?, ?, ?, 'CONFIRMED',?,?)
        """, (mobile, room_no, check_in, check_out, guests,room_type,final_amount))
        
        conn.commit()
 
        return cursor.lastrowid
    except Exception:
        conn.rollback()
        raise
def guest_history(mobile):
    cursor.execute("""
        SELECT Booking_ID, Room_No, Check_In, Check_Out, Guests, Status
        FROM BOOKINGS
        WHERE Mobile=?
        ORDER BY Booking_ID
    """, (mobile,))
    records = cursor.fetchall()
    if not records:
        print("No booking history found.")
    else:
        for record in records:
            print(record)
def check_in_data(booking_id):
    cursor.execute(
        """SELECT Status from BOOKINGS WHERE Booking_id=?""",
        (booking_id,)
    )
    status=cursor.fetchone()
    return status
def check_in_update(booking_id):
    cursor.execute(
        """UPDATE BOOKINGS SET Status=? Where Booking_id=?""",("CHECKED_IN",booking_id)
    )
    conn.commit()
    if cursor.rowcount == 0:
        print("Invalid Booking ID.")
    else:
        print("Check-in successful!")
def check_out_data(booking_id):
    cursor.execute(
            """SELECT Status from BOOKINGS WHERE Booking_id=?""",
            (booking_id,)
        )
    status=cursor.fetchone()
    return status
def check_out_update(booking_id):
    cursor.execute(
            """UPDATE BOOKINGS SET Status=? Where Booking_id=?""",("CHECKED_OUT",booking_id)
        )
    conn.commit()
    if cursor.rowcount == 0:
        print("Invalid Booking ID.")
    else:
        print("Check-out successful!")
def get_booking_details(booking_id):
    cursor.execute(
        """SELECT Check_In, Final_Amount, Status
        FROM BOOKINGS
        WHERE Booking_ID=?""",
        (booking_id,)
    )
    return cursor.fetchone()
def cancel_booking(booking_id):
    cursor.execute(
        """UPDATE BOOKINGS
        SET Status=?
        WHERE Booking_ID=? AND Status=?""",
        ("CANCELLED", booking_id, "CONFIRMED")
    )
    conn.commit()
    return cursor.rowcount
def Number_of_visits(mobile):
    cursor.execute(
        """SELECT Visits FROM CUSTOMERS WHERE Mobile=?""",(mobile,)
    )
    visits=cursor.fetchone()
    return visits[0]
def close_connection():
    conn.close()
