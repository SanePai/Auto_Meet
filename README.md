Pulls all meetings from google calendar  
Joins and exits them at specific times
Meet link must be in the location field of the event  


Meet enchancement extension is needed to turn off mic and camera.(https://www.meetenhancementsuite.com/)

Steps:(1-6 are only for the first time)
1. Enable Calendar API and add the credentials.json file into the directory
2. Make sure that the auto mic and cam off options are enabled in the meet enchancement extension
3. run "pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib notify-run" without the quotation marks.
4. add chrome to PATH (google for steps if needed).
5. run "chorme --remote-debugging-port=<port number> --user-data-dir=<user_data_dir_path> and sign in using the google account that is used to join meetings. port number is 6942 by default. If you change that make sure to change it in the settings.json as well. Create a new folder somewhere in your system. That folder path will be user_data_dir_path.
6. run "notify-run register" to create a channel for notifications. Scan the QR or go to the link in a browser on your phone(or any device) and subscribe for notifications.
7. Navigate to the directory and run the Main.py file (python Main.py or python3 Main.py). First time run will open a oauth window in your browser.(Delete token.pickle if you wish to change the account in the future)

Settings:  
weekdays: Weeks start on Monday by default. set to any number between 1 and 6  
elementPaths: element paths in the html source for google meet  
defaults:  
    defaultPort: default debugging port selenium. default=6942  
    seleniumExecutable: selenium driver path  
    seleniumProfile: selenium profile folder path  
    sleepUpdateTime: long sleep times are continually updated after a set duration instead of one long sleep.Low update time might affect performance. value is in seconds. default=600s (10 minutes)  
    muteAudio: mute the audio of the meet site. default=true   
    minimizeWindowAfterJoin: minimize window after joining the class. the tab needs to be in focus to allow the mic and cam to be switched off automatically by the meet enchancement extension.  
   
Work in progress:  
    remove dependency on meet enhancement extension  
    record.py - record meetings (ideally using OBS).  
