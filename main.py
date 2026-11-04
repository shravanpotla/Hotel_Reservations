from database import create_tables, insert_customer
from database import insert_room
from models import StandardRoom, DeluxeRoom, SuiteRoom
import csv
import re
create_tables()
def validating():
    Standard_Obj = []
    DeluxeRoom_Obj = []
    SuiteRoom_Obj = []
    rooms = []
    room_no = []
    valid_data = []
    with open("rooms.csv", "r", newline="") as file, open("app.log", "w") as app:
        data = csv.DictReader(file)
        for row in data:
            rooms.append(row)
        for room in rooms:
            if room["room_type"].lower() not in ("standard", "deluxe", "suite"):
                app.write(f"{room}, Invalid room type.\n")
                continue
            if room["room_no"] == "":
                app.write(f"{room}, Room number cannot be empty.\n")
                continue
            if not room["room_no"].isdigit():
                app.write(f"{room}, Room number must be an integer.\n")
                continue
            if room["room_no"] in room_no:
                app.write(f"{room}, Duplicate room number.\n")
                continue
            if not room["floor"].isdigit():
                app.write(f"{room}, Invalid floor.\n")
                continue
            if room["room_type"].lower() == "standard":
                obj = StandardRoom(room["room_no"], room["room_type"], room["floor"])
                Standard_Obj.append(obj)
            elif room["room_type"].lower() == "deluxe":
                obj = DeluxeRoom(room["room_no"], room["room_type"], room["floor"])
                DeluxeRoom_Obj.append(obj)
            elif room["room_type"].lower() == "suite":
                obj = SuiteRoom(room["room_no"], room["room_type"], room["floor"])
                SuiteRoom_Obj.append(obj)
            valid_data.append(room)
            room_no.append(room["room_no"])
            insert_room(
                int(room["room_no"]),
                room["room_type"],
                int(room["floor"])
            )

    return valid_data, Standard_Obj, DeluxeRoom_Obj, SuiteRoom_Obj
valid_data, sta_obj, d_obj, sui_obj = validating()
Number_of_customers = int(input("Enter no of customers: "))
for _ in range(Number_of_customers):
    while True:
        guest_name = input("Enter guest name: ")
        if guest_name.strip() == "":
            print("Name cannot be empty.")
            continue
        break
    while True:
        mobile_number = input("Enter mobile number: ")
        if (len(mobile_number) != 10 or mobile_number[0] not in "6789"):
            print("Enter valid mobile number.")
            continue
        break
    while True:
        email = input("Enter email: ")
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(pattern, email):
            print("Enter valid email.")
            continue
        break
    insert_customer(mobile_number, guest_name, email)
print("Customer details inserted successfully.")