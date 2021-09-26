# ==============================================================================
# start everything up
# ==============================================================================

# ==============================================================================
'''
Copyright (c) 2021 Suran Warnakulasooriya

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
# ==============================================================================

# discord.py
import discord
from discord.ext import commands
from discord.ext.commands import Cog

import sys # to kill code
import functools # for help command
from youtube_dl import YoutubeDL # to search YouTube
from discord import FFmpegPCMAudio # to stream audio
from datetime import timedelta as td # for music duration
import time

class Bot_Info: # class with basic bot info
    def __init__(self,prefix,token):
        self.prefix = prefix
        self.token = token
        self.connected = False
        with open("cooldown.txt",'r') as f: self.cooldown = int(f.readline()); f.close()
        self.rate = 5 # rate at which users level up relative to messages sent
        self.lvlroles = {}

class Log(Cog): # cog listeners for ranking
    def __init__(self,bot,obj):
        self.bot = bot # the client
        self.obj = obj # the Bot object

    @Cog.listener()
    async def on_reaction_add(self,reaction,user):
        print(f"{user} reacted with{reaction.emoji}")

    @Cog.listener()
    async def on_member_join(member):
        if member not in U:
            U[member] = User(member.id,self.obj)

    @Cog.listener("on_message")
    async def on_message(self,message):
        if client.user.mentioned_in(message):
            await message.channel.send(f"My prefix is `{self.obj.prefix}`")
        if not message.author.bot:
            if message.author.id not in U: U[message.author.id] = User(message.author.id,self.obj)
            elif U[message.author.id].valid(self.obj.cooldown):
                U[message.author.id].xp += 1
                if U[message.author.id].lvlup():
                    await message.channel.send(embed=discord.Embed(description=f"{message.author.mention} has leveled up! Now level {U[message.author.id].lvl}. {U[message.author.id].nxp}/{self.obj.rate*(U[message.author.id].lvl+1)} until level {U[message.author.id].lvl+1}.",color=message.author.color))
                    author = U[message.author.id]
                    user = message.author
                    if author.lvl == 1:
                        await user.add_roles(discord.utils.get(message.guild.roles,name='one'))
                    elif author.lvl == 2:
                        await user.remove_roles(discord.utils.get(message.guild.roles,name='one'))
                        await user.add_roles(discord.utils.get(message.guild.roles,name='two'))
                    '''
                    if author.lvl == 1:
                        await user.add_roles(discord.utils.get(message.guild.roles,name='Protostars'))
                    elif author.lvl == 5:
                        await user.remove_roles(discord.utils.get(message.guild.roles,name='Protostars'))
                        await user.add_roles(discord.utils.get(message.guild.roles,name='Main Sequence Stars'))
                    elif author.lvl == 10:
                        await user.remove_roles(discord.utils.get(message.guild.roles,name='Main Sequence Stars'))
                        await user.add_roles(discord.utils.get(message.guild.roles,name='Red Giants'))
                    elif author.lvl == 20:
                        await user.remove_roles(discord.utils.get(message.guild.roles,name='Red Giants'))
                        await user.add_roles(discord.utils.get(message.guild.roles,name='Red Supergiants'))
                    elif author.lvl == 30:
                        await user.remove_roles(discord.utils.get(message.guild.roles,name='Red Supergiants'))
                        await user.add_roles(discord.utils.get(message.guild.roles,name='White Dwarfs'))
                    elif author.lvl == 50:
                        await user.remove_roles(discord.utils.get(message.guild.roles,name='White Dwarfs'))
                        await user.add_roles(discord.utils.get(message.guild.roles,name='Black Dwarfs'))
                    elif author.lvl == 70:
                        await user.remove_roles(discord.utils.get(message.guild.roles,name='Black Dwarfs'))
                        await user.add_roles(discord.utils.get(message.guild.roles,name='Supernovas'))
                    elif author.lvl == 90:
                        await user.remove_roles(discord.utils.get(message.guild.roles,name='Supernovas'))
                        await user.add_roles(discord.utils.get(message.guild.roles,name='Neutron Stars'))
                    elif author.lvl == 100:
                        await user.remove_roles(discord.utils.get(message.guild.roles,name='Neutron Stars'))
                        await user.add_roles(discord.utils.get(message.guild.roles,name='Black Holes'))
                    '''
class Copypastas: # create copypastas
    def __init__(self):
        self.kira = "My name is Yoshikage Kira. I'm 33 years old. My house is in the northeast section of Morioh, where all the villas are, and I am not married. I work as an employee for the Kame Yu department stores, and I get home every day by 8 PM at the latest. I don't smoke, but I occasionally drink. I'm in bed by 11 PM, and make sure I get eight hours of sleep, no matter what. After having a glass of warm milk and doing about twenty minutes of stretches before going to bed, I usually have no problems sleeping until morning. Just like a baby, I wake up without any fatigue or stress in the morning. I was told there were no issues at my last check-up. I'm trying to explain that I'm a person who wishes to live a very quiet life. I take care not to trouble myself with any enemies, like winning and losing, that would cause me to lose sleep at night. That is how I deal with society, and I know that is what brings me happiness. Although, if I were to fight I wouldn't lose to anyone."
        self.napkin = "Suppose that you were sitting down at this table. The napkins are in front of you, which napkin would you take? The one on your ‘left’? Or the one on your ‘right’? The one on your left side? Or the one on your right side? Usually you would take the one on your left side. That is ‘correct’ too. But in a larger sense on society, that is wrong. Perhaps I could even substitute ‘society’ with the ‘Universe’. The correct answer is that ‘It is determined by the one who takes his or her own napkin first.’ …Yes? If the first one takes the napkin to their right, then there’s no choice but for others to also take the ‘right’ napkin. The same goes for the left. Everyone else will take the napkin to their left, because they have no other option. This is ‘society’… Who are the ones that determine the price of land first? There must have been someone who determined the value of money, first. The size of the rails on a train track? The magnitude of electricity? Laws and Regulations? Who was the first to determine these things? Did we all do it, because this is a Republic? Or was it Arbitrary? NO! The one who took the napkin first determined all of these things! The rules of this world are determined by that same principle of ‘right or left?’! In a Society like this table, a state of equilibrium, once one makes the first move, everyone must follow! In every era, this World has been operating by this napkin principle. And the one who ‘takes the napkin first’ must be someone who is respected by all. It’s not that anyone can fulfill this role… Those that are despotic or unworthy will be scorned. And those are the ‘losers’. In the case of this table, the ‘eldest’ or the ‘Master of the party’ will take the napkin first… Because everyone ‘respects’ those individuals."
        self.neitzsche = "God is dead. God remains dead. And we have killed him. How shall we comfort ourselves, the murderers of all murderers? What was holiest and mightiest of all that the world has yet owned has bled to death under our knives? Who will wipe this blood off us? What water is there for us to clean ourselves? What festivals of atonement, what sacred games shall we have to invent? Is not the greatness of this deed too great for us? Must we ourselves not become gods simply to appear worthy of it?"
        self.space = "​\n"*50

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

class User: # to store user ranking data
    def __init__(self,id,bot,xp=0,lvl=0,nxp=0):
        self.id = id
        self.xp = xp # total xp
        self.lvl = lvl
        self.nxp = nxp # xp gained after last lvl up
        self.clock = Stopwatch_() # for message cooldown
        self.clock.Start()
        self.rate = bot.rate
    def __repr__(self):
        return f"xp: {self.xp}, lvl: {self.lvl}, nxp: {self.nxp}"
    def valid(self,cd):
        if int(time.time()-self.clock.start) >= cd:
            self.clock.Reset()
            self.clock.Start()
            return True
        else: return False
    def lvlup(self):
        if self.nxp >= self.rate*(self.lvl+1)-1:
            self.lvl += 1
            self.nxp = 0
            return True
        else:
            self.nxp += 1
            return False

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
with open('prefix.txt','r') as f: bot_prefix = f.read(); f.close()
with open('/home/suranwarnakulasooriya/Desktop/LaylaII_token.txt','r') as f: bot_token = f.read(); f.close()
Bot = Bot_Info(bot_prefix,bot_token)

# initialize dict of user ranking objects
U = {}
with open('users.txt') as f: usersraw = f.readlines(); f.close()
usersstr = []
for user in usersraw: usersstr.append(user.split())
for user in usersstr:
    for item in range(len(user)): user[item] = int(user[item])
    U[user[0]] = User(user[0],Bot,user[1],user[2],user[3])

# other global objects
Q = Queue()
stopwatch = Stopwatch_() # for music
copypastas = Copypastas()

# initialize Discord client
activity = discord.Activity(name='for that c&d', type=discord.ActivityType.listening)
client = commands.Bot(command_prefix=bot_prefix,help_command=None)
client.add_cog(Log(client,Bot))