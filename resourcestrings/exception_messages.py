creation_event_day_exception = "ごめんなさい, you entered the date in an unrecognized format, try again with MM/DD/YYYY"

creation_event_time_exception = "ごめんなさい, you entered the time in an unrecognized format, try again with HHHH (24 Hour)"

creation_rank_exception = """ごめんなさい, you entered an unrecognized minimum rank, please enter one of the following **exactly** as written:
Valkyrie, Shieldbreaker, Marauder, Citizen, Thrall, Follower, @everyone"""

creation_canceled_exception = "Event creation has been canceled."

creation_timeout_exception = """ごめんなさい！I timed out waiting for a response to that last question (I can't wait forever, it causes my server to crash! :sob:). 
Please try creating the event again, but try to reply within 5 minutes."""

no_space_in_signup_exception = "Try it again, but without a space between the ? and the x (e.g. ?x rdps)"

missing_permission_exception = """失礼します This function requires a Moderator, or Admin."""

operation_not_permitted_in_dm_exception = """失礼します you can't do that operation from a private message (it's a Discord limitation)."""

creation_database_commit_exception = "There was an error saving the event to the database, let Aeriana know!"

incorrect_menu_option_exception = "Not an option, please select an available option from the menu."

no_event_for_channel_exception = "せみません, it looks like there wasn't an event created for this channel."

saving_event_edit_exception = "There was an error trying to edit this event, please try again."

edit_event_timeout_exception = """Are you still there? It looks like you might have finished editing, but forgot to enter the **Finished editing** option to close out my editing function. 
I get tired when I have to run constantly, and Aeriana has to pay me more :sweat_smile:. 
If you were in the middle of editing something, don't worry, I've saved your progress up to now, but I'm going to go take a nap for a bit.
If you want to restart editing, just rerun the edit command from the channel you want to edit, and we can pick back up where we left off :slight_smile:."""

edit_event_description_too_long_exception = """
**ERROR!!!**

While I've saved your edited event information, when attempting to post the new updated information into the event channel, Discord has informed me that the entire message (Date + Time + Leader + Description + Roster + Rank) is too long (over 2,000 characters- I know it's not very much, but I didn't make the rules) :sob: 

**Until the message is below the hard character cutoff, I can't update the event message at all.** 

Please re-open the edit menu, and reduce the amount of information in the event message. The typical culprit is the description, you might want to start there.
If after cutting down on the information, and you're still having issues, let Aeriana know, otherwise, good luck!"""