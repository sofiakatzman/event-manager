# Event:
#     1 - CREATE AN EVENT - add_event()
#     2 - CREATE AN EVENT STAFF SCHEDULE - create_schedule()
#     3 - EDIT AN EVENT STAFF SCHEDULE - edit_schedule()
#     4 - CLOSE OUT AN EVENT - closeout()

from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from db.models import (Event, Schedule, Position, Staff)

engine = create_engine("sqlite:///db/event_manager.db")
session = Session(engine, future=True)

def test():
    print('Entering Event Module...')

# create an event
def add_event():
    print("Creating an Event...")
    print("Please enter an Event Type:")
    new_name = str(input())
    print("Please enter an Event Description:")
    new_description = str(input())
    print("Please enter Event Date: 00")
    new_date = str(input())
    new_event = Event(type = new_name , description = new_description , date = new_date )
    session.add(new_event)
    session.commit()

# create a staff schedule 
def create_schedule():
    print("Let's create a schedule...")
    # print all events 
    print("What event would you like to create a schedule for?")
    all_active_events = session.query(Event).filter(Event.is_active == True).all()
    print(all_active_events)
    event_selection = int(input())

    print("This is the event you've selected:")
    selected_event = session.query(Event).filter(Event.id == event_selection).first()
    print(selected_event)

    # new_schedule = Schedules()

    # iterate through the positions table positions to capture how many of each type of staff you want to hire 
    positions = session.query(Position).all()
    staff_counts = {}
    for position in positions:
        print(f"How many {position.name} staff do you want to add?")
        count = int(input())
        staff_counts[position.id] = count

    # ask user to pick staff based on position -- DICTIONARY! 
    selected_staff = {}
    for position_id, count in staff_counts.items():
        staff_time = None
        if count > 0:
            staff_time = input(f"Enter the time for {next((p.name for p in positions if p.id == position_id), '')}: ")
            print(f"Select {count} staff for {next((p.name for p in positions if p.id == position_id), '')}:")
            available_staff = session.query(Staff).filter(Staff.position_id == position_id).all()
            selected_staff[position_id] = []
            if available_staff:
                for staff in available_staff:
                    print(f"{staff.id}. {staff.first_name} {staff.last_name}")
                for _ in range(count):
                    while True:
                        staff_selection = input("Enter the ID of the staff member: ")
                        if staff_selection.isdigit():
                            staff_selection = int(staff_selection)
                            if staff_selection not in [staff.id for staff_list in selected_staff.values() for staff in staff_list if staff is not None]:
                                if staff_selection in [staff.id for staff in available_staff]:
                                    break
                                else:
                                    print("Invalid staff ID. Please try again.")
                            else:
                                print("Staff member has already been selected. Please choose a different ID.")
                        else:
                            print("Invalid input. Please enter a valid staff ID.")
                    selected_staff[position_id].append(next((staff for staff in available_staff if staff.id == staff_selection), None))
            else:
                print("No staff available for this position.")
                selected_staff[position_id] = []
        else:
            selected_staff[position_id] = []

    # create a Schedule entry per staff that uses the event name, position id, staff id, time of arrival, etc.
    for position_id, staff_list in selected_staff.items():
        if staff_list:
            for staff in staff_list:
                if staff is not None:
                    arrival_time = staff_time
                    new_schedule = Schedule(
                        event_id=selected_event.id,
                        event_type=selected_event.type,
                        staff_id=staff.id,
                        position_id=position_id,
                        arrival_time=arrival_time
                        )
                session.add(new_schedule)
    session.commit()
    print("Schedule created successfully!")

# close out an event
def closeout():
    print("Let's closeout an event!")
    
    # print all active events
    active = session.query(Event).filter(Event.is_active == True).all()
    print(active)
    print("Please enter the ID of the event you would like to closeout")
    
    # find event 
    find_id = int(input())
    event = session.query(Event).filter(Event.id == find_id).first()
    print("This is the event you've selected.")
    print(event)
    
    print("Your changes have been made!")
    # make event inactive
    event[0].is_active = False
    session.commit()

# view all event history 
def view():
    print("Printing Event History...")  
    active = session.query(Event).all()
    print(active)
