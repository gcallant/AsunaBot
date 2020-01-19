# Constants
import asyncio
import logging

import discord
from discord.abc import PrivateChannel

from config import config
from config.asunabot_declative import Event
from config.database import session
from asunadiscord.discord_client import client, SIGNUP_LOG_CHANNEL_ID
from config.utilities import disappearing_message, echo, send_message_to_user
from guildevents.easter_eggs import process_easter_egg
from guildevents.promotions import check_promotions
from guildevents.reminders import check_reminders
from resourcestrings import non_descript_messages, exception_messages


@client.event
async def on_guild_channel_delete(channel):
    existing_event = session.query(Event).get(channel.id)
    if existing_event:
        existing_event.active = False
        try:
            session.commit()
        except:
            session.rollback()
            aeriana = client.get_user(config.AERIANA_ID)
            aeriana.send(f'Had a problem deactivating deleted channel {channel.name} to DB')
            logging.exception(f'Problem committing channel deactivation with channel {channel.name}')
            return

        channel = client.get_channel(SIGNUP_LOG_CHANNEL_ID)
        await channel.send(non_descript_messages.channel_deleted,
                           f' {channel.name}.', delete_after=30)


@client.event
async def on_message(message):
    if message.content.lower().startswith("? x"):
        await message.channel.send(f"{message.author.mention} {exception_messages.no_space_in_signup_exception}", delete_after=10)
        await disappearing_message(message)
        return
    elif message.content.startswith("?"):
        await client.process_commands(message)
        return
    if isinstance(message.channel, PrivateChannel):
        author = message.author
        # we do not want the bot to reply to itself
        if message.author == client.user:
            return
        if message.content == "echo":
            await echo(message)
            return
        if not (config.is_creation_event or config.is_editing or config.is_toy):
            lowercase = message.content.upper().lower()
            await process_easter_egg(author, lowercase)


@client.event
async def on_member_join(member):
    roles = member.guild.roles
    role = discord.utils.get(roles, name="Follower")
    await member.add_roles(role, reason=non_descript_messages.role_assign_reason)
    await send_message_to_user(member, non_descript_messages.member_join_welcome)


@client.event
async def on_ready():
    while not client.is_closed():
        print("Current servers:")
        await check_reminders()
        await check_promotions()
        for server in client.guilds:
            print(server.name)
        print('------')
        await asyncio.sleep(300)


def init():
    pass
