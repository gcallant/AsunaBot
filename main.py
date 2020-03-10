# Original credit goes to Synthrelik for creating this bot
# Work continued on by Aeriana Filauria (and some help from Blitznacht112)
# To be used by Incurable Insanity admins for creating and leading trials and other events
import asunadiscord
import config
from asunadiscord.discord_client import client
from config.config import BOT_TOKEN

config.__init__()
asunadiscord.__init__()
client.run(BOT_TOKEN)
