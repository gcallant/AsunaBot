import logging
import os
import platform
import sys

# Constants
import time

AERIANA_ID = 289942088596979713
have_run = False
is_toy = False
is_creation_event = False
is_editing = False
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
    'Follower': 10
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
else:
    # Setup Proper Time Zone
    os.environ['TZ'] = 'America/Chicago' #Equivalent to the deprecated US/Central
    time.tzset()
    logging.basicConfig(filename='../Asuna.log', format='%(asctime)s - %(levelname)s - %(message)s',
                        level=logging.INFO)


def init():
    pass
