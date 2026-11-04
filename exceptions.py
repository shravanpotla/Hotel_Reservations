class StayEasy(Exception):
    pass
class room_Unavailable(StayEasy):
    pass
class invalid_data(StayEasy):
    pass
class invalid_status(StayEasy):
    pass
class Booking_not_found(StayEasy):
    pass
class InvalidDate(StayEasy):
    pass