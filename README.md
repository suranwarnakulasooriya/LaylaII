# Layla II
Layla II is a Discord bot intended to replace the Groovy and Rythm bots that were shut down by YouTube, with ranking features included. Python 3.5+, discord.py, youtube-dl, and ffmpeg are needed to run the bot. This bot is not capable of functioning in multiple servers and is designed with the intent for use in a single server, both for ease of programming and to not be abused like Groovy and Rythm were.

Layla II is named after an old bot named Layla that I attempted to write in discord.js. Though that went nowhere, the removal of Groovy and Rythm inspired me to reattempt it, this time in my native language, Python.

## Music
The primary features of Layla II are music streaming and a ranking system. Starting with the music, the bot can play the audio of any public and non-age-restricted YouTube video. The music is played by querying the song title or by providing a URL. The youtube-dl library is used to search YouTube and retrieve the info of the top result. The ffmpeg library is used to stream the audio. The bot has a queue system that can contain up to 20 songs (queue length can of course be changed). The bot is incapable of both playing the next song in the queue authomatically after the current one ends and skipping to the next song on command. I chose to sacrifice automatic playing to preserve on-command skipping, meaning that going down the queue takes one more command than Groovy and Rythm (I tried for many hours to get both to work, but the way that Python nests async functions seems to make that impossible). For a server as small as the one that I made Layla II for, this is not a large issue. The bot can also display the progress of, pause, resume, and loop the current song on command.

## Ranking
Onto ranking, the bot is designed with a single server in mind and so cannot log xp and ranks for multiple servers. The bot increases a user's xp every time they send a message after a cooldown after their last message. Unlike the AmariBot that has a paid program that allows administrators to change the cooldown, Layla II can change the cooldown for free! The rate at which users level up is linear and the rate of leveling up can be changed. Users can see their xp and rank on command as well as see a leaderboard of the top 10 users with the most xp.

### The Rest
The bot has other extraneous commands that I added for fun, including text manipulation, copypastas, and reaction images/videos. These commands (along with the music and ranking commands) are kept in separate Python files that are imported into commands_all.py (which is then imported into main.py), so you can edit commands_all.py to add/remove groups of commands that you do not want. 

The init.py file reads a local txt file to obtain the token. If you want to plug this code into your bot, make a txt file with your token and read from it in bot_info.py. Then run main.py to run your bot. There are many resources to help you set up a bot with Discord's developer API.

If you happen to find this GitHub page, you are free to do whatever you wish with my code. This is a project that I took on to kill time and get better at Python,  so I don't care about what you do with it. Read the MIT license for the specifics.
