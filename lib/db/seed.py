from faker import Faker
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from datetime import date
import random

from models import (Users, Events, Positions, Tips, Schedules)

fake = Faker()

engine = create_engine("sqlite:///event_manager.db")
session = Session(engine, future=True)

# clear data when session runs
session.query(Users).delete()
session.query(Positions).delete()
session.query(Events).delete()
session.query(Tips).delete()
session.query(Schedules).delete()

positions_list = {
    0 : "Standby",
    1 : "Waitress" , 
    2 : "Bartender",
    3 : "Busser",
    4 : "Hostess",
    5 : "Administration"
    }

# generate users seeded data
users = []
for i in range(30):
    user = Users(
        first_name=f'{fake.first_name()}',
        last_name=f'{fake.last_name()}',
        position_id=random.randint(0, 5)
    )
    users.append(user)


# generate position data
positions = []
for position_id, position_name in positions_list.items():
    position = Positions(
        id=position_id,
        name=position_name
    )
    positions.append(position)

# generate event data
#=> NO EVENT DATA FOR NOW ** 

event_types = {"Art Gallery Opening" : "Art Gallery Opening for P&W" ,
                "Private Event" : "Private Event for Sir Elton John",
                "Music Show" : "Music Event at The Edge",
                "Talent Showcase" : "Talent Showcase at Sony Hall", 
                "Music Festival" : "CircoLoco Music Festival"}
events = []

# self, type, description, date
start_date = date(2022, 1, 1)
end_date = date(2023, 6, 1)
for event_type, event_description in event_types.items():
    event = Events(
        type = f'{event_type}',
        description = f'{event_description}',
        date = f'{fake.date_between_dates(date_start=start_date, date_end=end_date)}'
    )
    events.append(event)

# Generate schedule data

# Generate tip data

# Seed data
print("Seeding data...")

# Add all data to the session
session.add_all(users)
session.add_all(positions)
session.add_all(events)

session.commit()