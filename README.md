# Layla II
Layla II is a Discord bot intended to replace the Groovy and Rythm bots that were shut down by YouTube, with ranking features included. Python 3.8+, discord.py, youtube-dl, and ffmpeg are needed to run the bot. This bot is not capable of functioning in multiple servers and is designed with the intent for use in a single server, both for ease of programming and to not be abused like Groovy and Rythm were.
Layla II is named after an old bot named Layla that I attempted to write in discord.js. Though that went nowhere, the removal of Groovy and Rythm inspired me to reattempt it, this time in my native language, Python.

## Features
The primary features of Layla II are music streaming and a ranking system. Starting with the music, the bot can play the audio of any public and non-age-restricted YouTube video. The music is played by querying the song title or by providing a URL. The youtube-dl library is used to search YouTube and retrieve the info of the top result. The ffmpeg library is used to stream the audio. The bot has a queue system that can contain up to 20 songs (queue length can of course be changed). The bot is incapable of both playing the next song in the queue authomatically after the current one ends and skipping to the next song on command. I chose to sacrifice automatic playing to preserve on-command skipping, meaning that going down the queue takes one more command than Groovy and Rythm (I tried for many hours to get both to work, but the way that Python nests async functions seems to make that impossible). For a server as small as the one that I made Layla II for, this is not a large issue. The bot can also display the progress of, pause, resume, and loop the current song on command.

Onto ranking, the bot is designed with a single server in mind and so cannot log xp and ranks for multiple servers. The bot increases a user's xp every time they send a message after a cooldown after their last message. Unlike the AmariBot that has a paid program that allows administrators to change the cooldown, Layla II can change the cooldown for free! The rate at which users level up is linear and the rate of leveling up can be changed. Users can see their xp and rank on command as well as see a leaderboard of the top 10 users with the most xp. Administrators can assign levels to users and users can give themselves color roles. The bot will give a user ranking roles if they reach xp thresholds. Any role related stuff is hard coded.

The bot has other extraneous commands that I added for fun, including text manipulation, copypastas, and reaction images/videos. The init.py file reads a local txt file to obtain the token and obtains saved user data and the message cooldown in the same way (users.txt is not present in the repo for privacy reasons). If you want to plug this code into your bot, make a txt file with your token and read from it in init.py. Then run main.py to run your bot. There are many resources to help you set up a bot with Discord's developer API If you happen to find this GitHub page, you are free to do whatever you wish with my code. This is a project that I took on to kill time and get better at Python,  so I don't care about what you do with it. Read the MIT license for the specifics.

## Using Layla II

### Install Packages
A Python interpreter, discord.py, youtube-dl, and ffmpeg are needed to run the bot. The most recent stable version of Python is recommended at [python.org](https://www.python.org/downloads/). 3.8 is the oldest usable version. discord.py can be installed using `pip` with Rapptz' guide on his [GitHub page](https://github.com/Rapptz/discord.py). youtube-dl and ffmpeg will have to be installed according to your operating system and a `pip install` of these packages may also be necessary.

### Create Discord Bot
To create your bot, go to the [Discord developer portal](https://discord.com/developers/) and log in. Click `New Application` and give it a name. Under application settings, select `Bot` and click `Add Bot`. Here you can give a bot a separate name from the application. Go to `OAuth2` and under scopes select `bot`. You can select the bot's permissions here as well if you like, selecting `Administrator` is usually fine. Copy the OAuth2 URL and enter it in a new tab. This will invite the bot to your server and it will be offline. 

### Customization
After this, get the code from this repo is whatever way you wish and make sure to add `users.txt`, `cooldown.txt`, `rate.txt`, and `prefix.txt` in the same directory. `users.txt` can be left empty but the other three files need starting data. Pick a number between 1-10 for `cooldown`, a number between 10-20 for `rate`, and any 1-6 character string for `prefix`. The bot is run by giving its token to the code, allowing it to connect to Discord's bot API. In the developer portal, go back to the `Bot` tab and copy its token. Do not post this token anywhere on the internet as Discord will notice and change it. You can either save the token as an environment variable or on a local txt file. The easiest way is with a text file somewhere on your local machine that you can read from in `init.py`. The ranking roles and thresholds are hard coded in `init.py` in the `on_message` listener. A template set of ranking roles is given in a docstring here and is where you would add the ranking roles for your server. The message cooldown and prefix can be changed with the `cooldown` and `prefix` commands respectively. The rate at which users level up is proportional to their xp, as `(xp needed to level up) = (rate of level up) * (current level + 1)`. The rate of level up can also be changed with the `changerate` command. These commands can only be used by server administrators. If you want to further make your bot your own by changing the code, you are free to do so. If so, I suggest reading the [Layla II Verbose Documentation](https://github.com/suranwarnakulasooriya/LaylaII/wiki/Layla-II-Verbose-Documentation) to better understand the ins and outs of the code.

### Troubleshooting
Occasionally, the music commands will fail to work. youtube-dl, ffmpeg, and discord.py as a whole require a good internet connection to run, as a bad connection may prevent the bot from joining voice at all. The time it takes for the audio libraires to retrive the vidoes varies but is usually close to proportional with the length of the song. Sometimes the ffmpeg request is denied entirely and the audio won't play (the output window will show this). Requeue the song and skip to it to make it play normally. If in any case the current song (labeled by "<==" in the queue) is not correct, use `setcurrent` to fix it. If you don't know how to solve an audio issue, use `leave` to clear the queue and leave the voice channel, then rejoin the bot. If this does not work, the bot needs to be restarted. Disconecting the bot from a voice channel or using music/ranking commands in DMs can potentially cause this. 

### Commands List (Music & Ranking)
```python
# Music
play(query) # plays + enqueues the queried song, will adjust if not in voice or if a song is already playing
queue() # shows the queue
join() # joins the voice channel of the author 
leave() # leave voice and clear the queue
pause() # pause audio
resume() # resume audio after pause
stop() # stops audio without the ability to unpause
next() # to progress to the next song in the queue
remove(index) # remove any valid index in the queue
clear() # clears queue but stays in voice
loop() # toggle whether currint song is looping (if true, next will restart the song instead of go the the next one)
jump(index) # skip to a given index in the queue
np() # see the progress of the current song
setcurrent(index) # manually set the current song in the queue if wrong

# Ranking
rank() # see your level and xp 
cooldown(newcooldown) # (admin only) change the cooldown from 1-10
getcooldown() # see what the current cooldown is without changing it
leaderboard() # show the top 10 users with the most xp
givelevel(user,level) # (admin only) assign a level to a user (changes xp accordingly)
changerate(rate) # (admin only) change the rate at which users level up
getrate() # see the current level up rate
```
