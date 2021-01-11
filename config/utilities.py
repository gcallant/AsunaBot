import asyncio
import logging

import discord
from discord import Forbidden, NotFound, HTTPException, InvalidArgument
from config import config
from asunadiscord.discord_client import client
from resourcestrings import easter_egg_messages, exception_messages


async def disappearing_message(message, time_to_wait=20):
    """
    Waits specified amount of seconds (default 20), then makes specified message "disappear" (deletes it)

    :param message: The message to delete
    :param time_to_wait: The time to wait before deleting the specified message
    """
    await asyncio.sleep(time_to_wait)
    try:
        await message.delete()
    except Forbidden as fb:
        logging.debug(f'Tried to delete message, but it was likely a DM {fb}')
    except:
        logging.info('Attempted to delete a message, but it was not found- it was probably already deleted.')


async def get_menu_option_in_range(menu, author, first_option, last_option):
    while True:
        message: str = await ask_user(menu, author)
        if message.isdigit() and first_option <= int(message) <= last_option:
            return int(message)
        else:
            await send_message_to_user(author, exception_messages.incorrect_menu_option_exception)


async def check_permissions(context):
    """
    Checks if a user can perform an action for a given group

    :param context: The context of the current function
    :return: The author if permissions match lowest officer rank, otherwise None
    :raises KeyError: If user has a rank not in the roles dictionary
    """

    def officer(author: discord.user) -> bool:
        lowest_officer_rank = 'Aesir'
        try:
            if config.DISCORD_ROLES_RANKED[author.top_role.name] > config.DISCORD_ROLES_RANKED[lowest_officer_rank]:
                return False
            else:
                return True
        except KeyError as Key:
            logging.exception(f'Unknown rank {Key} tried to perform admin function')
            return False

    try:
        if not (context.message.author.guild_permissions.administrator or officer(context.message.author)):
            await send_message_to_user(context.message.author, exception_messages.missing_permission_exception)
            await disappearing_message(context.message, time_to_wait=5)
        else:
            return context.message.author
    except AttributeError as error:
        await send_message_to_user(context.message.author, exception_messages.operation_not_permitted_in_dm_exception)


async def ask_user(question, author):
    await send_message_to_user(author, question)
    msg = await client.wait_for('message', check=lambda message: message.author == author and message.channel.type
                                                                 is discord.ChannelType.private, timeout=300)
    data = msg.content.strip()
    # This allows you to cancel creating or editing an event
    if data == '?cec' or data == '?cancel':
        raise InterruptedError
    # Allows for returning to a previous edit menu
    elif data == '?return':
        raise UserWarning
    return data


async def send_message_to_user(user, message, file=None):
    try:
        if file is not None:
            await user.send(message, file=file)
        else:
            await user.send(message)
    except Forbidden as forbiddenError:
        logging.error(f'{user}, blocked Asuna \n{forbiddenError}')
    except NotFound as nfError:
        logging.error(f'{user} was not found.\n{nfError}')
    except HTTPException as httpError:
        logging.error(f'Global problem sending message to {user}\n{httpError}')
    except InvalidArgument as iaError:
        logging.error(f'Some kind of invalid argument error sending message to {user}\n{iaError}')
    except:
        logging.exception(f'More Bullshit from some dipshit {user}')


async def ask_user_checked(message, author, function, format, exception_message):
    valid = False
    while not valid:
        try:
            raw_data = await ask_user(message, author)
            data = function(raw_data, format)
            return data
        except ValueError:
            await send_message_to_user(author, exception_message)


async def echo(message):
    author = message.author
    if author.id != config.AERIANA_ID:
        await send_message_to_user(author, easter_egg_messages.default)
        return
    config.is_toy = True
    try:
        channel = await ask_user("What's the channel id?", author)
        message = await ask_user("What's the message?", author)
    except InterruptedError:
        await send_message_to_user(author, easter_egg_messages.end_toy)
        config.is_toy = False
        return

    channel = client.get_channel(int(channel))
    await channel.send(message)
    config.is_toy = False


async def get_highest_discord_role(player_id, context):
    member = context.message.guild.get_member(player_id)
    try:
        return member.top_role
    except:
        logging.exception(f'Could not get a member from that player id, they might have left the server.')
        return "Follower"
