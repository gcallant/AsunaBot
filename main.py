import asunadiscord
import config
from asunadiscord.discord_client import client
from config.config import BOT_TOKEN

config.__init__()
asunadiscord.__init__()
client.run(BOT_TOKEN)
