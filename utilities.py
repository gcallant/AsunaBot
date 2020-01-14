import asyncio
import logging

import discord
from discord import Forbidden, NotFound, HTTPException, InvalidArgument

from asunabot import DISCORD_ROLES_RANKED
from main import client


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
            if DISCORD_ROLES_RANKED[author.top_role.name] > DISCORD_ROLES_RANKED[lowest_officer_rank]:
                return False
            else:
                return True
        except KeyError as Key:
            logging.exception(f'Unknown rank {Key} tried to perform admin function')
            return False

    try:
        if not (context.message.author.guild_permissions.administrator or officer(context.message.author)):
            await send_message_to_user(context.message.author,
                                       "????? This function requires a Moderator, or Admin.")
            await disappearing_message(context.message, time_to_wait=5)
        else:
            return context.message.author
    except AttributeError as error:
        await send_message_to_user(context.message.author, f'????? you can\'t do that operation '
                                                           f'from a private message (it\'s a Discord limitation)')


async def ask_user(question, author):
    await send_message_to_user(author, question)
    msg = await client.wait_for('message', check=lambda message: message.author == author, timeout=300)
    data = msg.content.strip()
    # This allows you to cancel creating an event
    if data == '?cec':
        raise InterruptedError
    return data


async def send_message_to_user(user, message):
    try:
        await user.send(message)
    except Forbidden as forbiddenError:
        logging.error(f'{user}, blocked Asuna \n{forbiddenError}')
    except NotFound as nfError:
        logging.error(f'{user} was not found.\n{nfError}')
    except HTTPException as httpError:
        logging.error(f'Global problem sending message to {user}\n{httpError}')
    except InvalidArgument as iaError:
        logging.error(f'Some kind of invalid argument error sending message to {user}\n{iaError}')


async def ask_user_checked(message, author, function, format, exception_message):
    valid = False
    while not valid:
        try:
            raw_data = await ask_user(message, author)
            data = function(raw_data, format)
            return data
        except ValueError:
            await send_message_to_user(author, exception_message)


# Tries rank in the dictionary, if rank doesn't exist, throws and rethrows exception
def validate_min_rank(rank, format=None):
    try:
        possible_rank = DISCORD_ROLES_RANKED[rank]
        return rank
    except KeyError:  # Keeps our function with only one exception
        raise ValueError


def get_highest_discord_role(player_id, context):
    member = context.message.guild.get_member(player_id)
    discord_role = member.top_role
    return discord_role
