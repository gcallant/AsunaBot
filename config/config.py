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
    'Thane': 3,
    'Aesir': 4,
    'Valkyrie': 5,
    'Shieldbreaker': 6,
    'Marauder': 7,
    'Citizen': 8,
    'Thrall': 9,
    'Follower': 10,
    '@everyone': 11
}

if platform.system() == 'Windows':
    DEBUG = True
elif platform.system() == 'Linux':
    DEBUG = False
else:  # I don't know what the hell is going on
    sys.exit("This is an unsupported system")

if DEBUG:
    logging.basicConfig(filename='Asuna.log', filemode='w', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.DEBUG)
    BOT_TOKEN = 'NTE5NzA2ODQ4NTg1MTg3MzMy.DujPDg.5kr_-LfnCUeRLTR23yaqFY97OWo'
    COMMUNICATION_CHANNEL_ID = 543925704358756352
else:
    # Setup Proper Time Zone
    os.environ['TZ'] = 'America/Chicago' #Equivalent to the deprecated US/Central
    time.tzset()
    logging.basicConfig(filename='../Asuna.log', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)
    BOT_TOKEN = 'NTE4NTUzNTcyNDI2NjQ1NTA0.DuShbw.TwNTD0i5vvgjbM27QtHCYG3vY44'

    # Asuna-communications channel
    COMMUNICATION_CHANNEL_ID = 544214746249822209


def init():
    pass
