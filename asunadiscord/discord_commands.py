from discord.abc import PrivateChannel

from asunadiscord.discord_client import client
from config.utilities import disappearing_message, check_permissions
from guildevents.edit_event import perform_event_edit, edit_selector_menu
from guildevents.event_creation import perform_event_creation
from guildevents.event_utilities import perform_show_event_details, perform_show_player_events
from guildevents.promotions import check_promotions
from guildevents.reminders import check_reminders
from guildevents.signups import perform_cancel_signup, perform_player_signup


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

    await perform_player_signup(message, context, player_role, *flex_roles_args)


@client.command(name='edit',
                description='Edits the event in the current channel.',
                brief='Edits this event.',
                pass_context=True)
async def edit_event(context):
    delete_message_after = 5
    officer = await check_permissions(context)
    if not officer:
        return

    message = context.message

    # we do not want the bot to reply to itself
    if message.author == client.user:
        return

    await perform_event_edit(officer, context, delete_message_after, message)


@client.command(name='event',
                aliases=['event-create'],
                description='Creates an event, and a new channel for that event.',
                brief='Create an event',
                pass_context=True)
async def create_event(context):
    officer = await check_permissions(context)
    if not officer:
        return

    delete_message_after = 5

    await perform_event_creation(context, officer, delete_message_after)


@client.command(name='event-details',
                description='Check details for this event.',
                brief='Check details for this event.',
                pass_context=True)
async def show_event_details(context, extra=None):
    await perform_show_event_details(context, extra)


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
    officer = await check_permissions(context)
    if not officer:
        return
    delete_message_after = 5
    await context.channel.send(f"行く！{officer.mention} A request to run a check for all reminders was initiated!",
                               delete_after=10)
    await disappearing_message(context.message, delete_message_after)
    await check_reminders()


@client.command(name='myevents',
                description='Shows events you signed up for.',
                brief='Shows events you signed up for.',
                pass_context=True)
async def show_player_events(context):
    await perform_show_player_events(context)


@client.command(name='cancel',
                description='Cancels your signup for the current event.',
                brief='Cancel signup',
                pass_context=True)
async def cancel_signup(context):
    await perform_cancel_signup(context)


@client.command(name='promotionCheck',
                description='Initiates a command to check users for eligible promotions now',
                brief='Checks promotions',
                pass_context=True)
async def check_promotions_now(context):
    officer = await check_permissions(context)
    if not officer:
        return

    delete_message_after = 5
    await context.message.channel.send("A request to run a check for promotions was initiated", delete_after=10)
    await disappearing_message(context.message, delete_message_after)
    await check_promotions()


def init():
    pass
