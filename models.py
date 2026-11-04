from abc import ABC,abstractmethod
class Room(ABC):
    def __init__(self,room_no,room_type,floor):
        self.room_no=room_no
        self.room_type=room_type
        self.floor=floor
    @abstractmethod
    def tariff(self):
        pass
    @abstractmethod
    def guest_charges(self):
        pass
    @abstractmethod
    def breakfast(self):
        pass
class StandardRoom(Room):
    def __init__(self,room_no,room_type,floor):
        super().__init__(room_no,room_type,floor)
        self.base_price=2500
        self.Available=True
    def tariff(self):
        return self.base_price
    def guest_charges(self):
        return 0
    def breakfast(self,count):
        return count*350
class DeluxeRoom(Room):
    def __init__(self,room_no,room_type,floor):
        super().__init__(room_no,room_type,floor)
        self.base_price=4000
        self.Available=True
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
            self.Available=True
    def tariff(self):
        return self.base_price
    def guest_charges(self,count):
        if count>2:
            return (count-2)*800
        return 0
    def breakfast(self,count):
        return 0
