from sqlalchemy import true

from asunadiscord.discord_client import client
from config.asunabot_declative import Event, PlayerSignup
from config.config import PLAYER_ROLES_DATA
from config.database import session
from config import utilities, config
from config.utilities import disappearing_message, send_message_to_user


async def get_event_details(event_id, context, extra=None):
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
                        f'\t {signup.player_mention} {"(Can Flex: " + signup.flex_roles + ")" if signup.flex_roles else ""} (Rank:{await utilities.get_highest_discord_role(int(signup.id), context)}) {signup.date_created.strftime("- %Y-%m-%d %H:%M") if extra == "extra" else ""}'
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


async def perform_show_event_details(context, extra):
    author = context.message.author
    event_details = get_event_details(context.message.channel.id, context, extra)
    await disappearing_message(context.message, time_to_wait=5)
    await send_message_to_user(author, event_details)


async def perform_show_player_events(context):
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


def validate_min_rank(rank, format=None):
    """
    # Tries rank in the dictionary, if rank doesn't exist, throws and rethrows exception
    :param rank:
    :param format:
    :return: rank, or throws ValueError
    :raises: ValueError if rank doesn't exist in dictionary
    """

    try:
        _ = config.DISCORD_ROLES_RANKED[rank]
        return rank
    except KeyError:  # Keeps our function with only one exception
        raise ValueError


async def update_channel_info_message(event_id, context):
    event = session.query(Event).get(event_id)
    channel = client.get_channel(event_id)
    channel_message = await channel.fetch_message(event.channel_info_message)
    new_message_content = f'@everyone\nDate: {str(event.event_day).split()[0]}\nTime: {str(event.event_time).split()[1]} Central\n{event.event_description}\n\nRaid Leader:{event.event_leader} \n\n\n{await get_event_details(event_id, context)}\n\nMinimum Rank: {event.min_rank}\nIf you are not this rank, you may still signup, but you will be listed as reserve.'
    await channel_message.edit(content=new_message_content)
    event.channel_info_message = channel_message.id
    session.commit()
