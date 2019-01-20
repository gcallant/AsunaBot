# Work with Python 3.6
# Original credit goes to Synthrelik for creating this bot
# Work continued on by AerianaFilauria
# To be used by Incurable Insanity admins for creating and leading trials and other events
import asyncio
import platform
import discord
import datetime
from datetime import timedelta
from discord.ext.commands import Bot
from sqlalchemy import create_engine, text
from sqlalchemy.sql.expression import true
from sqlalchemy.orm import sessionmaker
from asunabot_declative import Event, PlayerSignup, Reminder, Roster, Base

engine = create_engine('sqlite:////home/ec2-user/asunabot.db')
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
   #botspam channel
   SIGNUP_LOG_CHANNEL_ID = '480506881237057566'


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
      if cleaned_player_role == 'flex': #or cleaned_player_role == 'reserve':
         await client.say(
            'ごめんなさい, I am no longer supporting the flex role.'
            )
         return
      #Allows users to also type heals without adding an additional dictionary entry
      if  cleaned_player_role == 'heals':
         cleaned_player_role = 'heal'
      flex_roles = None
      if cleaned_player_role == 'reserve':
          flex_roles = ' '.join(flex_roles_args).strip().lower()

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
         await update_channel_info_message(event_id, context)
      else:
         await client.say(
            'ごめんなさい, I do not recognize that role. Please try one of the following roles: ' + ', '.join(
               PLAYER_ROLES))
   else:
      await client.say("せみません, it looks like there wasn't an event created for this channel.")


@client.command(name='edit',
                description='Edits the event in the current channel.',
                brief='Edits this event.',
                pass_context=True)
async def edit_event(context):
   client.say("ごめんなさい, functionality has not yet been implemented for this feature.")
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
      await update_channel_info_message(event_id, context)
   else:
      await client.say("せみません, it looks like there wasn't an event created for this channel.")


async def check_permissions(context):
   if not context.message.author.server_permissions.administrator:
      await client.send_message(context.message.author,
                                "ごめんなさい, I don't seem to have you on my list of admins. If this is an error "
                                "please contact a Thane and let them know you need admin permissions.")
   else:
      return context.message.author



@client.command(name='event',
                aliases=['event-create'],
                description='Creates an event, and a new channel for that event.',
                brief='Create an event',
                pass_context=True)
async def create_event(context):
   author = await check_permissions(context)
   if not author:
      return
   
   def check(msg):
      return true
   SERVER_ID = context.message.server.id

   async def ask_user(question, author, client):
      await client.send_message(author, question)
      msg = await client.wait_for_message(author=author, check=check)
      data = msg.content.strip()
      if data == '?cec':
         raise InterruptedError
      return data

   async def askUserChecked(message, author, client, function, format, exceptionMessage):
      valid = False
      while not valid:
         try:
            raw_data = await ask_user(message, author, client)
            data = function(raw_data, format)
            return data
         except ValueError:
            await client.send_message(author, exceptionMessage)
   try:
      event_name = await ask_user("What do you want to name the event?", author, client)

      event_day = await askUserChecked(message="What day is the event (ex. 06/24/1990)?", author=author, client=client,
                                 function=datetime.datetime.strptime, format="%m/%d/%Y",
                                 exceptionMessage="ごめんなさい, you entered the date in an unrecognized format, try again with MM/DD/YYYY\n")

      event_time = await askUserChecked("What CST time is the event in 24 hour format (ex. 1800 for 6PM)?",
                                        author, client, datetime.datetime.strptime, "%H%M",
                                        "ごめんなさい, you entered the time in an unrecognized format, try again with HHHH (24 Hour)\n")
      event_leader = await ask_user("Who is leading the event?", author, client)
      num_of_tanks = await ask_user("How many TANKS for the event?", author, client)
      num_of_heals = await ask_user("How many HEALERS for the event?", author, client)
      num_of_mdps = await ask_user("How many MELEE DPS for the event?", author, client)
      num_of_rdps = await ask_user("How many RANGED DPS for the event?", author, client)
      event_description = await ask_user("What is the event description?", author, client)
      event_rank = await ask_user("What is the lowest rank that can apply for the event?", author, client)
   except InterruptedError:
      await client.send_message(author, "Event creation has been canceled.")
      print(f'Event creation was canceled by {author} {datetime.datetime.now()}')
      return

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

   channel_message = f'@everyone\nDate: {str(event_day).split()[0]}\nTime: {str(event_time).split()[1]} Central\n{event_description}\n\nRaid Leader:{event_leader} \n\n\n{get_event_details(new_channel.id, context)}'
   channel_info_message = await client.send_message(new_channel, channel_message)

   event = session.query(Event).get(new_channel.id)
   event.channel_info_message = channel_info_message.id
   session.commit()

async def update_channel_info_message(event_id, context):
   event = session.query(Event).get(event_id)
   channel = client.get_channel(event_id)
   channel_message = await client.get_message(channel, event.channel_info_message)
   new_message_content = f'@everyone\nDate: {str(event.event_day).split()[0]}\nTime: {str(event.event_time).split()[1]} Central\n{event.event_description}\n\nRaid Leader:{event.event_leader} \n\n\n{get_event_details(event_id, context)}'
   channel_info_message = await client.edit_message(channel_message, new_content=new_message_content)
   event.channel_info_message = channel_info_message.id
   session.commit()

def set_reminders():
   print()
   #48 hours, 24 hours, 2hours, 15minutes- canned reminders requested for now
   # eventNumReminders = await askUserChecked("How many reminders would you like to make (specify a number 0-3)\n"
   #                                          "You'll be asked when you'd like to set them in the follow question.",
   #                                          author, client, int, 10,
   #                                          "ごめんなさい, you entered the number in an unrecognized format, try again with 0-3\n")
   #
   # def numberOrdinal(number):
   #    if number == 1:
   #       return "1st"
   #    elif number == 2:
   #       return "2nd"
   #    elif number == 3:
   #       return "3rd"
   #    else:
   #       return "It's over 9000!"
   #
   # if eventNumReminders > 0:
   #    eventReminders = range(eventNumReminders)
   #    for event in eventReminders:
   #       eventReminders[event] = await askUserChecked("Enter the day and time you'd like the {} reminder to be sent in 24H time CST\n"
   #                                                    "For example: 12/07/2018/1600/0 would send a reminder to all users "
   #                                                    "signed up for the event at 4:00PMCST on 12/07/2018)".format(numberOrdinal(event + 1)),
   #                                                    author, client, datetime.datetime.strptime,
   #                                                    "%m/%d/%Y/%H/%M",
   #                                                    "ごめんなさい, you entered the date in an unrecognized format, try again with MM/DD/YYYY/HHHH/MM\n")


def get_highest_discord_role(player_id, context):
   discord_role = client.get_server(context.message.server.id).get_member(player_id).top_role
   return discord_role.name


# @client.command(pass_context=True)
# async def tell_them(context):
#    await client.say("My master he...he...he...I CAN'T SAY")
#
#
# @client.command(pass_context=True)
# async def tell_them_more(context):
#    await client.say("My master he...he...he...I CAN'T SAY")

@client.command(name='event-details',
                description='Check details for this event.',
                brief='Check details for this event.',
                pass_context=True)
async def event_details(context, extra=None):
   event_details = get_event_details(context.message.channel.id, context, extra)
   await client.say(event_details)


@client.command(name='cec',
                description='When used in a message to the bot, during making an event, it will stop the current '
                            'event that is being created.',
                brief='Cancels creating the current event.',
                pass_context=True)
async def cancelEventCreation(context):
   if not context.message.channel.is_private:
      await client.say("ごめんなさい, this command will only work during an event creation.")


@client.command(name='reminderCheck',
                description='Initiates a command to check all events for reminders to send out now, instead of '
                            'during the usual 5 minute check',
                brief='Checks all events for reminders',
                pass_context=True)
async def runRemindersNow(context):
   author = await check_permissions(context)
   if not author:
      return

   await client.say("A request to run a check for all reminders was initiated")
   await checkReminders()


def get_event_details(event_id, context, extra=None):
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
                  f'\t {signup.player_mention} {"(Roles: " + signup.flex_roles + ")" if signup.flex_roles else ""} (Rank:{get_highest_discord_role(signup.id, context)}) {signup.date_created.strftime("- %Y-%m-%d %H:%M") if extra=="extra" else ""}'
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
      await update_channel_info_message(event_id, context)
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

def defaultMessage(event, player, time):
   return f"こんにちわ {player.player_name},\n\nThis is a friendly {time} reminder that you signed up for the event:\n\n\
```{event.event_name} \non {str(event.event_day).split()[0]}\nat {str(event.event_time).split()[1]}CST\n\
You signed up as a: {player.player_roles}```\n\n\
For more information, please refer to the {event.event_name} channel.\nIf you cannot attend the event, or wish to cancel, please \
use the command ?cancel in the {event.event_name} channel."

def imminentMessage(event, player):
   return f"こんにちわ, {player.player_name}, your event {event.event_name} starts in less than 15 minutes!\nPlease get logged in \
on your character as a {player.player_roles} and x-up in chat in the next 5 minutes.\nPlease ensure your inventory is \
clear and you have all appropriate gear, food, and potions needed for the run. We will be starting shortly!"

def getMessageForTime(reminder, event, player):
   if reminder == 0:
      return defaultMessage(event, player, "48 hour")
   elif reminder == 1:
      return defaultMessage(event, player, "24 hour")
   elif reminder == 2:
      return defaultMessage(event, player, "2 hour")
   elif reminder == 3:
      return imminentMessage(event, player)
   else:
      print(f"Received an invalid reminder number {reminder} for event {event.event_name}")

def markReminderSent(reminderNumber, eventID):
   newReminder = session.query(Reminder).filter(Reminder.id == eventID).one_or_none()

   if reminderNumber == 0:
      if(newReminder == None):
         newReminder = Reminder(id = eventID, first_reminder_sent=True, second_reminder_sent=False,
                             third_reminder_sent=False, fourth_reminder_sent=False)
      session.add(newReminder)
      session.commit()
   elif reminderNumber == 1:
      if(newReminder == None):
         newReminder = Reminder(id = eventID, first_reminder_sent=False, second_reminder_sent=True,
                                third_reminder_sent=False, fourth_reminder_sent=False)
         session.add(newReminder)
      else:
         newReminder.second_reminder_sent = True
      session.commit()
   elif reminderNumber == 2:
      if(newReminder == None):
         newReminder = Reminder(id = eventID, first_reminder_sent=False, second_reminder_sent=False,
                                third_reminder_sent=True, fourth_reminder_sent=False)
         session.add(newReminder)
      else:
         newReminder.third_reminder_sent = True
      session.commit()
   elif reminderNumber == 3:
      if(newReminder == None):
         newReminder = Reminder(id = eventID, first_reminder_sent=False, second_reminder_sent=False,
                                third_reminder_sent=False, fourth_reminder_sent=True)
         session.add(newReminder)
      else:
         newReminder.fourth_reminder_sent = True
      session.commit()

async def sendReminder(reminder, event):
   players = session.query(PlayerSignup).filter(PlayerSignup.event_id == event.channel_id)

   for player in players:
      user = await client.get_user_info(player.id)
      await client.send_message(destination=user, content=getMessageForTime(reminder, event, player))

   markReminderSent(reminder, event.channel_id)

def columFromNumber(reminder):
   if reminder == 0:
      return "first_reminder_sent"
   elif reminder == 1:
      return "second_reminder_sent"
   elif reminder == 2:
      return "third_reminder_sent"
   elif reminder == 3:
      return "fourth_reminder_sent"

def reminderSent(reminderNumber, eventID):
   reminder = session.query(Reminder).filter(Reminder.id == eventID).filter(text(columFromNumber(reminderNumber))).one_or_none()
   return reminder

def getTimeRange(event):
  eventDay = str(event.event_day).split()[0]
  eventTime = str(event.event_time).split()[1]
  dateString = eventDay + eventTime
  eventDate = datetime.datetime.strptime(dateString, "%Y-%m-%d%H:%M:%S")
  timeinTwoDays = datetime.datetime.now() + timedelta(hours=48)
  timeinOneDay = datetime.datetime.now() + timedelta(hours=24)
  timeinTwoHours = datetime.datetime.now() + timedelta(hours=2)
  timeinFifteenMinutes = datetime.datetime.now() + timedelta(minutes=15)
  now = datetime.datetime.now()

  if timeinTwoDays >= eventDate > timeinOneDay:
     return 0
  elif timeinOneDay >= eventDate > timeinTwoHours:
     return 1
  elif timeinTwoHours >= eventDate > timeinFifteenMinutes:
     return 2
  elif timeinFifteenMinutes >= eventDate > now:
     return 3
  else:
     return 4


async def checkReminders():
   events = getEventsToRemind()

   for event in events:
      timeRange = getTimeRange(event)
      if timeRange < 0 or timeRange > 3:
         continue
      eventID = event.channel_id
      if not reminderSent(timeRange, eventID) or None:
         await sendReminder(timeRange, event)


def getEventsToRemind():
   timeInTwoDays = datetime.datetime.now() + timedelta(hours=48)
   events = session.query(Event).filter(Event.active == True) \
      .filter(timeInTwoDays >= Event.event_day).all()
   return events


async def runClient():
   await client.wait_until_ready()
   while not client.is_closed:
      print("Current servers:")
      await checkReminders()
      for server in client.servers:
         print(server.name)
      print('------')
      await asyncio.sleep(600)


client.loop.create_task(runClient())
client.run(BOT_TOKEN)
