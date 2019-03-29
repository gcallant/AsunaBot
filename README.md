# AsunaBot
Originally created by Synthrelik and taken over by AerianaFilauria, this bot is intended for use by Incurable Insanity admins to assist in creating and leading trials and other events.

## Installation

**This guide assumes your developer environment is Windows.**

### Python 3.6
*But I already have a different version of Python!*

**AsunaBot requires Python 3.6 - don't worry, it won't overwrite your other install.**

1. [Click here to download the Python 3.6 installer.](https://www.python.org/ftp/python/3.6.0/python-3.6.0-amd64.exe)
2. Run the installer.
3. Navigate to `python.exe` (by default this is `C:\Users\<user>\AppData\Local\Programs\Python\Python36\python.exe`) and rename it to `python36.exe` (Optional, but recommended)
4. Take note of the python executable file's location.
5. Search Windows for `Edit the system environment variables`.
6. Click `Environment Variables`
7. Select the `Path` variable in the upper box and click `Edit`.
8. Click `New` and paste in the full path of the python executable file. By default this is `C:\Users\<user>\AppData\Local\Programs\Python\Python36\python.exe` (Note that renaming this file in step 3 will change the name of this file.)
9. Click `Ok` in both windows. You can now close the System Settings window as well.

### AsunaBot
1. Clone the repository by either downloading it as a ZIP archive and unzipping or using `git clone` directly.
2. Navigate to the root of the repository in the command line (CMD or Git Bash).
3. Run the command `python36 -m pip install -r requirements.txt --user`. This will install all the Python module dependencies for the project.


### Running AsunaBot
On the command line, run `python36 asunabot.py`. This will start the bot and connect it to the Memoize Discord server for testing. You should see debug output in the console.
