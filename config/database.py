import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config.asunabot_declative import Base
from config.config import DEBUG

if DEBUG:
    engine = create_engine('sqlite:///asunabot.db')
else:
    engine = create_engine('sqlite:///./asunabot.db')

Base.metadata.bind = engine
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)
DBSession = sessionmaker(bind=engine)
session = DBSession()
