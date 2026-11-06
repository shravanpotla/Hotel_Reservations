from datetime import datetime,timedelta
class Pricing:
    def __init__(self):
        pass
    def calculate_room_charges(self,room_type,base_rate,check_in,check_out,no_of_guests,completed_stays,breakfast=False):
        print("check_in:", check_in, type(check_in))
        print("check_out:", check_out, type(check_out))
        
        if isinstance(check_in, str):
            check_in = datetime.strptime(check_in, "%d-%m-%Y").date()

        if isinstance(check_out, str):
            check_out = datetime.strptime(check_out, "%d-%m-%Y").date()
        nights=(check_out-check_in).days
        breakfast_charges=0
        if nights<=0:
            raise ValueError("Check-out date must be after check-in date")
        if no_of_guests<1:
            raise ValueError("At least one guest is required.")
        
        if room_type=="standard" and breakfast:
            breakfast_charges=350*no_of_guests*nights
        if room_type!="standard":
            breakfast=False
        extra_guest_charges=0
        total_room_charge=0
        gst_amount=0
        current_date=check_in
        if room_type in ('deluxe','suite') and no_of_guests>2:
            extra_guest_charges=(no_of_guests-2)*800*nights
        if room_type=="standard" and breakfast:
            breakfast_charges=(no_of_guests*350)*nights
        while current_date<check_out:
            daily_rate=base_rate
            if current_date.weekday() in (4,5):
                daily_rate+=daily_rate*0.2
            total_room_charge+=daily_rate
            current_date=current_date+timedelta(days=1)
        total_room_charge+=extra_guest_charges
        total_room_charge+=breakfast_charges
        long_stay_discount=0
        loyalty_discount=0
        if nights>=7:
            long_stay_discount=total_room_charge*0.10
        if completed_stays>=3:
            loyalty_discount=total_room_charge*0.05
        total_discount=long_stay_discount+loyalty_discount
        discounted_room_charge=total_room_charge-total_discount
        if base_rate<=7500:
            gst_rate=0.12
        else:
            gst_rate=0.18
        gst_amount=discounted_room_charge*gst_rate
        final_amount=discounted_room_charge+gst_amount
        return {
            "no_of_nights":nights,
            "room_charge":total_room_charge,
            "extra_guest_charge":extra_guest_charges,
            "total_room_charge":total_room_charge,
            "long_stay_discount":long_stay_discount,
            "loyalty_discount":loyalty_discount,
            "total_discount":total_discount,
            "discounted_room_charge":discounted_room_charge,
            "gst_rate":gst_rate*100,
            "gst_amount":gst_amount,
            "final_amount":final_amount
        }
