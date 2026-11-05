from database import create_tables, insert_customer
from database import insert_room,Availability
from exceptions import room_Unavailable
from database import allocate_room, insert_booking,guest_history
from datetime import datetime
from models import StandardRoom, DeluxeRoom, SuiteRoom,Guest
import csv
import re
create_tables()
def validating():
    Room_Obj = []
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
                Room_Obj.append(obj)
            elif room["room_type"].lower() == "deluxe":
                obj = DeluxeRoom(room["room_no"], room["room_type"], room["floor"])
                Room_Obj.append(obj)
            elif room["room_type"].lower() == "suite":
                obj = SuiteRoom(room["room_no"], room["room_type"], room["floor"])
                Room_Obj.append(obj)
            valid_data.append(room)
            room_no.append(room["room_no"])

        for obj in Room_Obj:
            insert_room(obj.room_no,obj.room_type,obj.floor,obj.Available)

    return valid_data, Room_Obj
valid_data, room_obj = validating()
def registering():
    Number_of_customers = int(input("Enter no of customers: "))
    Guests=[]
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
            pattern = r'^[a-zA-Z0-9.]+@[a-z]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                print("Enter valid email.")
                continue
            break
        guest=Guest(guest_name,mobile_number,email)
        Guests.append(guest)
    g=Guests[0]
    insert_customer(g.mobile, g.name, g.email)
    print("Customer details inserted successfully.")
while True:
    room_type = input("Enter type of room: ").lower().strip()
    if room_type in ("standard", "deluxe", "suite"):
        count = Availability(room_type)
        print(count)
        break
    else:
        print("Enter valid room type.")
today=datetime.now().strftime("%d-%m-%Y")
def check_in():
    while True:
        check_in=input("Enter check in date in DD-MM-YYYY format:")
        if not datetime.strptime(check_in,"%d-%m-%Y"):
            print("Enter date in the given format.")
        if check_in < today:
            print("Enter check in date in future or present.")
        if (check_in-today).days>180:
            print("Check in date cannot be after 180 days.")
        else:
            break
    return check_in
def check_out():
    while True:
        check_out=input("Enter check in date in DD-MM-YYYY format:")
        if not datetime.strptime(check_out,"%d-%m-%Y"):
            print("Enter date in the given format.")
        if check_in()>check_out:
            print("Enter valid dates.")
        else:
            break
while True:
    print("""
            1.search availability
            2.create booking
            3.check in
            4.check out
            5.cancel booking
            6.view booking details
            7.guest stay history
            8.occupancy report
            9.revenue report
            10.export bookings
            11.exit
    """)
    choice=input("Enter your choice:")
 
    if choice=="1":
        Availability()
    elif choice=="2":
        registering()
    elif choice=="3":
        check_in()
    elif choice=="4":
        check_out()
    elif choice=="5":
        pass
    elif choice=="6":
        pass
    elif choice=="7":
        guest_history()
    elif choice=="8":
        pass
    elif choice=="9":
        pass
    elif choice=="10":
        pass
    elif choice=="11":
        print("Thank you!" \
              "visit again..")
        break
    else:
        print("Invalid choice")