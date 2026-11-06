from abc import ABC,abstractmethod
from datetime import date,timedelta,datetime
class Room(ABC):
    def __init__(self,room_no,room_type,floor):
        self.room_no=room_no
        self.room_type=room_type
        self.floor=floor
    @abstractmethod
    def tariff(self):
        pass
    @abstractmethod
    def guest_charges(self,count):
        pass
    @abstractmethod
    def breakfast(self,count):
        pass
class StandardRoom(Room):
    def __init__(self,room_no,room_type,floor):
        super().__init__(room_no,room_type,floor)
        self.base_price=2500
        self.Available=1
        self.max_guests = 2
    def tariff(self):
        return self.base_price
    def guest_charges(self,count):
        return 0
    def breakfast(self,count):
        return count*350
class DeluxeRoom(Room):
    def __init__(self,room_no,room_type,floor):
        super().__init__(room_no,room_type,floor)
        self.base_price=4000
        self.Available=1
        self.max_guests = 3
    def tariff(self):
        return self.base_price
    def guest_charges(self,count):
        if count>2:
            return (count-2)*800
        return 0
    def breakfast(self,count):
        return 0
class SuiteRoom(Room):
    def __init__(self,room_no,room_type,floor):
            super().__init__(room_no,room_type,floor)
            self.base_price=7500
            self.Available=1
            self.max_guests = 4
    def tariff(self):
        return self.base_price
    def guest_charges(self,count):
        if count>2:
            return (count-2)*800
        return 0
    def breakfast(self,count):
        return 0
class Guest():
    def __init__(self,name,mobile,email):
        self.name=name
        self.mobile=mobile
        self.email=email
class Bookings():
    def __init__(self,guest,room,check_in,check_out,guests):
        if guests<1 or guests>room.max_guests:
            raise ValueError("No of guests are not valid.")
        nights=(check_out-check_in).days
        if nights<1 or nights>30:
            raise ValueError("Cannot stay more than 30 days or less than 1 day.")
        self.guest = guest
        self.room = room
        self.check_in_date = check_in
        self.check_out_date = check_out
        self.guests = guests
        self._status = "CONFIRMED"
        self.booking_id = None

        
    


    
    