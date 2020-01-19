import asyncio
import datetime
import logging

import discord
from discord import InvalidArgument, HTTPException

from asunadiscord.discord_client import client, SERVER_ID
from config import config
from resourcestrings import exception_messages, event_creation_messages
from config.asunabot_declative import Event, Roster
from config.database import session
from config.utilities import ask_user, ask_user_checked, send_message_to_user, disappearing_message
from guildevents.event_utilities import validate_min_rank, get_event_details


async def perform_event_creation(context, author, delete_message_after):
    event_day, event_description, event_leader, event_name, event_rank, event_time, event_trial_name, \
    number_of_heals, number_of_mdps, number_of_rdps, number_of_tanks \
    = await get_event_info_from_user(author, context, delete_message_after)

    success, new_channel = await create_event_channel(author, event_name)
    if not success:
        return

    success = await save_event_details(number_of_tanks, number_of_heals, number_of_mdps, number_of_rdps,
                                       author, event_name, event_trial_name, new_channel, event_day, event_time,
                                       event_leader, event_description, event_rank)
    if not success:
        return

    event_channel_message = f"""@everyone
Date: {str(event_day).split()[0]}
Time: {str(event_time).split()[1]} Central
{event_description}

Raid Leader:{event_leader} 


{await get_event_details(new_channel.id, context)}

Minimum Rank: {event_rank}
If you are not this rank, you may still signup, but you will be listed as reserve."""

    channel_info_message = await new_channel.send(event_channel_message)

    event = session.query(Event).get(new_channel.id)
    event.channel_info_message = channel_info_message.id

    try:
        session.commit()
    except:
        session.rollback()
        await send_message_to_user(author, f'There was an error saving the event to the database, let Aeriana know!')
        logging.exception(f'There was an error saving {event_name} to the database')
        config.is_creation_event = False
        return

    config.is_creation_event = False


async def save_event_details(number_of_tanks, number_of_heals, number_of_mdps, number_of_rdps,
                             author, event_name, event_trial_name, new_channel, event_day, event_time,
                             event_leader, event_description, event_rank):
    new_roster = Roster(
        max_tanks=number_of_tanks,
        max_heal=number_of_heals,
        max_mdps=number_of_mdps,
        max_rdps=number_of_rdps
    )

    new_event = Event(
        event_name=event_name,
        trial_name=event_trial_name,
        channel_id=new_channel.id,
        event_day=event_day,
        event_time=event_time,
        event_leader=event_leader,
        created_by_id=author.id,
        roster=new_roster,
        event_description=event_description,
        min_rank=event_rank
    )

    # These two tables have a foreign key constraint, commit as one transaction, or rollback operation
    try:
        session.add(new_roster)
        session.commit()
        session.add(new_event)
        session.commit()
        return True
    except:
        session.rollback()
        await send_message_to_user(author, exception_messages.creation_database_commit_exception)
        logging.exception(f'There was an error saving {event_name} to the database')
        config.is_creation_event = False
        return False


async def create_event_channel(author, event_name):
    server = client.get_guild(SERVER_ID)
    new_channel = discord.TextChannel

    try:
        categories = server.categories
        category = discord.utils.get(categories, name='Raid Sign Ups & Events')
        new_channel = await server.create_text_channel(name=event_name, category=category, position=0)
    except InvalidArgument:
        await send_message_to_user(author, 'Could not create the event, the overwrite information was not correct!')
        logging.info(f'Had a problem creating channel with event {event_name}, by author {author.name}- overwrite '
                     f'information incorrect')
        config.is_creation_event = False
        return False
    except HTTPException as http_exception:
        await send_message_to_user(author, f'Could not create event, there was an error {http_exception}, let Aeriana '
                                           f'know!')
        logging.exception(f'There wan an error creating event {event_name}, '
                          f'by {author.name}, details are {http_exception}')
        config.is_creation_event = False
        return False
    except:
        await send_message_to_user(author, f'Could not create event, there was an unknown error, let Aeriana '
                                           f'know!')
        logging.exception(f'There was an unknown error when attempting to create event {event_name}')
        config.is_creation_event = False
        return False

    await send_message_to_user(author, 'Created new channel for event with name: ' + event_name)
    return True, new_channel


async def get_event_info_from_user(author, context, delete_message_after):
    try:
        config.is_creation_event = True
        event_name = await ask_user(event_creation_messages.event_name, author)

        event_day = await ask_user_checked(message=event_creation_messages.event_day, author=author,
                                           function=datetime.datetime.strptime, format="%m/%d/%Y",
                                           exception_message=exception_messages.creation_event_day_exception)

        event_time = await ask_user_checked(event_creation_messages.event_time,
                                            author, datetime.datetime.strptime, "%H%M",
                                            exception_messages.creation_event_time_exception)
        # Adding Event Trial Name
        event_trial_name = await ask_user(event_creation_messages.event_trials, author)
        event_leader = await ask_user(event_creation_messages.event_leader, author)
        number_of_tanks = await ask_user(event_creation_messages.event_tanks, author)
        number_of_heals = await ask_user(event_creation_messages.event_healers, author)
        number_of_mdps = await ask_user(event_creation_messages.event_melee, author)
        number_of_rdps = await ask_user(event_creation_messages.event_ranged, author)
        event_description = await ask_user(event_creation_messages.event_description, author)
        event_rank = await ask_user_checked(event_creation_messages.event_rank,
                                            author, validate_min_rank, None,
                                            exception_messages.creation_rank_exception)
    except InterruptedError:
        await send_message_to_user(author, exception_messages.creation_canceled_exception)
        logging.info(f'Event creation was canceled by {author} {datetime.datetime.now()}')
        config.is_creation_event = False
        return
    except asyncio.TimeoutError:
        logging.info(f'We timed out waiting for {author.name}')
        await send_message_to_user(author, exception_messages.creation_timeout_exception)
        config.is_creation_event = False
        return
    finally:
        await disappearing_message(context.message, delete_message_after)
    return event_day, event_description, event_leader, event_name, event_rank, event_time, event_trial_name, \
           number_of_heals, number_of_mdps, number_of_rdps, number_of_tanks
