import csv
from typing import List

import discord
from beautifultable import BeautifulTable
from discord import File, Member

from config.asunabot_declative import PlayerSignup, Event
from config.database import session
from config.utilities import send_message_to_user
from resourcestrings import report_messages


async def run_audit_report(officer, channel: discord.TextChannel):
    members: List[Member] = channel.guild.members

    with open('report_file.csv', mode='w', encoding='utf8') as report_file:
        report_writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        report_writer.writerow(['Display Name', 'Nick Name', 'Date Joined', 'Roles'])

        for member in members:
            report_writer.writerow(
                [f'{member.display_name}', f'{member.nick}', f"{member.joined_at.astimezone().isoformat()}",
                 f'{[role.name for role in member.roles]}'])

    await send_csv_report(officer)


async def perform_report(context, report_to_run: str, user_id: int, officer, report_format):
    channel = context.channel
    time_to_delete = 10

    if report_to_run == '':
        await channel.send(report_messages.report_type_needed, delete_after=time_to_delete)
    elif report_to_run == 'user':
        if user_id is None:
            await channel.send(report_messages.user_id_needed, delete_after=time_to_delete)
            return
        else:
            await run_user_report(channel, officer, user_id, report_format)
    elif report_to_run == 'audit':
        await run_audit_report(officer, channel)


async def get_user_report(user_id):
    return session.query(PlayerSignup).join(Event).filter(PlayerSignup.id == user_id) \
        .order_by(Event.event_day.asc()).all()


async def run_user_report(channel, officer, user_id: int, report_format):
    report = await get_user_report(user_id)

    if len(report) == 0:
        await channel.send(report_messages.user_not_found, delete_after=10)
        return

    if report_format == 'csv':
        await generate_csv_report(officer, report)
    elif report_format == 'message':
        await generate_message_report(officer, report)
    else:
        await channel.send(report_messages.report_format_unknown_option, delete_after=10)


async def send_csv_report(officer):
    file = File('report_file.csv', 'report.csv')
    await send_message_to_user(officer, 'Your report', file=file)


async def generate_csv_report(officer, report):
    with open('report_file.csv', mode='w', encoding='utf8') as report_file:
        report_writer = csv.writer(report_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

        report_writer.writerow(["Player Name", "Role", "Event Name", "Event Date"])

        for run in report:
            report_writer.writerow([f'{run.player_name}', f'{run.player_roles}', f'{run.event.event_name}',
                                    f'{str(run.event.event_day).split()[0]}'])

    await send_csv_report(officer)


async def generate_message_report(officer, report):
    table = BeautifulTable()
    table.column_headers = ["Player Name", "Role", "Event Name", "Event Date"]
    table.column_widths['Event Name'] = 50

    for run in report:
        if len(table.get_string()) > 1800:  # Discord's character limit is 2k, so send and clear our table
            await send_message_to_user(officer, table)
            table = None
            table = BeautifulTable()
            table.column_headers = ["Player Name", "Role", "Event Name", "Event Date"]

        table.append_row([f'{run.player_name}', f'{run.player_roles}', f'{run.event.event_name}',
                          f'{str(run.event.event_day).split()[0]}'])

    await send_message_to_user(officer, table)
