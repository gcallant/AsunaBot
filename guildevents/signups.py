import logging

import discord

import config
from config import config
from config.asunabot_declative import Event, PlayerSignup
from config.config import PLAYER_ROLES
from config.database import session
from config.utilities import disappearing_message
from guildevents.event_utilities import update_channel_info_message


async def perform_cancel_signup(context, user: discord.user, admin_edit=False):
    event_id = context.message.channel.id
    player_id = user.id
    delete_message_after = 5
    existing_player_signup = session.query(PlayerSignup).get((player_id, event_id))
    if existing_player_signup:
        session.delete(existing_player_signup)
        session.commit()
        if not admin_edit:
            await context.message.channel.send(
                f'{user.mention}, you are no longer signed up for this event.',
                delete_after=10)
            await update_channel_info_message(event_id, context)
            await disappearing_message(context.message, delete_message_after)
    else:
        await context.message.channel.send(f'{context.message.author.mention}, you, or the user you entered are not '
                                           f'signed up for this event.',
                                           delete_after=10)
        await disappearing_message(context.message, delete_message_after)


async def perform_player_signup(message, user: discord.user, context, player_role, *flex_roles_args,
                                proxy_signup=False, admin_edit=False):
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
            await perform_cancel_signup(context, user)
            return

        # Allows users to also type heals or healer without adding an additional dictionary entry
        if cleaned_player_role == 'heals' or cleaned_player_role == 'heal':
            cleaned_player_role = 'healer'

        if cleaned_player_role in config.PLAYER_ROLES:
            cleaned_player_role, flex_roles = await do_signups_meet_minimum_standards(channel, cleaned_player_role,
                                                                                      event, flex_roles, message,
                                                                                      proxy_signup, admin_edit)

            if flex_roles_args:
                flex_roles = ' '.join(flex_roles_args).strip().lower() + ' ' + flex_roles
            existing_player_signup = session.query(PlayerSignup).get((user.id, event.channel_id))
            if existing_player_signup:
                existing_player_signup.player_roles = cleaned_player_role
                existing_player_signup.flex_roles = flex_roles
            else:
                new_player_signup = PlayerSignup(
                    id=user.id,
                    player_name=user.display_name,
                    player_mention=user.mention,
                    player_roles=cleaned_player_role,
                    flex_roles=flex_roles,
                    event=event,
                )
                session.add(new_player_signup)
            try:
                session.commit()
            except:
                session.rollback()
                logging.exception(f'We had an error trying to add {user.name} to the roster')
                await channel.send(f'ごめんなさい, {message.author.mention} '
                                   f'There was an error, please try again!', delete_after=10)
            if not admin_edit:
                await message.add_reaction('✅')
                await channel.send(f'{user.mention} You are now signed up as ' + cleaned_player_role.lower(),
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


async def do_signups_meet_minimum_standards(channel, cleaned_player_role, event, flex_roles, message,
                                            proxy_signup=False, admin_edit=False):
    if (channel.guild.id == config.TESTING_SERVER_ID or channel.guild.id == config.INCURABLE_SERVER_ID) and not (proxy_signup or admin_edit):  # Ignore all other servers
        if not cleaned_player_role == 'reserve' and \
                (config.DISCORD_ROLES_RANKED[message.author.top_role.name] > config.DISCORD_ROLES_RANKED[
                    event.min_rank]):
            await channel.send(f"ごめんなさい, you don't meet the minimum certified rank required for this run "
                               f"as a {message.author.top_role.name}. You'll be signed up as reserve.\nIf this is "
                               f"an error, "
                               f"please contact an officer.", delete_after=15)
            flex_roles = cleaned_player_role
            cleaned_player_role = "reserve"

            # More performance intensive search only for needed runs
        elif event.min_rank == "Shieldbreaker" and discord.utils.get(message.author.roles,
                                                                     name=cleaned_player_role) is None:
            await channel.send(f"ごめんなさい, you don't meet the minimum certified rank required for this run "
                               f"as a {cleaned_player_role}. You'll be signed up as a reserve.\nIf you are "
                               f"certified as a different role, "
                               f"please signup with a role you are certified for.\nIf this is an error, "
                               f"please contact an officer.", delete_after=15)
            flex_roles = cleaned_player_role
            cleaned_player_role = "reserve"

    return cleaned_player_role, flex_roles
