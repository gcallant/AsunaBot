from discord.abc import PrivateChannel

from admin.reporting import perform_report
from asunadiscord.discord_client import client
from config.config import signups_enabled
from config.utilities import disappearing_message, check_permissions, get_user
from guildevents.edit_event import perform_event_edit
from guildevents.event_creation import perform_event_creation
from guildevents.event_utilities import perform_show_event_details, perform_show_player_events
from guildevents.promotions import check_promotions
from guildevents.reminders import check_reminders
from guildevents.signups import perform_cancel_signup, perform_player_signup
from resourcestrings import exception_messages


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

    try:
        signup_enabled = signups_enabled[context.message.channel.id]
        if signup_enabled is False:
            await message.channel.send("すみません, signups are not enabled for this run. If you believe this is an error, "
                                       "please contact the raid lead.")
            return
        await perform_player_signup(message, message.author, context, player_role, *flex_roles_args)
    except:
        await perform_player_signup(message, message.author, context, player_role, *flex_roles_args)


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


@client.command(name='report',
                description='Creates a report based on specified parameters that you define. For example '
                            '?report user <userid> will create a report for user with an id of <userid>. '
                            'Allowed types are: user, audit',
                brief='Runs a report', pass_context=True)
async def run_report(context, report_to_run='', user_id: str = None, report_format='csv'):
    officer = await check_permissions(context)
    if not officer:
        return

    user = await get_user(context, user_id)
    if not user:
        return

    delete_message_after = 5
    report_to_run = str(report_to_run).lower().strip()
    report_format = str(report_format).lower().strip()

    await disappearing_message(context.message, delete_message_after)

    await perform_report(context, report_to_run, user.id, officer, report_format)


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


@client.command(name='proxy',
                description='Proxy performs a command for another user- can be used to quickly signup or remove '
                            'someone from player_roster. Usage- ?proxy <command> <user> [<signup role> [flex roles]]',
                brief='Performs a command for another user- **ADMIN use only**',
                pass_context=True)
async def proxy_command(context, command_to_run: str, user_id: str, role='', *player_flex_args):
    officer = await check_permissions(context)
    if not officer:
        return

    user = await get_user(context, user_id)
    if not user:
        return

    if command_to_run.lower().strip() in ["signup", "x", "X"]:
        await perform_player_signup(context.message, user, context, role, *player_flex_args, proxy_signup=True)
    elif command_to_run.lower().strip() in ["remove", "cancel"]:
        await perform_cancel_signup(context, user)
    else:
        await context.message.channel.send(exception_messages.unknown_proxy_command)


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
    await perform_cancel_signup(context, context.message.author)


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
