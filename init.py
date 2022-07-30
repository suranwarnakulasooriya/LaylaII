# ==============================================================================
# start everything up
# ==============================================================================

# discord.py
import discord
from discord.ext import commands
import os # for environment variables

import sys # to kill code
import functools # for help command

# different libraries are needed because only youtube-dl returns a URL that can be used by FFmpeg and only youtube_search can give multiple results
from youtube_dl import YoutubeDL # to get top YouTube search result in play command
from youtube_search import YoutubeSearch # to get multiple results in search command
from discord import FFmpegPCMAudio # to stream audio

# to keep alive 24/7
from flask import Flask
from threading import Thread

# for music duration and cooldown
from datetime import timedelta as td
import time

dir = "<directory>" # directory of all code files

class Bot_Info: # class with basic bot info
    def __init__(self,token):
        self.token = token
        self.connected = False
        with open(f'{dir}/data.txt','r') as f: data = f.read().split(); f.close()
        self.prefix = data[0]
        with open(f'{dir}/status.txt','r') as f: data = f.readlines(); f.close()
        self.acttype = data[0]
        self.status = data[1]

class Song: # class with repeatedly accessed song information
  def __init__(self,title,url,length,request,rawtime):
    self.title = title # title of youtube video
    self.url = url # url for ffmpeg to use
    self.length = length # duration in hh:mm:ss
    self.request = request # the user who requested the song
    self.rawtime = rawtime # duration in seconds
  def __repr__(self): return f"{self.title} : {self.url} : {self.length}"

class Queue: # class with repeatedly accessed queue information
  def __init__(self):
    self.queue = [] # list of Song objects
    self.loop = False # bool of whether the current song is looping or not
    self.current = 0 # index of current song in Q.queue
    self.search = []

class Stopwatch_: # for np and ranking
    def __init__(self):
        self.start = 0 # when song begins
        self.suspend = 0 # when paused
        self.downtime = 0 # total amount of time spent paused
        self.paused = False
    def Start(self):
        if not self.paused: self.start = time.time()
    def Pause(self):
        if not self.paused: self.suspend = time.time(); self.paused = True
    def Resume(self):
        if self.paused:
            self.downtime += time.time()-self.suspend
            self.suspend = 0; self.paused = False
    def GetTime(self): # elapsed time is the time since the song started minus the downtime
        downtime = self.downtime
        if self.paused: downtime += time.time()-self.suspend
        return int(time.time()-downtime-self.start)
    def Reset(self): # reset when song ends
        self.start = 0
        self.suspend = 0
        self.downtime = 0
        self.paused = False

# to get the name and description of a function for the help command, __doc__ returns the doc of @client.command()
class reprwrapper(object):
    def __init__(self, repr, func):
        self._repr = repr
        self._func = func
        functools.update_wrapper(self, func)
    def __call__(self, *args, **kw): return self._func(*args, **kw)
    def __repr__(self): return self._repr(self._func)

def withrepr(reprfun):
    def _wrap(func): return reprwrapper(reprfun, func)
    return _wrap

# initialize Bot object
with open('<token directory>','r') as f: bot_token = f.read(); f.close() # read token from local file
#bot_token = os.environ['TOKEN'] # read token as environment variable
Bot = Bot_Info(bot_token)

# initialize dict of user ranking objects
U = {}

# other global objects
Q = Queue()
stopwatch = Stopwatch_() # for music

# embed colors
#grey = 0x99a3a4
grey = 0xabb2bf
#red = 0xe74c3c
red = 0xe06c75
#green = 0x3ce74c
green = 0x98c379
purple = 0xb07bff

# initialize Discord client
intents = discord.Intents.default()
intents.presences = True
intents.members = True
if 'playing' in Bot.acttype: ty = discord.ActivityType.playing
elif 'watching' in Bot.acttype: ty = discord.ActivityType.watching
elif 'listening' in Bot.acttype: ty = discord.ActivityType.listening
elif 'streaming' in Bot.acttype: ty = discord.ActivityType.streaming
else: ty = discord.ActivityType.playing
activity = discord.Activity(name=Bot.status,type=ty)
client = commands.Bot(command_prefix=Bot.prefix,help_command=None,activity=activity,intents=intents)
