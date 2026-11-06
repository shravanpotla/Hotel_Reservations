import sqlite3
from datetime import datetime,timedelta
class ReportService():
    def occupancy_report(self,rooms,checkin,checkout):
       
        total_rooms=len(rooms)
        checkin=datetime.strptime(checkin,"%d-%m-%Y").date()
        checkout=datetime.strptime(checkout,"%d-%m-%Y").date()
        total_percentage=0
        days=0
        connection=sqlite3.connect("Stay_Easy.db")
        cursor=connection.cursor()
        while checkin<checkout:
            date=checkin.isoformat()
            cursor.execute("""
                        SELECT COUNT(DISTINCT Room_No)
                        FROM BOOKINGS WHERE Check_In <=?
                        AND Check_Out>?
                        AND Status IN('CONFIRMED','CHECKED-IN','CHECKED_IN')
                        """,(date,date))
            result=cursor.fetchone()
            occupied_rooms=result[0]
            percentage=(occupied_rooms/total_rooms)*100
            print("Date:",date)
            print("Total Rooms:",total_rooms)
            print("Occupied Rooms:",occupied_rooms)
            print("Occupied Percentage:",round(percentage,2),"%")
            print("-"*30)
           
            total_percentage+=percentage
            days+=1
            checkin+=timedelta(days=1)
        connection.close()
        if days>0:
            average=total_percentage/days
            print("Average Ocuupancy:",round(average,2),"%")
    def revenue_report(self):
        connection=sqlite3.connect("Stay_Easy.db")
        cursor=connection.cursor()
 
        room_types=["standard","deluxe","suite"]
 
        for room_type in room_types:
            cursor.execute("""
                SELECT COUNT(*), SUM(Final_Amount)
                FROM BOOKINGS
                WHERE Room_Type = ?
                AND Status IN ('CHECKED-OUT','CHECKED_OUT')
            """, (room_type,))
            result = cursor.fetchone()
            completed_stays=result[0]
            revenue =result[1]
 
            if revenue==None:
                revenue=0
 
            print("-" * 20)
            print("Room type:",room_type)
            print("Completed stays:",completed_stays)
            print("Revenue:",revenue)
 
        connection.close()