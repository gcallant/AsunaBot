from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Time, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
import datetime

# Database Structure
Base = declarative_base()

class Roster(Base):
    __tablename__ = 'roster'
    id = Column(Integer, primary_key=True)
    max_tanks = Column(Integer, default=2)
    max_heal = Column(Integer, default=2)
    max_mdps = Column(Integer, default=4)
    max_rdps = Column(Integer, default=4)
    tank_list = Column(String)
    heal_list = Column(String)
    mdps_list = Column(String)
    rdps_list = Column(String)
    flex_list = Column(String)
    reserve_list = Column(String)

class Event(Base):
    __tablename__ = 'event'
    id = Column(Integer, autoincrement=True)
    channel_id = Column(String, primary_key=True, nullable=True)
    event_name = Column(String(250), nullable=False)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated = Column(DateTime, onupdate=datetime.datetime.now)
    event_time = Column(DateTime, nullable=False)
    event_day = Column(DateTime, nullable=False)
    created_by_id = Column(String(250), nullable=False)
    event_leader = Column(String(250), nullable=False)
    active = Column(Boolean, default=True)
    roster = relationship(Roster)
    roster_id = Column(Integer, ForeignKey('roster.id'), nullable=False)
    event_description = Column(String, nullable=False)
    min_rank = Column(String, nullable=False)
    channel_info_message = Column(String, nullable=True)

class PlayerSignup(Base):
    __tablename__ = 'playersignup'
    id = Column(String, primary_key=True, nullable=False)
    player_name = Column(String(250), nullable=False)
    player_mention = Column(String(250), nullable=False)
    player_roles = Column(String, nullable=False)
    event_id = Column(Integer, ForeignKey('event.channel_id'), nullable=False, primary_key=True)
    event = relationship(Event)
    date_created = Column(DateTime, default=datetime.datetime.now)
    last_updated = Column(DateTime, onupdate=datetime.datetime.now)
    flex_roles = Column(String(250), nullable=True)

class Reminder(Base):
    __tablename__ = 'reminder'
    id = Column(Integer, ForeignKey('event.channel_id'), nullable=False, primary_key=True)
    event = relationship(Event, cascade="all, delete")
    first_reminder_sent = Column(Boolean, default=False, nullable=True)
    second_reminder_sent = Column(Boolean, default=False, nullable=True)
    third_reminder_sent = Column(Boolean, default=False, nullable=True)
    fourth_reminder_sent = Column(Boolean, default=False, nullable=True)



engine = create_engine('sqlite:///asunabot.db')
Base.metadata.create_all(engine)