# ==============================================================================
# config file
# ==============================================================================

import discord # discord.py
from discord.ext import commands
from discord.ext.commands import Cog
import sys # to kill code
import functools # for help command
from youtube_dl import YoutubeDL # to search YouTube
from discord import FFmpegPCMAudio # to stream audio
from datetime import timedelta as td # for music duration
import time

class Bot_Info:
    def __init__(self,prefix,token):
        self.prefix = prefix
        self.token = token
        self.connected = False
        with open("cooldown.txt",'r') as f:
            self.cooldown = int(f.readline())

class Log(Cog):
    def __init__(self,bot,obj):
        self.bot = bot
        self.obj = obj

    @Cog.listener()
    async def on_reaction_add(self,reaction,user):
        print(f"i saw that {user} dumbass react with{reaction.emoji}")

    @Cog.listener()
    async def on_member_join(member):
        if member not in U:
            U[member] = User(member.id)

    @Cog.listener("on_message")
    async def on_message(self,message):
        if not message.author.bot:
            if message.author.id not in U:
                U[message.author.id] = User(message.author.id)
            elif U[message.author.id].valid(self.obj.cooldown):
                U[message.author.id].xp += 1
                if U[message.author.id].lvlup():
                    await message.channel.send(embed=discord.Embed(description=f"{message.author.mention} has leveled up! Now level {U[message.author.id].lvl}. {U[message.author.id].nxp}/{5*(U[message.author.id].lvl+1)} until level {U[message.author.id].lvl+1}.",color=message.author.color))

class Copypastas:
    def __init__(self):
        self.kira = "My name is Yoshikage Kira. I'm 33 years old. My house is in the northeast section of Morioh, where all the villas are, and I am not married. I work as an employee for the Kame Yu department stores, and I get home every day by 8 PM at the latest. I don't smoke, but I occasionally drink. I'm in bed by 11 PM, and make sure I get eight hours of sleep, no matter what. After having a glass of warm milk and doing about twenty minutes of stretches before going to bed, I usually have no problems sleeping until morning. Just like a baby, I wake up without any fatigue or stress in the morning. I was told there were no issues at my last check-up. I'm trying to explain that I'm a person who wishes to live a very quiet life. I take care not to trouble myself with any enemies, like winning and losing, that would cause me to lose sleep at night. That is how I deal with society, and I know that is what brings me happiness. Although, if I were to fight I wouldn't lose to anyone."
        self.napkin = "Suppose that you were sitting down at this table. The napkins are in front of you, which napkin would you take? The one on your ‘left’? Or the one on your ‘right’? The one on your left side? Or the one on your right side? Usually you would take the one on your left side. That is ‘correct’ too. But in a larger sense on society, that is wrong. Perhaps I could even substitute ‘society’ with the ‘Universe’. The correct answer is that ‘It is determined by the one who takes his or her own napkin first.’ …Yes? If the first one takes the napkin to their right, then there’s no choice but for others to also take the ‘right’ napkin. The same goes for the left. Everyone else will take the napkin to their left, because they have no other option. This is ‘society’… Who are the ones that determine the price of land first? There must have been someone who determined the value of money, first. The size of the rails on a train track? The magnitude of electricity? Laws and Regulations? Who was the first to determine these things? Did we all do it, because this is a Republic? Or was it Arbitrary? NO! The one who took the napkin first determined all of these things! The rules of this world are determined by that same principle of ‘right or left?’! In a Society like this table, a state of equilibrium, once one makes the first move, everyone must follow! In every era, this World has been operating by this napkin principle. And the one who ‘takes the napkin first’ must be someone who is respected by all. It’s not that anyone can fulfill this role… Those that are despotic or unworthy will be scorned. And those are the ‘losers’. In the case of this table, the ‘eldest’ or the ‘Master of the party’ will take the napkin first… Because everyone ‘respects’ those individuals."
        self.neitzsche = "God is dead. God remains dead. And we have killed him. How shall we comfort ourselves, the murderers of all murderers? What was holiest and mightiest of all that the world has yet owned has bled to death under our knives? Who will wipe this blood off us? What water is there for us to clean ourselves? What festivals of atonement, what sacred games shall we have to invent? Is not the greatness of this deed too great for us? Must we ourselves not become gods simply to appear worthy of it?"
        self.space = "​\n"*50

# to get the name and description of a function for the help command, __doc__ returns the doc of @client.command()
class reprwrapper(object):
    def __init__(self, repr, func):
        self._repr = repr
        self._func = func
        functools.update_wrapper(self, func)
    def __call__(self, *args, **kw):
        return self._func(*args, **kw)
    def __repr__(self):
        return self._repr(self._func)

def withrepr(reprfun):
    def _wrap(func):
        return reprwrapper(reprfun, func)
    return _wrap

class Song:
  def __init__(self,title,url,length,request,rawtime):
    self.title = title # title of youtube video
    self.url = url # url for ffmpeg to use
    self.length = length # length in hh:mm:ss
    self.request = request # the user who requested the song
    self.rawtime = rawtime # duration in seconds
  def __repr__(self):
    return f"{self.title} : {self.url} : {self.length}"

class Queue:
  def __init__(self):
    self.queue = [] # list of Song objects
    self.loop = False # bool of whether the current song is looping or not
    self.current = 0 # index of current song in Q.queue

class Stopwatch: # for np and ranking
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
        if self.paused:
            downtime += time.time()-self.suspend
        return int(time.time()-downtime-self.start)
    def Reset(self): # reset when song ends
        self.start = 0
        self.suspend = 0
        self.downtime = 0
        self.paused = False

class User:
    def __init__(self,id):
        self.id = id
        self.xp = 0 # total xp
        self.lvl = 0
        self.nxp = 0 # xp gained after last lvl up
        self.clock = Stopwatch()
        self.clock.Start()
    def valid(self,cd):
        if int(time.time()-self.clock.start) >= cd:
            self.clock.Reset()
            self.clock.Start()
            return True
        else: return False
    def lvlup(self):
        if self.nxp >= 5*(self.lvl+1)-1:
            self.lvl += 1
            self.nxp = 0
            # code to assign a new role would go here
            return True
        else:
            self.nxp += 1
            return False

U = {} # dict of users being tracked {user id:User obj}
