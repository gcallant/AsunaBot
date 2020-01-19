import re

from config.utilities import send_message_to_user
from resourcestrings import easter_egg_messages, non_descript_messages


async def process_easter_egg(author, lowercase):
    if re.match(r"hey.*", lowercase):
        await send_message_to_user(author, easter_egg_messages.hey_asuna)
    elif lowercase == "stfu":
        await send_message_to_user(author, easter_egg_messages.stfu)
    elif re.match(r".*fuck.*", lowercase):
        await send_message_to_user(author, easter_egg_messages.wildcard_fuck)
    elif lowercase == "thank you" or lowercase == 'thanks':
        await send_message_to_user(author, easter_egg_messages.thank_you)
    elif lowercase == "captain":
        await send_message_to_user(author, easter_egg_messages.captain)
    elif lowercase == "duel":
        await send_message_to_user(author, easter_egg_messages.duel)
    elif lowercase == "treb":
        await send_message_to_user(author, easter_egg_messages.treb)
    elif lowercase == "no":
        await send_message_to_user(author, easter_egg_messages.no)
    elif lowercase == "hammer":
        await send_message_to_user(author, easter_egg_messages.hammer)
    elif lowercase == "hi" or lowercase == "hello" or lowercase == "hey":
        await send_message_to_user(author, easter_egg_messages.hi)
    elif lowercase == "help":
        await send_message_to_user(author, easter_egg_messages.help)
    elif lowercase == "welcome":
        await send_message_to_user(author, non_descript_messages.member_join_welcome)
    else:
        await send_message_to_user(author, easter_egg_messages.default)