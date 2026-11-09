# Stay Easy – Hotel Reservation System

## Project Overview

**Stay Easy** is a Python-based Hotel Reservation System developed using Object-Oriented Programming (OOP), SQLite database management, and CSV file handling.

The application allows users to search for room availability, register guests, make reservations, calculate booking charges, manage check-in/check-out operations, and generate hotel reports.

## Technologies Used

- **Programming Language:** Python
- **Database:** SQLite
- **File Handling:** CSV and TXT
- **Concepts:** Object-Oriented Programming, Abstract Classes, Inheritance, Exception Handling, SQL Queries, Regular Expressions

## Project Structure

```text
Hotel_Reservation/
│
├── main.py
├── database.py
├── models.py
├── exceptions.py
├── pricing.py
├── reports.py
│
├── rooms.csv
├── Stay_Easy.db
├── app.log
│
└── invoices/
    └── Booking invoices
```

## Features

### 1. Room Management
- Supports Standard, Deluxe, and Suite rooms.
- Loads room details from a CSV file.
- Validates room information.
- Prevents duplicate room numbers.

### 2. Room Availability
- Search rooms based on room type.
- Check room availability for selected dates.
- Prevent overlapping confirmed bookings.

### 3. Guest Registration
- Register guest details.
- Validate mobile numbers.
- Validate email addresses.
- Store customer information in SQLite.

### 4. Booking Management
- Book rooms based on availability.
- Validate check-in and check-out dates.
- Apply room-specific guest limits.
- Generate unique booking IDs.
- Store booking information in the database.

### 5. Pricing and Billing
- Calculate room charges based on room type.
- Apply weekend pricing.
- Calculate additional guest charges.
- Provide breakfast charges for Standard rooms.
- Apply long-stay discounts.
- Apply loyalty discounts.
- Calculate GST.
- Generate the final booking amount.

### 6. Check-in and Check-out
- Check in customers using their booking ID.
- Update booking status.
- Check out customers.
- Maintain booking status in the database.

### 7. Booking Cancellation
- Cancel confirmed bookings.
- Prevent cancellation after check-in or check-out.

### 8. Reports
- Generate daily occupancy reports.
- Calculate average occupancy.
- Generate revenue reports based on room types.
- Calculate completed stays and revenue.

### 9. Invoice Generation
- Export booking details into individual TXT files.
- Include guest details, room information, stay duration, and pricing breakdown.

## Room Pricing

| Room Type | Base Price | Maximum Guests |
|---|---:|---:|
| Standard | ₹2,500 | 2 |
| Deluxe | ₹4,000 | 3 |
| Suite | ₹7,500 | 4 |

### Additional Pricing Rules

- Weekend surcharge: 20%.
- Extra guest charge: ₹800 per night.
- Standard room breakfast: ₹350 per guest per night.
- Long-stay discount: 10% for stays of 7 nights or more.
- Loyalty discount: 5% for customers with at least 3 completed stays.
- GST: Calculated based on the room's base rate.

## Database Tables

The application uses SQLite with the following tables:

### ROOMS
Stores room number, room type, floor, and availability.

### CUSTOMERS
Stores customer mobile number, name, email, and number of visits.

### BOOKINGS
Stores booking ID, customer details, room number, check-in date, check-out date, guest count, booking status, room type, and final amount.

## Installation and Execution

### Prerequisites
- Python 3.x
- SQLite3

### Step 1: Clone or Download the Project

Download the project and open the `Hotel_Reservation` folder.

### Step 2: Check Project Files

Ensure that all Python files and `rooms.csv` are available in the project directory.

### Step 3: Run the Application

Open a terminal inside the project folder and execute:

```bash
python main.py
```

The application initializes the database tables and loads room information from the CSV file.

**Note:** Create an `invoices` directory before exporting booking invoices.

## Application Menu

The application provides the following operations:

1. Search Availability
2. Registering / Booking
3. Check-in
4. Check-out
5. Cancel Booking
6. View Booking Details
7. Guest Stay History
8. Occupancy Report
9. Revenue Report
10. Export Bookings
11. Exit

## Concepts Demonstrated

- Object-Oriented Programming
- Abstraction and Inheritance
- Polymorphism
- Custom Exception Handling
- SQLite Database Connectivity
- SQL Subqueries and Joins
- CSV File Processing
- Input Validation
- Regular Expressions
- Dynamic Pricing and Billing
- Report Generation

## Conclusion

Stay Easy demonstrates the development of a hotel reservation application by integrating Python programming, OOP principles, database management, file handling, validation, and business logic into a single system.