import datetime

import discord

from config import config, database
from guildevents import event_creation


async def test_non_admin_cannot_create_event():
    config.init()
    session = database.session
    await event_creation.save_event_details(2, 2, 2, 2, "me", "test", "f", 3, datetime.datetime.now().day, 2000, "me", "s", "Follower")
