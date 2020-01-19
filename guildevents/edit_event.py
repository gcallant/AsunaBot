import logging

from config.asunabot_declative import Event
from config.database import session
from config.utilities import send_message_to_user, disappearing_message
from guildevents.event_utilities import update_channel_info_message


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


async def perform_event_edit(author, context, delete_message_after, message):
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