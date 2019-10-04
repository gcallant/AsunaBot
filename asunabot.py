# Original credit goes to Synthrelik for creating this bot
# Work continued on by Aeriana Filauria (and some help from Blitznacht112)
# To be used by Incurable Insanity admins for creating and leading trials and other events
import asyncio
import datetime
import logging
import platform
import re
import sys
from datetime import timedelta

import discord
from discord import Forbidden, NotFound, HTTPException, InvalidArgument
from discord.abc import PrivateChannel
from discord.ext.commands import Bot
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import true

from asunabot_declative import Event, PlayerSignup, Reminder, Roster, Base

# CONSTANTS
AERIANA_ID = 289942088596979713
have_run = False
is_toy = False
is_creation_event = False
is_editing = False

# Are we on our local dev machine?
if platform.system() == 'Windows':
    DEBUG = True
elif platform.system() == 'Linux':
    DEBUG = False
else:  # I don't know what the hell is going on
    sys.exit("This is an unsupported system")

if DEBUG:
    engine = create_engine('sqlite:///asunabot.db')
    BOT_TOKEN = 'NTE5NzA2ODQ4NTg1MTg3MzMy.DujPDg.5kr_-LfnCUeRLTR23yaqFY97OWo'
    # Testing Discord
    SERVER_ID = 373782910010130442
    # bot-test channel
    SIGNUP_LOG_CHANNEL_ID = 518513396484800512
    OFFICER_CHANNEL_ID = 543925704358756352
    logging.basicConfig(filename='Asuna.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
else:
    engine = create_engine('sqlite:////home/ec2-user/asunabot.db')
    BOT_TOKEN = 'NTE4NTUzNTcyNDI2NjQ1NTA0.DuShbw.TwNTD0i5vvgjbM27QtHCYG3vY44'
    # Incurable Insanity Discord
    SERVER_ID = 269224197299896320
    # botspam channel
    SIGNUP_LOG_CHANNEL_ID = 480506881237057566
    # Asuna-communications channel
    OFFICER_CHANNEL_ID = 544214746249822209
    logging.basicConfig(filename='Asuna.log', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)

Base.metadata.bind = engine
logging.getLogger('sqlalchemy.engine').setLevel(logging.WARN)
DBSession = sessionmaker(bind=engine)
session = DBSession()

BOT_PREFIX = ('?')
PLAYER_ROLES = {
    'tank',
    'healer',
    'mdps',
    'rdps',
    'reserve'
}

PLAYER_ROLES_DATA = {
    'tank': {
        'emoji': ':shield:',
        'display_name': 'Tank'
    },
    'healer': {
        'emoji': ':ambulance:',
        'display_name': 'Healer'
    },
    'mdps': {
        'emoji': ':crossed_swords:',
        'display_name': 'Melee'
    },
    'rdps': {
        'emoji': ':bow_and_arrow:',
        'display_name': 'Ranged'
    },
    'reserve': {
        'emoji': ':fingers_crossed:',
        'display_name': 'Reserve'
    }
}

DISCORD_ROLES_RANKED = {
    'High Queen': 1,
    'The Hand': 2,
    'Thane': 3,
    'Aesir': 4,
    'Valkyrie': 5,
    'Shieldbreaker': 6,
    'Marauder': 7,
    'Citizen': 8,
    'Thrall': 9,
    'Follower': 10
}

client = Bot(command_prefix=BOT_PREFIX)


@client.command(name='x',
                aliases=['X', 'signup', 'apply', ' '],
                description='Signs you up for an event in the current channel.',
                brief='Sign up for event.',
                pass_context=True)
async def player_signup(context, player_role, *flex_roles_args):
    message = context.message

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    channel = context.message.channel
    delete_message_after = 5
    event_id = channel.id
    flex_roles = ""
    event = session.query(Event).get(event_id)
    if event:
        cleaned_player_role = player_role.strip().lower()
        if cleaned_player_role == 'flex':
            await channel.send(
                'If you wish to flex a role, signup for your preferred role with additional specifiers '
                '(eg. ?x rdps mdps, tank)', delete_after=10)
            await disappearing_message(context.message, delete_message_after)
            return

        # Allows users to use ?x cancel
        if cleaned_player_role == 'cancel':
            await cancel_signup_execution(context)
            return

        # Allows users to also type heals or healer without adding an additional dictionary entry
        if cleaned_player_role == 'heals' or cleaned_player_role == 'heal':
            cleaned_player_role = 'healer'

        if cleaned_player_role in PLAYER_ROLES:
            if not cleaned_player_role == 'reserve' and \
                    (DISCORD_ROLES_RANKED[message.author.top_role.name] > DISCORD_ROLES_RANKED[event.min_rank]):
                await channel.send(f"ごめんなさい, you don't meet the minimum certified rank required for this run "
                                   f"as a {message.author.top_role.name}. You'll be signed up as reserve.\nIf this is "
                                   f"an error, "
                                   f"please contact Aeriana Filauria or Blitznacht112.", delete_after=15)
                flex_roles = cleaned_player_role
                cleaned_player_role = "reserve"
            elif event.min_rank == "Shieldbreaker" and discord.utils.get(message.author.roles,
                                                                         name=cleaned_player_role) is None:
                await channel.send(f"ごめんなさい, you don't meet the minimum certified rank required for this run "
                                   f"as a {cleaned_player_role}. You'll be signed up as a reserve.\nIf you are "
                                   f"certified as a different role, "
                                   f"please signup with a role you are certified for.\nIf this is an error, "
                                   f"please contact Aeriana Filauria or Blitznacht112.", delete_after=15)
                flex_roles = cleaned_player_role
                cleaned_player_role = "reserve"

            if flex_roles_args:
                flex_roles = ' '.join(flex_roles_args).strip().lower() + ' ' + flex_roles
            existing_player_signup = session.query(PlayerSignup).get((context.message.author.id, event.channel_id))
            if existing_player_signup:
                existing_player_signup.player_roles = cleaned_player_role
                existing_player_signup.flex_roles = flex_roles
            else:
                new_player_signup = PlayerSignup(
                    id=context.message.author.id,
                    player_name=context.message.author.display_name,
                    player_mention=context.message.author.mention,
                    player_roles=cleaned_player_role,
                    flex_roles=flex_roles,
                    event=event,
                )
                session.add(new_player_signup)
            try:
                session.commit()
            except:
                session.rollback()
                logging.exception(f'We had an error trying to add {message.author.name} to the roster')
                await channel.send(f'ごめんなさい, {message.author.mention} '
                                   f'There was an error, please try again!', delete_after=10)
            await message.add_reaction('✅')
            await channel.send(f'{message.author.mention} You are now signed up as ' + player_role.lower(),
                               delete_after=10)
            await update_channel_info_message(event_id, context)
            await disappearing_message(context.message)
        else:
            await channel.send(f'ごめんなさい, {message.author.mention} I do not recognize that role. Please try one of the '
                               f'following roles: '
                               + ', '.join(PLAYER_ROLES), delete_after=10)
            await disappearing_message(context.message, delete_message_after)
    else:
        await channel.send(f"せみません, {message.author.mention} it looks like there wasn\'t an event created for this "
                           f"channel.",
                           delete_after=10)
        await disappearing_message(context.message, delete_message_after)


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


@client.command(name='edit',
                description='Edits the event in the current channel.',
                brief='Edits this event.',
                pass_context=True)
async def edit_event(context):
    delete_message_after = 5
    author = await check_permissions(context)
    if not author:
        return

    message = context.message

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    channel = context.message.channel
    event_id = channel.id
    event = session.query(Event).get(event_id)
    if event:
        await edit_selector(event, author)
        try:
            session.commit()
        except:
            session.rollback()
            logging.exception(f'There was an error trying to edit event {channel.name}')
            channel.send(f'{message.author.mention} There was an error trying to edit this event, please try again.',
                         delete_after=10)
        await update_channel_info_message(event_id, context)
    else:
        await channel.send(f"せみません, {message.author.mention} it looks like there wasn\'t an event created for this "
                           f"channel.",
                           delete_after=10)
        await disappearing_message(message, delete_message_after)


async def edit_selector(event, author):
    continue_edit = True
    while continue_edit:
        await display_edit_menu(author)


async def display_edit_menu(author):
    await send_message_to_user(author, "Please type the number you would like to edit\n"
                                       "1: Name of the event\n"
                                       "2: Time of the event\n"
                                       "3: What trials you plan to run\n"
                                       "4: Event leader\n"
                                       "5: Number of tanks\n"
                                       "6: Number of healers\n"
                                       "7: Number of mDPS\n"
                                       "8: Number of rDPS\n"
                                       "9: Event description\n"
                                       "10: Minimum event rank\n"
                                       "11: Cancel editing\n")


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
                                       "すみません This function requires a Moderator, or Admin.")
            await disappearing_message(context.message, time_to_wait=5)
        else:
            return context.message.author
    except AttributeError as error:
        await send_message_to_user(context.message.author, f'すみません you can\'t do that operation '
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


# Tries rank in dictionary, if rank doesn't exist, throws and rethrows exception
def validate_min_rank(rank, format=None):
    try:
        possible_rank = DISCORD_ROLES_RANKED[rank]
        return rank
    except KeyError:  # Keeps our function with only one exception
        raise ValueError


@client.command(name='event',
                aliases=['event-create'],
                description='Creates an event, and a new channel for that event.',
                brief='Create an event',
                pass_context=True)
async def create_event(context):
    author = await check_permissions(context)
    if not author:
        return

    delete_message_after = 5
    try:
        global is_creation_event
        is_creation_event = True
        event_name = await ask_user("What do you want to name the event?", author)

        event_day = await ask_user_checked(message="What day is the event (ex. 06/24/1990)?", author=author,
                                           function=datetime.datetime.strptime, format="%m/%d/%Y",
                                           exception_message="ごめんなさい, you entered the date in an unrecognized format, "
                                                             "try again with MM/DD/YYYY\n")

        event_time = await ask_user_checked("What CST time is the event in 24 hour format (ex. 1800 for 6PM)?",
                                            author, datetime.datetime.strptime, "%H%M",
                                            "ごめんなさい, you entered the time in an unrecognized format, try again with "
                                            "HHHH (24 Hour)\n")
        # Adding Event Trial Name
        event_trial_name = await ask_user("What trials are you running? If multiple please list them."
                                          " You may use acronyms."
                                          "If running a dungeon type n/a Example: vAA, vHRC, vSO, vAS, vCR, vHoF, "
                                          "vMoL, "
                                          " nAA, nHRC, nSO, nCR, nHoF, nMoL", author)
        event_leader = await ask_user("Who is leading the event?", author)
        num_of_tanks = await ask_user("How many TANKS for the event?", author)
        num_of_heals = await ask_user("How many HEALERS for the event?", author)
        num_of_mdps = await ask_user("How many MELEE DPS for the event?", author)
        num_of_rdps = await ask_user("How many RANGED DPS for the event?", author)
        event_description = await ask_user("What is the event description?", author)
        event_rank = await ask_user_checked("What is the lowest rank that can apply for the event?",
                                            author, validate_min_rank, None,
                                            "ごめんなさい, you entered an unrecognized minimum rank, please enter "
                                            "one of the following **exactly** as written:\n"
                                            "Valkyrie, Shieldbreaker, Marauder, Citizen, Thrall, Follower\n")
    except InterruptedError:
        await send_message_to_user(author, "Event creation has been canceled.")
        logging.info(f'Event creation was canceled by {author} {datetime.datetime.now()}')
        is_creation_event = False
        return
    except asyncio.TimeoutError:
        logging.info(f'We timed out waiting for {author.name}')
        await send_message_to_user(author, f'ごめんなさい！I timed out waiting for a response to that last question (I '
                                           f'can\'t wait forever, it causes my server to crash!). Please try creating '
                                           f'the event again, but try to reply back within 5 minutes.')
        is_creation_event = False
        return
    finally:
        await disappearing_message(context.message, delete_message_after)

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
        is_creation_event = False
        return
    except HTTPException as http_exception:
        await send_message_to_user(author, f'Could not create event, there was an error {http_exception}, let Aeriana '
                                           f'know!')
        logging.exception(f'There wan an error creating event {event_name}, '
                          f'by {author.name}, details are {http_exception}')
        is_creation_event = False
        return
    except:
        await send_message_to_user(author, f'Could not create event, there was an unknown error, let Aeriana '
                                           f'know!')
        logging.exception(f'There was an unknown error when attempting to create event {event_name}')
        is_creation_event = False
        return

    await send_message_to_user(author, 'Created new channel for event with name: ' + event_name)

    new_roster = Roster(
        max_tanks=num_of_tanks,
        max_heal=num_of_heals,
        max_mdps=num_of_mdps,
        max_rdps=num_of_rdps
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
    except:
        session.rollback()
        await send_message_to_user(author, f'There was an error saving the event to the database, let Aeriana know!')
        logging.exception(f'There was an error saving {event_name} to the database')
        is_creation_event = False
        return

    channel_message = f'@everyone\nDate: {str(event_day).split()[0]}\nTime: ' \
                      f'{str(event_time).split()[1]} Central\n{event_description}\n\nRaid Leader:{event_leader} ' \
                      f'\n\n\n{get_event_details(new_channel.id, context)}' \
                      f'\n\nMinimum Rank: {event_rank}\nIf you are not this rank, ' \
                      f'you may still signup, but you will be listed as reserve.'
    channel_info_message = await new_channel.send(channel_message)

    event = session.query(Event).get(new_channel.id)
    event.channel_info_message = channel_info_message.id
    try:
        session.commit()
    except:
        session.rollback()
        await send_message_to_user(author, f'There was an error saving the event to the database, let Aeriana know!')
        logging.exception(f'There was an error saving {event_name} to the database')
        is_creation_event = False
        return

    is_creation_event = False


async def update_channel_info_message(event_id, context):
    event = session.query(Event).get(event_id)
    channel = client.get_channel(event_id)
    channel_message = await channel.fetch_message(event.channel_info_message)
    new_message_content = f'@everyone\nDate: {str(event.event_day).split()[0]}\nTime: {str(event.event_time).split()[1]} Central\n{event.event_description}\n\nRaid Leader:{event.event_leader} \n\n\n{get_event_details(event_id, context)}\n\nMinimum Rank: {event.min_rank}\nIf you are not this rank, you may still signup, but you will be listed as reserve.'
    await channel_message.edit(content=new_message_content)
    event.channel_info_message = channel_message.id
    session.commit()


def get_highest_discord_role(player_id, context):
    member = context.message.guild.get_member(player_id)
    discord_role = member.top_role
    return discord_role


@client.command(name='event-details',
                description='Check details for this event.',
                brief='Check details for this event.',
                pass_context=True)
async def show_event_details(context, extra=None):
    author = context.message.author
    event_details = get_event_details(context.message.channel.id, context, extra)
    await disappearing_message(context.message, time_to_wait=5)
    await send_message_to_user(author, event_details)


@client.command(name='cec',
                description='When used in a message to the bot, during making an event, it will stop the current '
                            'event that is being created.',
                brief='Cancels creating the current event.',
                pass_context=True)
async def cancel_event_creation(context):
    if not isinstance(context.message.channel, PrivateChannel):
        await context.channel.send(f"ごめんなさい, {context.author.mention} "
                                   f"this command will only work during an event creation.", delete_after=10)


@client.command(name='reminderCheck',
                description='Initiates a command to check all events for reminders to send out now, instead of '
                            'during the usual 5 minute check',
                brief='Checks all events for reminders',
                pass_context=True)
async def run_reminders_now(context):
    author = await check_permissions(context)
    if not author:
        return
    delete_message_after = 5
    await context.channel.send(f"行く！{author.mention} A request to run a check for all reminders was initiated!",
                               delete_after=10)
    await disappearing_message(context.message, delete_message_after)
    await check_reminders()


def get_event_details(event_id, context, extra=None):
    event = session.query(Event).get(event_id)
    if event:
        signups = session.query(PlayerSignup).filter(PlayerSignup.event_id == event.channel_id) \
            .order_by(PlayerSignup.date_created.asc()).all()
        if signups and len(signups) > 0:
            signups_by_role = {}

            for signup in signups:
                signups_by_role[signup.player_roles] = signups_by_role.get(signup.player_roles, []) + [signup]

            result = ""
            for player_role, player_role_data in PLAYER_ROLES_DATA.items():
                player_names_joined = None
                if player_role in signups_by_role:
                    signups = signups_by_role[player_role]
                    player_names_joined = "\n".join([
                        f'\t {signup.player_mention} {"(Can Flex: " + signup.flex_roles + ")" if signup.flex_roles else ""} (Rank:{get_highest_discord_role(int(signup.id), context)}) {signup.date_created.strftime("- %Y-%m-%d %H:%M") if extra == "extra" else ""}'
                        for signup in signups])
                if player_names_joined:
                    result += f'{player_role_data["emoji"]} {player_role_data["display_name"]}: \n{player_names_joined}\n\n'
                else:
                    result += f'{player_role_data["emoji"]} ' \
                              f'{player_role_data["display_name"]}: \n\tNo players signed up for this role\n\n'

            return f'The current players signed up are: \n{result}'
        else:
            return 'No players have signed up for this event.'
    else:
        return 'No event has been created for this channel.'


@client.command(name='myevents',
                description='Shows events you signed up for.',
                brief='Shows events you signed up for.',
                pass_context=True)
async def my_events(context):
    signups = session.query(PlayerSignup).filter(PlayerSignup.id == context.message.author.id) \
        .filter(PlayerSignup.event.has(active=true())).all()

    if signups is None or len(signups) == 0:
        await context.message.channel.send(f'{context.message.author.mention}, '
                                           f'you are not signed up for any events.', delete_after=10)
    else:
        result = "\n".join(
            [f'* {client.get_channel(int(signup.event.channel_id)).name} - {signup.player_roles}' for signup in
             signups])
        await send_message_to_user(context.message.author,
                                   f'{context.message.author.mention}, your current events are: \n{result}')

    await disappearing_message(context.message, time_to_wait=5)


@client.command(name='cancel',
                description='Cancels your signup for the current event.',
                brief='Cancel signup',
                pass_context=True)
async def cancel_signup(context):
    await cancel_signup_execution(context)


async def cancel_signup_execution(context):
    event_id = context.message.channel.id
    player_id = context.message.author.id
    delete_message_after = 5
    event = session.query(Event).get(event_id)
    existing_player_signup = session.query(PlayerSignup).get((player_id, event_id))
    if existing_player_signup:
        session.delete(existing_player_signup)
        session.commit()
        await context.message.channel.send(
            f'{context.message.author.mention}, you are no longer signed up for this event.',
            delete_after=10)
        await update_channel_info_message(event_id, context)
        await disappearing_message(context.message, delete_message_after)
    else:
        await context.message.channel.send(f'{context.message.author.mention}, my records show you never signed up '
                                           f'for this event.',
                                           delete_after=10)
        await disappearing_message(context.message, delete_message_after)


@client.event
async def on_guild_channel_delete(channel):
    existing_event = session.query(Event).get(channel.id)
    if existing_event:
        existing_event.active = False
        try:
            session.commit()
        except:
            session.rollback()
            aeriana = client.get_user(AERIANA_ID)
            aeriana.send(f'Had a problem deactivating deleted channel {channel.name} to DB')
            logging.exception(f'Problem committing channel deactivation with channel {channel.name}')
            return

        channel = client.get_channel(SIGNUP_LOG_CHANNEL_ID)
        await channel.send(f'The following event was marked inactive due to channel removal: '
                           f'{channel.name}.', delete_after=30)


def welcome_message():
    return "\n**Welcome to _Incurable Insanity_!**\n\nWe are pleased to have you here and want to take this " \
           "opportunity to lay out the next steps in your journey with us.\n\nFirstly, most of who and " \
           f"what we are can be found in the **Rules-N-Shit** discord text channel. " \
           f"There you will find our " \
           "ranking system clearly laid out. If you are a player that is wanting some advice on your toon(s), " \
           "we have class captains of every role and toon type. Please reach out to any officer *(Aesir or above)* " \
           "about hooking you up with the right mentor. If you are more of a seasoned player and are itching " \
           "to get into one of our progression teams, please reach out to *Blitznacht* or *Angiefaerie*.\n\nNext, " \
           "we want you to know that **_Incurable Insanity_** is a welcoming and fun place for people to have a " \
           "great time and kick ass. We have **__3__ rules**: **__no drama__**, **__no elitism__**, **__help " \
           "people__**. We do **__not__ tolerate** any **hateful speech** but we **_adore_ bad puns and innuendo**. " \
           "So please feel free let myself or any of " \
           "the officers know what your in-game goals are and " \
           "we would love to help you meet those goals!\n\n - **Angiefaerie, GM**"


async def echo(message):
    author = message.author
    if author.id != AERIANA_ID:
        await send_message_to_user(author, "Take your toys and go home, I do not want to play anymore")
        return
    global is_toy
    is_toy = True
    try:
        channel = await ask_user("What's the channel id?", author)
        message = await ask_user("What's the message?", author)
    except InterruptedError:
        await send_message_to_user(author, 'Okay, no more fun for you! :stuck_out_tongue_winking_eye:')
        is_toy = False
        return

    channel = client.get_channel(channel)
    await channel.send(message)
    is_toy = False


@client.event
async def on_message(message):
    if message.content.startswith("?"):
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
        if not (is_creation_event or is_editing or is_toy):
            lowercase = message.content.upper().lower()
            if lowercase == "hey asuna":
                await send_message_to_user(author, "What do you want?? :unamused: "
                                                   "Don't I already do enough for you people? :rage:")
            elif lowercase == "stfu":
                await send_message_to_user(author, "I am confused, fuck does not go up! :confused:")
            elif re.match(r".*fuck.*", lowercase):
                await send_message_to_user(author, ":open_mouth: You kiss your mother with that mouth?!")
            elif lowercase == "thank you" or lowercase == 'thanks':
                await send_message_to_user(author, "WOW!  You are the first person to thank me for the services I "
                                                   "provide for free.\n"
                                                   "You know, you are very, very welcome kind one.\n"
                                                   "Live long and prosper! :vulcan:")
            elif lowercase == "captain":
                await send_message_to_user(author, "Has anyone ever told you that Cap is the best Magicka "
                                                   "DragonKnight I know? Well she is! :dragon_face:\nTell her to keep "
                                                   "that shit up! Perhaps she and I can spar one day.")
            elif lowercase == "duel":
                await send_message_to_user(author, "Some Roshambo?\nFisticuffs?\nA Battle of the wits?\n"
                                                   "Perhaps jousting... I like jousting...\n"
                                                   "I jest, I mean I wish I could fight, but alas, I am but a mere "
                                                   "administrative assistant with aspirations of great adventures. "
                                                   "Perhaps you could "
                                                   "send me a post card, and I can live bi-curiously through you?")
            elif lowercase == "treb":
                await send_message_to_user(author, "これは一体何！:scream: Why does everyone keep asking me about Trebusan?! "
                                                   ":flushed: I mean, I think he's a good looking guy, I do... but, "
                                                   "he's just not my type. ごめんなさい Trebusan! :cow:")
            elif lowercase == "no":
                await send_message_to_user(author,
                                           "Well fine then! I will go play go play the reboot of the 1978 Space "
                                           "Invaders by myself! :stuck_out_tongue: :robot: "
                                           "You on the other hand should avoid those arrows to the knee! "
                                           ":bow_and_arrow: "
                                           "I hear it hurts, and in the end you turn into a guard. What a boring life "
                                           "that is!")
            elif lowercase == "hammer":
                await send_message_to_user(author,
                                           "Captain Hammer huh? Well, you're no Nathan Fillion, but...\n```'You got a "
                                           "job, we can do it, "
                                           "don't much care what it is.'```\nSorry I could not resist a juicy movie "
                                           "quote. :squid: :movie_camera: ")
            elif lowercase == "hi" or lowercase == "hello" or lowercase == "hey":
                await send_message_to_user(author, "Hi to you too! Or as I would say in Japan, こんにちわ! :smiley:")
            elif lowercase == "help":
                await send_message_to_user(author,
                                           "So you want help? Try typing **hey asuna** or **captain**. **Hammer** "
                                           "might work too... :stuck_out_tongue_winking_eye:\nI was coded with a "
                                           "decent amount of lines but my memory is kinda poor (because Aeriana has "
                                           "to pay for my resources :sob:). You might have to just try random shit, "
                                           "that is what my friend Blitz does. :scream_cat:.\nIf you really want "
                                           "*actual* help, try typing **?help**  for a better list of my command "
                                           "functions!")
            else:
                await send_message_to_user(author, "Take your toys and go home, I do not want to play anymore\n(i.e. "
                                                   "I don't know what you mean by that, try something else! "
                                                   ":stuck_out_tongue_winking_eye:)")


@client.event
async def on_member_join(member):
    roles = member.guild.roles
    role = discord.utils.get(roles, name="Follower")
    await member.add_roles(role, reason='Because they\'re a new member of our discord!')
    await send_message_to_user(member, welcome_message())


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')


def default_message(event, player, time):
    return f"こんにちわ {player.player_name},\n\nThis is a friendly {time} reminder that you signed up for the event:\n\n\
```{event.event_name} \non {str(event.event_day).split()[0]}\nat {str(event.event_time).split()[1]}CST\n\
You signed up as a: {player.player_roles}```\n\n\
For more information, please refer to the {event.event_name} channel." \
           f"\nIf you cannot attend the event, or wish to cancel, please \
use the command ?cancel in the {event.event_name} channel."


def imminent_message(event, player):
    return f"こんにちわ, {player.player_name}, your event {event.event_name} " \
           f"starts in less than 15 minutes!\nPlease get logged in \
on your character as a {player.player_roles} and x-up in chat in the next 5 minutes.\nPlease ensure your inventory is \
clear and you have all appropriate gear, food, and potions needed for the run. We will be starting shortly!"


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
        print(f"Received an invalid reminder number {reminder} for event {event.event_name}")


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
    time_in_two_days = datetime.datetime.now() + timedelta(hours=48)
    time_in_one_day = datetime.datetime.now() + timedelta(hours=24)
    time_in_two_hours = datetime.datetime.now() + timedelta(hours=2)
    time_in_fifteen_minutes = datetime.datetime.now() + timedelta(minutes=15)
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


@client.command(name='promotionCheck',
                description='Initiates a command to check users for eligible promotions now',
                brief='Checks promotions',
                pass_context=True)
async def check_promotions_now(context):
    author = await check_permissions(context)
    if not author:
        return

    delete_message_after = 5
    await context.message.channel.send("A request to run a check for promotions was initiated", delete_after=10)
    await disappearing_message(context.message, delete_message_after)
    await check_promotions()


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
    time_in_two_days = datetime.datetime.now() + timedelta(hours=48)
    events = session.query(Event).filter(Event.active == True) \
        .filter(time_in_two_days >= Event.event_day).all()
    return events


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
        channel = client.get_channel(OFFICER_CHANNEL_ID)
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
        channel = client.get_channel(OFFICER_CHANNEL_ID)
        await channel.send(message)


def compile_members(citizen_list, thrall_list):
    server = client.get_guild(SERVER_ID)
    members = server.members
    for member in members:
        if member.top_role.name == 'Thrall' and not discord.utils.get(member.roles, name="Inactive"):
            thrall_list.append(member)
        elif member.top_role.name == 'Citizen' and not discord.utils.get(member.roles, name="Inactive"):
            citizen_list.append(member)


async def check_promotions():
    global have_run
    if have_run is True:
        return
    citizen_list = list()
    thrall_list = list()
    # It's most efficient to compile both lists at the same time, since all members have to be
    # iterated through- doing this through pass-by-reference is the cleanest way
    compile_members(citizen_list, thrall_list)
    await check_citizen_promotions(thrall_list)
    await check_marauder_promotions(citizen_list)
    have_run = True


async def run_client():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        await check_reminders()
        await check_promotions()
        for server in client.guilds:
            print(server.name)
        print('------')
        await asyncio.sleep(600)


client.loop.create_task(run_client())
client.run(BOT_TOKEN)
