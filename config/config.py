import logging
import os
import platform
import sys
import time


# Constants
AERIANA_ID = 289942088596979713
have_run = False
is_toy = False
is_creation_event = False
is_editing = False
message_user_timeout = 900
signups_enabled = {}

TESTING_SERVER_ID = 373782910010130442
INCURABLE_SERVER_ID = 269224197299896320
SKEEVERS_SERVER_ID = 260640164618043392

INCURABLE_BOT_SPAM_ID = 480506881237057566
SKEEVERS_BOT_SPAM_ID = 394250756183687169
TESTING_BOT_SPAM_ID = 518513396484800512

PLAYER_ROLES = {
    'tank',
    'healer',
    'mdps',
    'rdps',
    'reserve'
}

PLAYER_ROLES_DATA = {
    'tank': {
        'emoji': ':shield:',
        'display_name': 'Tank'
    },
    'healer': {
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
    'reserve': {
        'emoji': ':fingers_crossed:',
        'display_name': 'Reserve'
    }
}
DISCORD_ROLES_RANKED = {
    'High Queen': 1,
    'The Hand': 2,
    'Owner': 3,
    'Thane': 4,
    'officers': 5,
    'Aesir': 6,
    'Valkyrie': 7,
    'Shieldbreaker': 8,
    'Marauder': 9,
    'Citizen': 10,
    'Thrall': 11,
    'Active': 12,
    '@everyone': 13
}

if platform.system() == 'Windows':
    DEBUG = True
elif platform.system() == 'Linux':
    DEBUG = False
else:
    sys.exit("This is an unsupported system")

if DEBUG:
    logging.basicConfig(filename='Asuna.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    BOT_TOKEN = os.environ['DEBUG_API_TOKEN']
    COMMUNICATION_CHANNEL_ID = 543925704358756352
else:
    # Setup Proper Time Zone
    os.environ['TZ'] = 'America/Chicago' #Equivalent to the deprecated US/Central
    time.tzset()
    logging.basicConfig(filename='../Asuna.log', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    BOT_TOKEN = os.environ['PROD_API_TOKEN']

    # Asuna-communications channel
    COMMUNICATION_CHANNEL_ID = 544214746249822209


def init():
    pass
