from database import create_tables, insert_customer, create_booking_table,check_in_data,check_in_update,check_out_data,check_out_update
from database import insert_room,Availability,cancel_booking,Number_of_visits
from pricing import Pricing
from exceptions import room_Unavailable
from database import allocate_room, insert_booking,guest_history
from datetime import datetime
from reports import ReportService
report_service = ReportService()
from models import StandardRoom, DeluxeRoom, SuiteRoom,Guest,Bookings
import csv
import re
create_tables()
create_booking_table()
today=datetime.now().date()
limit={'standard':2,'deluxe':3,'suite':4}
def check_dates(room_type):
    while True:
        while True:
            check_in_date = input("Enter Check-in date (DD-MM-YYYY): ")
            try:
                check_in_date = datetime.strptime(check_in_date, "%d-%m-%Y").date()
                break
            except ValueError:
                print("Invalid date format. Enter DD-MM-YYYY.")
        while True:
            check_out_date = input("Enter Check-out date (DD-MM-YYYY): ")
            try:
                check_out_date = datetime.strptime(check_out_date, "%d-%m-%Y").date()
                break
            except ValueError:
                print("Invalid date format. Enter DD-MM-YYYY.")
        if check_in_date<today:
            print("Check_in must be after present day.")
            continue
        if (check_in_date-today).days>180:
            print("Check in date cannot be after 180 days.")
            continue
        total_stay=(check_out_date-check_in_date).days
        if 1>total_stay or total_stay>30:
            print("Guests can only book for 30 days.")
            continue
        return check_in_date, check_out_date
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
            elif room["room_type"].lower() == "deluxe":
                obj = DeluxeRoom(room["room_no"], room["room_type"], room["floor"])
            elif room["room_type"].lower() == "suite":
                obj = SuiteRoom(room["room_no"], room["room_type"], room["floor"])
            Room_Obj.append(obj)
            valid_data.append(room)
            room_no.append(room["room_no"])

        for obj in Room_Obj:
            insert_room(obj.room_no,obj.room_type,obj.floor,obj.Available)

    return valid_data, Room_Obj
valid_data, room_obj = validating()
def search_availability():
    while True:
        room_type = input("Enter room type (Standard/Deluxe/Suite): ").strip().lower()
        if room_type in limit:
            break
        print("Enter a valid room type.")
    dates = check_dates(room_type)
    if dates is None:
        return
    check_in, check_out = dates
    count = Availability(room_type, check_in, check_out )
    print("Available rooms:", count)
    if count == 0:
        print("No rooms available for the selected dates.")
def registering(Number_of_customers):
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
            pattern = r'^[a-zA-Z0-9]+@[a-z]+\.[a-zA-Z]{2,}$'
            if not re.match(pattern, email):
                print("Enter valid email.")
                continue
            break
        guest=Guest(guest_name,mobile_number,email)
        Guests.append(guest)
    g=Guests[0]
    insert_customer(g.mobile, g.name, g.email)
    print("Customer details registered successfully.")
    return g
today=datetime.now().date()
def check_in(booking_id):
    status=check_in_data(booking_id)
    if not status:
        print("No bookings for this mobile number.")
        return
    if status[0]!="CONFIRMED":
        print("Please book rooms for confirmation.")
        return
    check_in_update(booking_id)
def check_out(booking_id):
    status=check_out_data(booking_id)
    if not status:
        print("No bookings for this booking id.")
        return
    if status[0]!="CHECKED-IN":
        print("Please book rooms for confirmation.")
        return
    check_out_update(booking_id)
def booking():
    while True:
        room_type=input("Enter room type:").lower()
        if room_type not in ("standard","deluxe","suite"):
            print("Enter valid room type.")
        else:
            break
    dates=check_dates(room_type)
    if dates is None:
        return
    check_in_date,check_out_date=dates
    while True:
        try:
            guests=int(input("Enter number of guests:"))
            if guests<1:
                print("Atleast one guest is required.")
                continue
            if guests>limit[room_type]:
                print("Room limit exceeded.")
                continue
            break
        except ValueError:
            print("Enter valid whole number.")
   
    count=Availability(room_type,check_in_date,check_out_date)
    if count==0:
        print("The rooms in room_type that you searched are not present.")
        for type,Max_limit in limit.items():
            if type!=room_type and Max_limit>=guests:
                limits=Availability(type,check_in_date,check_out_date)
                if limits>0:
                    print(limits)
        return None
    try:
        registered_guest=registering(1)
        room_no=allocate_room(room_type,check_in_date,check_out_date)
    except room_Unavailable as error:
        print(error)
    except ValueError as error:
        print(error)
    return (room_no, check_in_date, check_out_date, room_type, guests, registered_guest.mobile)
def cancel_bookings():
    booking_id=int(input("Enter booking id:"))
    status=check_in_data(booking_id)
    if not status:
        print("status cannot be None.")
        return
    if status[0]!="CONFIRMED":
        print("Cannot cancel after check-in or check-out.")
        return
    Status="CANCEL"
    cancel_booking(Status)
def booking_details(booking_id_no,room_number,checkin_date,checkout_date):
    print("Booking Id:",booking_id_no)
    print("Room Number:",room_number)
    print("Check In Date:",checkin_date)
    print("Check Out Date:",checkout_date)
def occupancy_report():
    try:
        checkin=input("Enter start date (DD-MM-YYYY):")
        checkout=input("Enter end date date (DD-MM-YYYY)")
        report_service.occupancy_report(valid_data,checkin,checkout)
    except ValueError:
        print("Invalid date format use DD-MM-YYYY")
    except Exception as error:
        print(error)
       
def revenue_report():
    report_service.revenue_report()
def export_data(booking_id):
    filename=f"{booking_id}.txt"
    with open(filename,"w") as file:
        file.write()
while True:
    print("""
            1.search availability
            2.Registering
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
        search_availability()
    elif choice=="2":
        result=booking()
        if result is not None:
            room_number,checkin_date,checkout_date,room_type,guests,mobile=result
            print("Check-in:", checkin_date, type(checkin_date))
            print("Check-out:", checkout_date, type(checkout_date))
            completed_stays=Number_of_visits(mobile)
            want_breakfast=False
            if room_type=="standard":
                base_rate=2000
                breakfast=input("Enter yes for breakfast or no:").lower()
                if breakfast=="yes":
                    want_breakfast=True
        elif room_type=="deluxe":
            base_rate=4000
        else:
            base_rate=7500
        pricing=Pricing()
        bill=pricing.calculate_room_charges(room_type,base_rate,checkin_date,checkout_date,guests,completed_stays,want_breakfast)
        print(bill)
        last_id = insert_booking(mobile, room_number, checkin_date, checkout_date, guests,room_type,bill["final_amount"])

        booking_id = f"BK{last_id:04d}"
        print("Booking successful!")
        print("Booking ID:", booking_id)
    elif choice=="3":
        booking_id=input("Enter booking id:")
        check_in(booking_id)
    elif choice=="4":
        booking_id=input("Enter booking id:")
        check_out(booking_id)
    elif choice=="5":
        cancel_bookings()
    elif choice=="6":
        booking_details(booking_id,room_number,checkin_date,checkout_date)
    elif choice=="7":
        mobile=input("Enter the mobile number that user registered with:")
        guest_history(mobile)
    elif choice=="8":
        occupancy_report()
    elif choice=="9":
        revenue_report()
    elif choice=="10":
        pass
    elif choice=="11":
        print("Thank you!" \
              "visit again..")
        break
    else:
        print("Invalid choice")