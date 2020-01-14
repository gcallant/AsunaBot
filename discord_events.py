# Constants
from builtins import client
from database import session
AERIANA_ID = 289942088596979713


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


@client.event
async def on_message(message):
    if message.content.lower().startswith("? x"):
        await message.channel.send(f"{message.author.mention} Try it again, but without a space between the ? and the "
                                   f"x (e.g. ?x rdps)", delete_after=10)
        await disappearing_message(message)
        return
    elif message.content.startswith("?"):
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
                await send_message_to_user(author, "???????:scream: Why does everyone keep asking me about Trebusan?! "
                                                   ":flushed: I mean, I think he's a good looking guy, I do... but, "
                                                   "he's just not my type. ?????? Trebusan! :cow:")
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
                await send_message_to_user(author, "Hi to you too! Or as I would say in Japan, ?????! :smiley:")
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
    while not client.is_closed():
        print("Current servers:")
        await check_reminders()
        await check_promotions()
        for server in client.guilds:
            print(server.name)
        print('------')
        await asyncio.sleep(300)


def init():
    pass
