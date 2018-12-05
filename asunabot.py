# Work with Python 3.6
# Original credit goes to Synthrelik for creating this bot
# To be used by Incurable Insanity admins for creating and leading trials and other events
import asyncio
import platform
import discord
import datetime
from discord.ext.commands import Bot
from sqlalchemy import create_engine
from sqlalchemy.sql.expression import true
from sqlalchemy.orm import sessionmaker
from asunabot_declative import Event, PlayerSignup, Roster, Base

engine = create_engine('sqlite:///asunabot.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

# CONSTANTS

#Are we on our local dev machine?
if platform.system() == 'Windows':
   DEBUG = True
elif platform.system() == 'Linux':
   DEBUG = False
else: #I don't know what the hell is going on
   sys.exit("This is an unsupported system")

if DEBUG:
   BOT_TOKEN = 'NTE5NzA2ODQ4NTg1MTg3MzMy.DujPDg.5kr_-LfnCUeRLTR23yaqFY97OWo'
   #Testing Discord
   SERVER_ID = '373782910010130442'
   #bot-test channel
   SIGNUP_LOG_CHANNEL_ID = '518513396484800512'
else:
   BOT_TOKEN = 'NTE4NTUzNTcyNDI2NjQ1NTA0.DuShbw.TwNTD0i5vvgjbM27QtHCYG3vY44'
   #Incurable Insanity Discord
   SERVER_ID = '269224197299896320'
   #Not sure what channel this is '498328294366642195',
   #oct7-vdsa-training channel
   SIGNUP_LOG_CHANNEL_ID = '498322289410965504'


BOT_PREFIX = ("?")
PLAYER_ROLES = {
   'tank',
   'heal',
   'mdps',
   'rdps',
   'reserve'
   }

PLAYER_ROLES_DATA = {
   'tank': {
      'emoji': ':shield:',
      'display_name': 'Tank'
      },
   'heal': {
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
   'flex': {
      'emoji': ':question:',
      'display_name': 'Flex'
      },
   'reserve': {
      'emoji': ':fingers_crossed:',
      'display_name': 'Reserve'
      }
   }

DISCORD_ROLES_RANKED = {
   'High Queen': 1,
   'Jarl': 2,
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
                aliases=['X', 'signup', 'apply'],
                description='Signs you up for an event in the current channel.',
                brief='Sign up for event.',
                pass_context=True)
async def player_signup(context, player_role, *flex_roles_args):
   message = context.message

   # we do not want the bot to reply to itself
   if message.author == client.user:
      return

   channel = context.message.channel
   event_id = channel.id
   event = session.query(Event).get(event_id)
   if event:
      cleaned_player_role = player_role.strip().lower()
      if cleaned_player_role == 'flex' or cleaned_player_role == 'reserve':
         await client.say(
            'Sorry, I am no longer supporting the flex and reserve role.'
            )
         return
      #Allows users to also type heals without adding an additional dictionary entry
      if  cleaned_player_role == 'heals':
            cleaned_player_role = 'heal'
      flex_roles = None
      # if cleaned_player_role == 'flex' or cleaned_player_role == 'reserve':
      #    flex_roles = ' '.join(flex_roles_args).strip().lower()

      if cleaned_player_role in PLAYER_ROLES:
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
         session.commit()
         # await client.send_message(context.message.author,
         #     'You are now signed up as ' + player_role.lower() + ", " + context.message.author.mention)
         await client.add_reaction(context.message, '✅')
         await update_channel_info_message(event_id)
      else:
         await client.say(
            'Sorry, I do not recognize that role. Please try one of the following roles: ' + ', '.join(
               PLAYER_ROLES))
   else:
      await client.say("Oops, it looks like there wasn't an event created for this channel.")


@client.command(name='event',
                aliases=['event-create'],
                description='Creates an event, and a new channel for that event.',
                brief='Create an event',
                pass_context=True)
async def create_event(context):
   if not context.message.author.server_permissions.administrator:
      await client.send_message(context.message.author,
                                "Woah! Slow your roll bub. You're not an admin and can't do this.")
   else:
      author = context.message.author

      def check(msg):
         return true

      async def ask_user(question, author, client):
         await client.send_message(author, question)
         msg = await client.wait_for_message(author=author, check=check)
         return msg.content.strip()

      event_name = await ask_user("What do you want to name the event?", author, client)

      async def askUserChecked(message, author, client, function, format, exceptionMessage):
         valid = False
         while not valid:
            try:
               raw_data = await ask_user(message, author, client)
               data = function(raw_data, format)
               return data
            except:
              await client.send_message(author, exceptionMessage)

      event_day = await askUserChecked(message="What day is the event (ex. 06/24/1990)?", author=author, client=client,
                                 function=datetime.datetime.strptime, format="%m/%d/%Y",
                                 exceptionMessage="Sorry, you entered the date in an unrecognized format, try again with MM/DD/YYYY\n")


      

      event_time = await ask_user("What time is the event (in CST)?", author, client)


      eventNumReminders = await askUserChecked("How many reminders would you like to make (specify a number 0-3)\n"
                                               "You'll be asked when you'd like to set them in the follow question.",
                                               author, client, int, 10,
                                               "Sorry, you entered the number in an unrecognized format, try again with 0-3\n")

      # if eventNumReminders > 0:
      #    valid = False
      #    while not valid:
      #       try:
      #          eventReminders = [eventNumReminders]
      #          for events in eventReminders:
      #             eventReminders[event] = await askUserChecked("").__format__(events + 1)
      #       except:
      #          print("Nope")

      event_leader = await ask_user("Who is leading the event?", author, client)
      num_of_tanks = await ask_user("How many TANKS for the event?", author, client)
      num_of_heals = await ask_user("How many HEALERS for the event?", author, client)
      num_of_mdps = await ask_user("How many MELEE DPS for the event?", author, client)
      num_of_rdps = await ask_user("How many RANGED DPS for the event?", author, client)
      event_description = await ask_user("What is the event description?", author, client)
      event_rank = await ask_user("What is the lowest rank that can apply for the event?", author, client)

      new_roster = Roster(
         max_tanks=num_of_tanks,
         max_heal=num_of_heals,
         max_mdps=num_of_mdps,
         max_rdps=num_of_rdps
         )
      session.add(new_roster)
      session.commit()

      new_channel = await client.create_channel(client.get_server(SERVER_ID), event_name, type=discord.ChannelType.text)
      await client.send_message(author, 'Created new channel for event with name: ' + event_name)

      new_event = Event(
         event_name=event_name,
         channel_id=new_channel.id,
         event_day=event_day,
         event_time=event_time,
         event_leader=event_leader,
         created_by_id=author.id,
         roster=new_roster,
         event_description=event_description,
         min_rank=event_rank
         )

      session.add(new_event)
      session.commit()

      channel_message = f'@everyone\nDate: {event_day_raw}\nTime: {event_time} Central\n{event_description}\n\nRaid Leader:{event_leader} \n\n\n{get_event_details(new_channel.id)}'
      channel_info_message = await client.send_message(new_channel, channel_message)

      event = session.query(Event).get(new_channel.id)
      event.channel_info_message = channel_info_message.id
      session.commit()

async def update_channel_info_message(event_id):
   event = session.query(Event).get(event_id)
   channel = client.get_channel(event_id)
   channel_message = await client.get_message(channel, event.channel_info_message)
   new_message_content = f'@everyone\nDate: {event.event_day.split()[0]}\nTime: {event.event_time} Central\n{event.event_description}\n\nRaid Leader:{event.event_leader} \n\n\n{get_event_details(event_id)}'
   channel_info_message = await client.edit_message(channel_message, new_content=new_message_content)
   event.channel_info_message = channel_info_message.id
   session.commit()


def get_highest_discord_role(player_id):
   discord_role = client.get_server(client.get_).get_member(player_id).top_role
   return discord_role.name


@client.command(pass_context=True)
async def tell_them(context):
   await client.say("My master he...he...he...I CAN'T SAY")


@client.command(pass_context=True)
async def tell_them_more(context):
   await client.say("My master he...he...he...I CAN'T SAY")

@client.command(name='event-details',
                description='Check details for this event.',
                brief='Check details for this event.',
                pass_context=True)
async def event_details(context, extra=None):
   event_details = get_event_details(context.message.channel.id, extra)
   await client.say(event_details)


def get_event_details(event_id, extra=None):
   event = session.query(Event).get(event_id)
   if event:
      signups = session.query(PlayerSignup).filter(PlayerSignup.event_id == event.channel_id).order_by(
         PlayerSignup.date_created.asc()).all()
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
                  f'\t {signup.player_mention} {"(Roles: " + signup.flex_roles + ")" if signup.flex_roles else ""} (Rank:{get_highest_discord_role(signup.id)}) {signup.date_created.strftime("- %Y-%m-%d %H:%M") if extra=="extra" else ""}'
                  for signup in signups])
            if player_names_joined:
               result += f'{player_role_data["emoji"]} {player_role_data["display_name"]}: \n{player_names_joined}\n\n'
            else:
               result += f'{player_role_data["emoji"]} {player_role_data["display_name"]}: \n\tNo players signed up for this role\n\n'

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
   signups = session.query(PlayerSignup).filter(PlayerSignup.id == context.message.author.id).filter(
      PlayerSignup.event.has(active=true())).all()

   if signups is None or len(signups) == 0:
      await client.send_message(context.message.author, f'{context.message.author.mention}, you are not signed up for any events.')
   else:
      result = "\n".join([f'* {client.get_channel(signup.event.channel_id).name} - {signup.player_roles}' for signup in signups])
      await client.send_message(context.message.author, f'{context.message.author.mention}, your current events are: \n{result}')


@client.command(name='cancel',
                description='Cancels your signup for the current event.',
                brief='Cancel signup',
                pass_context=True)
async def cancel_signup(context):
   event_id = context.message.channel.id
   player_id = context.message.author.id
   event = session.query(Event).get(event_id)
   existing_player_signup = session.query(PlayerSignup).get((player_id, event_id))
   if existing_player_signup:
      session.delete(existing_player_signup)
      session.commit()
      await client.say(f'{context.message.author.mention}, you are no longer signed up for this event.')
      await update_channel_info_message(event_id)
   else:
      await client.say(f'{context.message.author.mention}, my records show you never signed up for this event.')


@client.event
async def on_channel_delete(channel):
   existing_event = session.query(Event).get(channel.id)
   if existing_event:
      existing_event.active = False
      session.commit()
      await client.send_message(client.get_channel(SIGNUP_LOG_CHANNEL_ID),
                                f'The following event was marked inactive due to channel removal: {channel.name}.')


@client.event
async def on_ready():
   print('Logged in as')
   print(client.user.name)
   print(client.user.id)
   print('------')


async def list_servers():
   await client.wait_until_ready()
   while not client.is_closed:
      print("Current servers:")
      for server in client.servers:
         print(server.name)
      print('------')
      await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(BOT_TOKEN)
