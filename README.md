# Asuna
This bot is primarily intended to help ESO guild leaders and officers manage trials more effectively.
Although primarily intended to help with trials, it could be used in other ways to run and manage events.

## Features
### Allows users to signup for their preferred role(s) quickly and easily
*?x mdps heals* 

Will sign up a user as a melee dps, with an optional healer flex role.

### Sends event reminders
Users will receive a total of four reminders per event 
(48 hours before, 24 hours before, 2 hours before, and 15 minutes before). Users can optionally silence 
these notifications by muting the bot (not blocking though, as this will prevent signups,
since the bot cannot read messages from blocked users).

### Powerful administration functions
Admins can quickly and easily create and edit events, as well as generate user reports based on previous event signups.

## Feature Requests
Since Asuna 1.0 (Python) is in a stable condition at the moment, and my goal is to get version 2.0 released ASAP
(web version with a Discord API)- I cannot unfortunately add any large features to the codebase, but feel free to open
a Feature Request issue in GitHub, and I will take a look at it.

## Contributions
I am not seeking any contributions at the moment, but if you have a feature request, you can open a new issue, 
or if you have a burning desire to fix a bug or add a feature, feel free to submit a pull request. If it meets my
standards, I will accept it. Please try to abide by PEP guidelines whenever possible. Comments are helpful, but don't
go overboard. Try to make it clear from your functions and variables what your code is doing as much as possible.
(I don't wish to be a hypocrite here, I realize there are several areas in my code that could use some love :). 
My goal is to however reduce the Python code to an API Discord liaison, and move all business logic over to the new 
Laravel backend with a fancy Vue SPA frontend.)

## Installation
Development was done in **Python 3.9.6**, however you may succeed in using an older version of Python. If you have any issues
running the code or resolving dependencies, I would first recommend updating your version of Python before opening an issue.
Asuna relies on the Discord and Discord.py libraries. Other dependencies are located in the *requirements.txt* and can
be easily installed using PIP.

### Cloning the repository and installing dependencies
1. Install Python (>= 3.9.6 recommended) and ensure it is added to your PATH as a system environment variable 
   (or you can optionally run from a Python virtual environment).
2. Ensure PIP is installed. PIP is usually installed along with Python.
3. Clone the repository by either downloading it as a ZIP archive and unzipping or using `git clone` directly.
4. Navigate to the root of the repository in the command line (CMD or Git Bash).
5. Run the command `pip install -r requirements.txt --user`. This will install all the Python module dependencies for the project.

### Running Asuna
1. First you will need a Discord bot token. This can be obtained from the Discord developer portal.
2. Add a system environment variable with the <K,V> of <PROD_API_TOKEN, token> or <DEBUG_API_TOKEN, token> 
   (depending on your environment- currently Linux defaults to prod, and Windows as debug, but these can be adjusted in config.py). 
   Or, you can inject the token into the config.py file directly: BOT_TOKEN= < your bot token > (not recommended, as this is 
      present in the codebase).
3. You will need to generate an OAuth2 invite from the Discord developer portal in order to add the bot to your Discord server.
4. On the command line, run `python main.py`. This will start the bot in your Discord server. 
   You should see debug output in the console.
5. You will notice in the config.py several dictionaries. One of these is named DISCORD_ROLES_RANKED. Since Asuna was 
   originally intended for use only in our guild (and later expanded to function for a handful of guilds), these roles work 
    for these guilds. You will need to create these same roles in your Discord to match this dictionary, or edit the 
   dictionary with your server's roles. You will also need to update the function officer() in utilities.py to match
    the **lowest officer rank** you wish to grant permissions to, in order for permissions to function correctly.
   I realize this is less than ideal, but version 2.0 is designed to accommodate many guilds with many more configurable options. 

## Asunaweb
Asunaweb (or Asuna 2.0) is the framework for moving Asuna from a simple Python tool to a full site with many added features 
not currently possible in the command-line only Discord interface. It is currently being built,
and it will use PHP Laravel for the backend API, and Vue for the frontend. The Python functionality will be kept, but will be 
reduced to mostly interfacing with the Discord API, and allowing legacy access to the Discord command-line version
that most users are familiar with. I don't have an ETA for when it will be completed, but hopefully early-mid 2022.
There will likely be a beta testing phase before full public release. If you are interested in joining the beta when it is 
released, you can fill out this 
[Google Form located here](https://docs.google.com/forms/d/e/1FAIpQLSf3Yab-g_jIHikzKekDzc989gmdUAYYJxcA5mfgtm3Y_aHUlw/viewform?usp=sf_link).
