Dispenser.py:

Features:
```
-Logging user messages as pictures
-Reaction role assignment
-RNG
-Free epic games DM reminder
```

Dispenser takes the token as a cmd line argument.
```
python3 Dispenser.py TOKEN
```
Key lists:

```
self.target_ids = Messages for reaction roles. Add channel ID's to assign roles corresponding to emojis.
self.authors = Effective administrators of the bot. Add user ID's for users of all privileges.
self.users_game_reminder = Users to be reminded of new free epic games
self.logged_channels = A list of channel ID's to be logged
```
