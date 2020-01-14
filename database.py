import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import DEBUG
from asunabot_declative import Event, PlayerSignup, Reminder, Roster, Base

if DEBUG:
    engine = create_engine('sqlite:///asunabot.db')
else:
    engine = create_engine('sqlite:////home/ec2-user/asunabot.db')


Base.metadata.bind = engine
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)
DBSession = sessionmaker(bind=engine)
session = DBSession()