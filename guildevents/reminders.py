import datetime
import logging

from sqlalchemy import text

from config.asunabot_declative import Event, Reminder, PlayerSignup
from config.database import session
from asunadiscord.discord_client import client
from config.utilities import send_message_to_user


async def check_reminders():
    events = get_events_to_remind()

    for event in events:
        time_range = get_event_reminder_time_range(event)
        if time_range < 0 or time_range > 3:
            continue
        event_id = event.channel_id
        if not was_reminder_sent(time_range, event_id) or None:
            await send_reminder(time_range, event)


def get_events_to_remind():
    time_in_two_days = datetime.datetime.now() + datetime.timedelta(hours=48)
    events = session.query(Event).filter(Event.active == True) \
        .filter(time_in_two_days >= Event.event_day).all()
    return events


def default_message(event, player, time):
    return f"""こんにちは {player.player_name},

This is a friendly {time} reminder that you signed up for the event:

```{event.event_name}
on {str(event.event_day).split()[0]}
at {str(event.event_time).split()[1]}CST
You signed up as a: {player.player_roles}```

For more information, please refer to the <#{event.channel_id}> channel.
If you cannot attend the event, or wish to cancel, please use the command ?cancel in the <#{event.channel_id}> channel."""


def imminent_message(event, player):
    return f"""こんにち, {player.player_name}, your event {event.event_name} starts in less than 15 minutes!
Please get logged in on your character as a {player.player_roles} and x-up in chat in the next 5 minutes.
Please ensure your inventory is clear and you have all appropriate gear, food, and potions needed for the run. We will be starting shortly!"""


def get_message_for_time_interval(reminder, event, player):
    if reminder == 0:
        return default_message(event, player, "48 hour")
    elif reminder == 1:
        return default_message(event, player, "24 hour")
    elif reminder == 2:
        return default_message(event, player, "2 hour")
    elif reminder == 3:
        return imminent_message(event, player)
    else:
        logging.warning(f"Received an invalid reminder number {reminder} for event {event.event_name}")


async def mark_reminder_sent(reminder_interval, event_id):
    new_reminder = session.query(Reminder).filter(Reminder.id == event_id).one_or_none()

    if reminder_interval == 0:
        if new_reminder is None:
            new_reminder = Reminder(id=event_id, first_reminder_sent=True, second_reminder_sent=False,
                                    third_reminder_sent=False, fourth_reminder_sent=False)
        session.add(new_reminder)
        session.commit()
    elif reminder_interval == 1:
        if new_reminder is None:
            new_reminder = Reminder(id=event_id, first_reminder_sent=False, second_reminder_sent=True,
                                    third_reminder_sent=False, fourth_reminder_sent=False)
            session.add(new_reminder)
        else:
            new_reminder.second_reminder_sent = True
        session.commit()
    elif reminder_interval == 2:
        if new_reminder is None:
            new_reminder = Reminder(id=event_id, first_reminder_sent=False, second_reminder_sent=False,
                                    third_reminder_sent=True, fourth_reminder_sent=False)
            session.add(new_reminder)
        else:
            new_reminder.third_reminder_sent = True
        session.commit()
    elif reminder_interval == 3:
        if new_reminder is None:
            new_reminder = Reminder(id=event_id, first_reminder_sent=False, second_reminder_sent=False,
                                    third_reminder_sent=False, fourth_reminder_sent=True)
            session.add(new_reminder)
        else:
            new_reminder.fourth_reminder_sent = True
        session.commit()


async def send_reminder(reminder, event):
    players = session.query(PlayerSignup).filter(PlayerSignup.event_id == event.channel_id)

    for player in players:
        user = client.get_user(int(player.id))
        await send_message_to_user(user, get_message_for_time_interval(reminder, event, player))

    await mark_reminder_sent(reminder, event.channel_id)


def get_column_from_number(reminder):
    if reminder == 0:
        return "first_reminder_sent"
    elif reminder == 1:
        return "second_reminder_sent"
    elif reminder == 2:
        return "third_reminder_sent"
    elif reminder == 3:
        return "fourth_reminder_sent"


def was_reminder_sent(reminder_number, event_id):
    reminder = session.query(Reminder).filter(Reminder.id == event_id).filter(
        text(get_column_from_number(reminder_number))).one_or_none()
    return reminder


def get_event_reminder_time_range(event):
    event_day = str(event.event_day).split()[0]
    event_time = str(event.event_time).split()[1]
    date_string = event_day + event_time
    event_date = datetime.datetime.strptime(date_string, "%Y-%m-%d%H:%M:%S")
    time_in_two_days = datetime.datetime.now() + datetime.timedelta(hours=48)
    time_in_one_day = datetime.datetime.now() + datetime.timedelta(hours=24)
    time_in_two_hours = datetime.datetime.now() + datetime.timedelta(hours=2)
    time_in_fifteen_minutes = datetime.datetime.now() + datetime.timedelta(minutes=15)
    now = datetime.datetime.now()

    if time_in_two_days >= event_date > time_in_one_day:
        return 0
    elif time_in_one_day >= event_date > time_in_two_hours:
        return 1
    elif time_in_two_hours >= event_date > time_in_fifteen_minutes:
        return 2
    elif time_in_fifteen_minutes >= event_date > now:
        return 3
    else:
        return 4
