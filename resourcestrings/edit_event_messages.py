menu = """Please enter the number of the operation you would like to perform.

**IMPORTANT:** When finished editing, please make sure you select option **Finished editing** to ensure the channel is updated.
Any edits you make will be saved along the way, but you will not see the edits updated in the channel until you select **Finished editing**.

**1**: Edit **name** of the event
**2**: Edit **date** of the event
**3**: Edit **time** of the event
**4**: Edit **trials** you plan to run
**5**: Edit event **leader**
**6**: Edit number of **tanks**
**7**: Edit number of **healers**
**8**: Edit number of **mDPS**
**9**: Edit number of **rDPS**
**10**: Edit event **description**
**11**: Edit minimum event **rank**
**12**: Edit **player roster**
**13**: **Finished** editing

To **return** to a previous menu during an edit, type *?return*, or to **cancel** editing at any time, type *?cancel*

"""

goodbye = "ありがとごじいます。では、失礼いたしました。:wave:"

menu_return = " Type ?return to return to the previous menu.\n"

name = "Sure! What do you want to call the event?\n"

date = "Sure! What new date do you want to set?\n"

time = "Sure! What new time do you want to set?\n"

trials = "Sure! What new trials do you want to run?\n"

leader = "Sure! Who do you want to be the new leader?\n"

tanks = "Sure! What is the max number of tanks you want?\n"

healers = "Sure! What is the max number of healers you want?\n"

mdps = "Sure! What is the max number of melee DPS you want?\n"

rdps = "Sure! What is the max number of ranged DPS you want?\n"

rank = "Sure! What is the new minimum rank you want to allow to signup?\n"

description = """Sure! What would you like the new event description to be? 
*(Just keep in mind, Discord still limits this to 2,000 **characters** [not words], and this also has to include the actual player_roster, so don't make it too long!)*

""" + menu_return

cancel_edit = "No problem, canceled editing this event. To restart, just re-type ?edit into the channel you wish to edit."

event_name_edited = "良いですよ, event **name** has been updated!\n"

event_time_edited = "良いですよ, event **time** has been updated!\n"

event_trials_edited = "良いですよ, the **trials** have been updated!\n"

event_leader_edited = "良いですよ, the event **leader** has been updated!\n"

event_tanks_edited = "良いですよ, the max number of **tanks** has been updated!\n"

event_healers_edited = "良いですよ, the max number of **healers** has been updated!\n"

event_mdps_edited = "良いですよ, the max number of **mDPS** has been updated!\n"

event_rdps_edited = "良いですよ, the max number of **rDPS** has been updated!\n"

event_rank_edited = "良いですよ, the minimum **rank** has been updated!\n"

event_description_edited = "良いですよ, the event **description** has been updated!\n"

edit_roster_menu = """Please enter the number of the operation you would like to perform.

**1**: **Add** someone to an event
**2**: **Remove** someone from an event
**3**: **Edit** A signed up user's role
**4**: **Toggle Signups** On or off *(preventing people from signing up)*
**5**: **Return** to the previous menu

"""

user_to_signup = """Sure, who do you want to **signup**? 

You'll need to provide me their discord ID, in order for me to **sign them up** properly.
In order to do this, you'll need to enable Developer mode. 
First, click the Gear next to your icon at the bottom left corner of discord to open settings.
Next, click on Appearance, and scroll down to the **ADVANCED** section.
Finally, toggle the **Developer Mode** function to on. 
Now, all you need to do from here, is right click the user you want to **signup**, and click **COPY ID**.

"""

user_roles_to_signup = "What roles do you want them to have? (No flexing please!)"

user_to_remove = """Sure, who do you want to **remove** from the player_roster? 

You'll need to provide me their discord ID, in order for me to **remove** them up properly.
In order to do this, you'll need to enable Developer mode. 
First, click the Gear next to your icon at the bottom left corner of discord to open settings.
Next, click on Appearance, and scroll down to the **ADVANCED** section.
Finally, toggle the **Developer Mode** function to on. 
Now, all you need to do from here, is right click the user you want to **remove**, and click **COPY ID**.

"""

toggle_signup_option = """Sure, which option do you want?

**1**. Toggle Signups **On** (Allows Signups)
**2**. Toggle Signups **Off** (Prevents Signups)
**3**. Return to the previous menu

"""
