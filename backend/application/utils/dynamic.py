from datetime import datetime


def calculate_dynamic_cost(num_seats_left,total_seats,starting_price_of_ticket, show_start_time):
    if num_seats_left == 0:
        return None  # No tickets available

    show_start_time = datetime.strptime(str(show_start_time), '%Y-%m-%dT%H:%M')  # Convert the show start time string to a datetime object
    time_left = show_start_time - datetime.now()

    price_multiplier = 1.0  
    if time_left.days > 2:  # more than 2 days
        if total_seats - num_seats_left < total_seats // 2:
            price_multiplier = 1.50
        elif total_seats - num_seats_left < total_seats // 4:
            price_multiplier = 2.0
        elif total_seats - num_seats_left < total_seats // 8:
            price_multiplier = 2.0
    elif time_left.days < 2 : # less than 2 days
        if total_seats - num_seats_left > total_seats//2:
            price_multiplier = 0.25
        elif total_seats - num_seats_left < total_seats // 2:
            price_multiplier = 1.50
        elif total_seats - num_seats_left < total_seats // 4:
            price_multiplier = 1.75
        elif total_seats - num_seats_left < total_seats // 8:
            price_multiplier = 2
    elif time_left.days < 1 : #less than 1 day
        if total_seats - num_seats_left > total_seats//2:
            price_multiplier = 0.25
        elif total_seats - num_seats_left < total_seats // 2:
            price_multiplier = 1.50
        elif total_seats - num_seats_left < total_seats // 4:
            price_multiplier = 1.75
        elif total_seats - num_seats_left < total_seats // 8:
            price_multiplier = 2
    elif time_left.days == 0 and time_left.seconds <1080: # less than 3 hrs
        if total_seats - num_seats_left > total_seats//2:
            price_multiplier = 0.50
        elif total_seats - num_seats_left < total_seats // 2:
            price_multiplier = 0.75
        elif total_seats - num_seats_left < total_seats // 4:
            price_multiplier = 1.25
        elif total_seats - num_seats_left < total_seats // 8:
            price_multiplier = 1.75
    elif time_left.days == 0 and time_left.seconds <7200: # less than 2 hrs
        if total_seats - num_seats_left > total_seats//2:
            price_multiplier = 0.75
        elif total_seats - num_seats_left < total_seats // 2:
            price_multiplier = 1
        elif total_seats - num_seats_left < total_seats // 4:
            price_multiplier = 1.25
        elif total_seats - num_seats_left < total_seats // 8:
            price_multiplier = 1.75
    elif time_left.days == 0 and time_left.seconds <3600: #less than 1 hr
        if total_seats - num_seats_left > total_seats//2:
            price_multiplier = 0.5
        elif total_seats - num_seats_left < total_seats // 2:
            price_multiplier = 1.0
        elif total_seats - num_seats_left < total_seats // 4:
            price_multiplier = 1.0
        elif total_seats - num_seats_left < total_seats // 8:
            price_multiplier = 1.5
    elif time_left.days == 0 and time_left.seconds <1800: #less than 1/2 hr
        if total_seats - num_seats_left > total_seats//2:
            price_multiplier = 0.5
        elif total_seats - num_seats_left < total_seats // 2:
            price_multiplier = 0.5
        elif total_seats - num_seats_left < total_seats // 4:
            price_multiplier = 0.75
        elif total_seats - num_seats_left < total_seats // 8:
            price_multiplier = 1.0

    

    # Calculate the dynamic cost of the ticket
    dynamic_cost = starting_price_of_ticket * price_multiplier
    # last filter return cost not more than 2 times of initial price and not less than half of initial price
    return max(min(dynamic_cost,2.0*starting_price_of_ticket),max(dynamic_cost,0.5*starting_price_of_ticket))