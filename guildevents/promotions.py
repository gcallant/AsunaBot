import datetime

import discord
from config import config
from asunadiscord.discord_client import client
from config.asunabot_declative import PlayerSignup, Event
from config.config import COMMUNICATION_CHANNEL_ID, INCURABLE_SERVER_ID
from config.database import session


async def check_citizen_promotions(thrall_list):
    eligible_members = list()
    two_weeks_ago = datetime.datetime.now() - datetime.timedelta(weeks=2)
    message = "Thrall Members eligible for promotion to Citizen:\n\n```"
    for member in thrall_list:
        if member.joined_at <= two_weeks_ago:
            eligible_members.append(member)
    if len(eligible_members) > 0:
        for member in eligible_members:
            message += member.name
            message += "\n"
        message += "```"
        channel = client.get_channel(COMMUNICATION_CHANNEL_ID)
        await channel.send(message)


async def check_marauder_promotions(marauder_list):
    eligible_members = list()
    message = "Citizen Members eligible for promotion to Marauder:\n\n```"
    for member in marauder_list:
        player_events = session.query(PlayerSignup).outerjoin(Event).filter(
            PlayerSignup.id == member.id and Event.event_day < datetime.datetime.now()).all()
        if len(player_events) >= 5:
            eligible_members.append(member)

    if len(eligible_members) > 0:
        for member in eligible_members:
            message += member.name
            message += "\n"
        message += "```"
        channel = client.get_channel(COMMUNICATION_CHANNEL_ID)
        await channel.send(message)


def compile_members(citizen_list, thrall_list):
    server = client.get_guild(INCURABLE_SERVER_ID)
    members = server.members
    for member in members:
        if member.top_role.name == 'Thrall' and not discord.utils.get(member.roles, name="Inactive"):
            thrall_list.append(member)
        elif member.top_role.name == 'Citizen' and not discord.utils.get(member.roles, name="Inactive"):
            citizen_list.append(member)


async def check_promotions():
    if config.have_run is True:
        return
    citizen_list = list()
    thrall_list = list()
    # It's most efficient to compile both lists at the same time, since all members have to be
    # iterated through- doing this through pass-by-reference is the cleanest way
    compile_members(citizen_list, thrall_list)
    await check_citizen_promotions(thrall_list)
    await check_marauder_promotions(citizen_list)
    config.have_run = True
