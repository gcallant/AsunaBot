import asyncio
import datetime
import logging

from discord import HTTPException

from asunadiscord.discord_client import client
from config import config
from config.asunabot_declative import Event, Roster
from config.database import session
from config.utilities import disappearing_message, get_menu_option_in_range, send_message_to_user, ask_user, \
    ask_user_checked
from guildevents.event_utilities import update_channel_info_message, validate_min_rank
from resourcestrings import edit_event_messages, exception_messages


async def perform_event_edit(author, context, delete_message_after, message):
    channel = context.message.channel
    event_id = channel.id
    event = session.query(Event).get(event_id)

    if event:
        try:
            roster = session.query(Roster).get(event.roster_id)
            config.is_editing = True
            await edit_selector_menu(author, event, roster)
        except asyncio.TimeoutError:
            await send_message_to_user(author, exception_messages.edit_event_timeout_exception)
        except InterruptedError:
            await send_message_to_user(author, edit_event_messages.cancel_edit)
        except:
            logging.info(f"There was an error editing {event.event_name}")
            aeriana = client.get_user(config.AERIANA_ID)
            await send_message_to_user(aeriana, f"{author} had a problem editing {event.event_name}!")
        finally:
            config.is_editing = False
            try:
                await update_channel_info_message(event_id, context)
            except HTTPException:
                await send_message_to_user(author, exception_messages.edit_event_description_too_long_exception)
    else:
        await channel.send(message.author.mention + exception_messages.no_event_for_channel_exception,
                           delete_after=10)
        await disappearing_message(message, delete_message_after)


async def save_event(author, event):
    channel = None
    try:
        session.commit()
        channel = client.get_channel(event.channel_id)
    except:
        session.rollback()
        logging.exception(f'There was an error trying to edit event {"unknown" if channel is None else channel.name}')
        channel.send(author.mention + exception_messages.saving_event_edit_exception,
                     delete_after=10)


async def edit_selector_menu(author, event, roster):
    while True:
        selection = await get_menu_option_in_range(edit_event_messages.menu, author, first_option=1, last_option=12)

        try:
            if selection == 1:
                await edit_event_name(author, event)
            elif selection == 2:
                await edit_event_date(author, event)
            elif selection == 3:
                await edit_event_time(author, event)
            elif selection == 4:
                await edit_event_trials(author, event)
            elif selection == 5:
                await edit_event_leader(author, event)
            elif selection == 6:
                await edit_event_tanks(author, event, roster)
            elif selection == 7:
                await edit_event_healers(author, event, roster)
            elif selection == 8:
                await edit_event_mdps(author, event, roster)
            elif selection == 9:
                await edit_event_rdps(author, event, roster)
            elif selection == 10:
                await edit_event_description(author, event)
            elif selection == 11:
                await edit_event_rank(author, event)
            else:
                await send_message_to_user(author, edit_event_messages.goodbye)
                break
        except UserWarning:
            await edit_selector_menu(author, event, roster)


async def update_channel_name(name, channel_id, author):
    channel = client.get_channel(channel_id)
    try:
        await channel.edit(name=name, reason=f"{author.name} is updating the event name.")
    except HTTPException:
        logging.exception(f"Error when trying to update channel name for channel {channel.name}")


async def edit_event_date(author, event):
    date = await ask_user_checked(message=edit_event_messages.date, author=author,
                                  function=datetime.datetime.strptime, format="%m/%d/%Y",
                                  exception_message=exception_messages.creation_event_day_exception)
    old_date = str(event.event_day).split()[0]
    event.event_day = date
    await save_event(author, event)
    await send_message_to_user(author, edit_event_messages.event_time_edited
                               + f" {old_date} updated to {str(date).split()[0]}.")


async def edit_event_name(author, event: Event):
    name = await ask_user(edit_event_messages.name + f" The current event name is {event.event_name}", author)
    old_name = event.event_name
    event.event_name = name
    await save_event(author, event)
    await update_channel_name(name, channel_id=int(event.channel_id), author=author)
    await send_message_to_user(author, edit_event_messages.event_name_edited + f" {old_name} updated to {name}.")


async def edit_event_time(author, event):
    time = await ask_user_checked(edit_event_messages.time,
                                  author, datetime.datetime.strptime, "%H%M",
                                  exception_messages.creation_event_time_exception)
    old_time = str(event.event_time).split()[1]
    event.event_time = time
    await save_event(author, event)
    await send_message_to_user(author,
                               edit_event_messages.event_time_edited + f" {old_time} updated to {str(time).split()[1]}.")


async def edit_event_trials(author, event):
    trials = await ask_user(edit_event_messages.trials + f" The current trials are {event.trial_name}", author)
    old_trial = event.trial_name
    event.trial_name = trials
    await save_event(author, event)
    await send_message_to_user(author, edit_event_messages.event_name_edited + f" {old_trial} updated to {trials}.")


async def edit_event_leader(author, event):
    leader = await ask_user(edit_event_messages.leader + f" The current leader is {event.event_leader}", author)
    old_leader = event.event_leader
    event.event_leader = leader
    await save_event(author, event)
    await send_message_to_user(author, edit_event_messages.event_leader_edited + f" {old_leader} updated to {leader}.")


async def edit_event_tanks(author, event, roster):
    tanks = await ask_user(edit_event_messages.tanks + f" The current max number of tanks is {roster.max_tanks}",
                           author)
    old_tanks = roster.max_tanks
    roster.max_tanks = tanks
    await save_event(author, event)
    await send_message_to_user(author, edit_event_messages.event_tanks_edited + f" {old_tanks} updated to {tanks}.")


async def edit_event_healers(author, event, roster):
    healers = await ask_user(edit_event_messages.healers + f" The current max number of healers is {roster.max_heal}",
                             author)
    old_healers = roster.max_heal
    roster.max_heal = healers
    await save_event(author, event)
    await send_message_to_user(author,
                               edit_event_messages.event_healers_edited + f" {old_healers} updated to {healers}.")


async def edit_event_rank(author, event):
    rank = await ask_user_checked(edit_event_messages.rank,
                                  author, validate_min_rank, None,
                                  exception_messages.creation_rank_exception)
    old_rank = event.min_rank
    event.min_rank = rank
    await save_event(author, event)
    await send_message_to_user(author, edit_event_messages.event_rank_edited + f" {old_rank} updated to {rank}.")


async def edit_event_mdps(author, event, roster):
    mdps = await ask_user(edit_event_messages.mdps + f" The current max number of mdps is {roster.max_mdps}", author)
    old_mdps = roster.max_mdps
    roster.max_mdps = mdps
    await save_event(author, event)
    await send_message_to_user(author, edit_event_messages.event_mdps_edited + f" {old_mdps} updated to {mdps}.")


async def edit_event_rdps(author, event, roster):
    rdps = await ask_user(edit_event_messages.rdps + f" The current max number of rdps is {roster.max_rdps}", author)
    old_rdps = roster.max_rdps
    roster.max_rdps = rdps
    await save_event(author, event)
    await send_message_to_user(author, edit_event_messages.event_rdps_edited + f" {old_rdps} updated to {rdps}.")


async def edit_event_description(author, event):
    description = await ask_user(edit_event_messages.description + f"\nThe current description is:```{event.event_description}```", author)
    old_description = event.event_description
    event.event_description = description
    await save_event(author, event)
    await send_message_to_user(author, edit_event_messages.event_description_edited + f"\nOld:```{old_description}```")
    await send_message_to_user(author, f"Was updated to:```{description}```")
