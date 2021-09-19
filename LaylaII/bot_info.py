# ==============================================================================
# config file
# ==============================================================================

import discord
from discord.ext import commands
from discord.ext.commands import Cog
import sys

class Bot_Info:
    def __init__(self,prefix,token,owner):
        self.prefix = prefix
        self.token = token
        self.owner = owner
        self.connected = False
        self.playtime = 0
        self.async_tasks = []
        self.playing = False

class Reactions(Cog):
    def __init__(self, client):
        self.client = client

    @Cog.listener()
    async def on_reaction_add(self,reaction,user):
        print(f'{user.display_name} reacted with {reaction.emoji.name}')

class Embeds:
    def __init__(self):
        pass

    def embed(self,title,content,color):
        return discord.Embed(title=title,description=content,color=color)

    def deny(self):
        emb = discord.Embed(title="Command Denied.",
        description="You aren't Suran.", color=0xe74c3c)
        return emb

    def error(self):
        emb = discord.Embed(title="Command Failed.",
        description="Oops, Suran cocked up and the command didnt work.", color=0xe74c3c)
        return emb

    def kill(self):
        emb = discord.Embed(title="Kill Confirmed.",
        description="Aight imma head out.", color=0x2ecc71)
        return emb

    def hello(self):
        emb = discord.Embed(title="Hi there hello.",
        description="I'm alive.", color=0xb07bff)
        return emb

    def confirm(self):
        emb = discord.Embed(title="Are you sure?",color=0xe74c3c)
        return emb

class Copypastas:
    def __init__(self):
        self.kira = "My name is Yoshikage Kira. I'm 33 years old. My house is in the northeast section of Morioh, where all the villas are, and I am not married. I work as an employee for the Kame Yu department stores, and I get home every day by 8 PM at the latest. I don't smoke, but I occasionally drink. I'm in bed by 11 PM, and make sure I get eight hours of sleep, no matter what. After having a glass of warm milk and doing about twenty minutes of stretches before going to bed, I usually have no problems sleeping until morning. Just like a baby, I wake up without any fatigue or stress in the morning. I was told there were no issues at my last check-up. I'm trying to explain that I'm a person who wishes to live a very quiet life. I take care not to trouble myself with any enemies, like winning and losing, that would cause me to lose sleep at night. That is how I deal with society, and I know that is what brings me happiness. Although, if I were to fight I wouldn't lose to anyone."
        self.napkin = "Suppose that you were sitting down at this table. The napkins are in front of you, which napkin would you take? The one on your ‘left’? Or the one on your ‘right’? The one on your left side? Or the one on your right side? Usually you would take the one on your left side. That is ‘correct’ too. But in a larger sense on society, that is wrong. Perhaps I could even substitute ‘society’ with the ‘Universe’. The correct answer is that ‘It is determined by the one who takes his or her own napkin first.’ …Yes? If the first one takes the napkin to their right, then there’s no choice but for others to also take the ‘right’ napkin. The same goes for the left. Everyone else will take the napkin to their left, because they have no other option. This is ‘society’… Who are the ones that determine the price of land first? There must have been someone who determined the value of money, first. The size of the rails on a train track? The magnitude of electricity? Laws and Regulations? Who was the first to determine these things? Did we all do it, because this is a Republic? Or was it Arbitrary? NO! The one who took the napkin first determined all of these things! The rules of this world are determined by that same principle of ‘right or left?’! In a Society like this table, a state of equilibrium, once one makes the first move, everyone must follow! In every era, this World has been operating by this napkin principle. And the one who ‘takes the napkin first’ must be someone who is respected by all. It’s not that anyone can fulfill this role… Those that are despotic or unworthy will be scorned. And those are the ‘losers’. In the case of this table, the ‘eldest’ or the ‘Master of the party’ will take the napkin first… Because everyone ‘respects’ those individuals."
        self.neitzsche = "God is dead. God remains dead. And we have killed him. How shall we comfort ourselves, the murderers of all murderers? What was holiest and mightiest of all that the world has yet owned has bled to death under our knives? Who will wipe this blood off us? What water is there for us to clean ourselves? What festivals of atonement, what sacred games shall we have to invent? Is not the greatness of this deed too great for us? Must we ourselves not become gods simply to appear worthy of it?"
        self.space = "​\n"*50

import functools

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
  def __init__(self,title,url,length,request):
    self.title = title
    self.url = url
    self.length = length
    self.request = request
  def __repr__(self):
    return f"{self.title} : {self.url} : {self.length}"

# make a queue attribute in the Bot class that is the Queue class to gain access to ctx
class Queue:
  def __init__(self,maxL):
    # idk what the maxL should be, groovy had 10, id say 10-15
    self.maxL = maxL
    self.queue = []
    self.loop_s = False
    self.loop_q = False
    self.current = 0
    self.save = 0
    self.song = None
  def maxed(self,index=False):
    if index or index == 0: i = index
    else: i = len(self.queue)
    if i > self.maxL or i < 0: return True
    else: return False
  async def play(self):
    # play self.queue[0]
    await ctx.send(f"Now playing: `{self.queue[0].title}`.")
  async def add_song(self,song):
    if not self.maxed(): self.queue.append(song)
    else: await ctx,send('Queue maxed out.')
  async def remove_song(self,index):
    if maxed(index): await ctx.send("There's no song with that index")
    else:
      if index == 0: self.skip(True) # if index is [0] just skip it and delete
      else: self.queue.pop(index)
  def skip(self,delete=False): # also used to transition to next song
    if (not self.loop_s or not self.loop_q) or delete:
      self.queue.pop(0)
      # delete exists if the current song is being deleted while on loop
      # stop voice and play next song
    else: pass # stop voice and play next song, but keep queue[0]

  async def jump(self,index):
    if maxed(index): await ctx.send("There's no song with that index")
    else:
      self.queue = self.queue[index:]
      # stop voice and play next song
  async def np(self):
    time = 0#get time elapsed
    await ctx.send(f"{time}/{self.queue[0].length}")
  async def display(self):
    message = ""
    for i,song in enumerate(self.queue):
      message += f"\n{i}) {song.title}  {song.length}"
    if self.loop_s: message += "\nThe current song is being looped."
    if self.loop_q: message += "\mThe queue is being looped."
    await ctx.send(message)
  def loop_song(self):
    if self.loop_s: self.loop_s = False
    else: self.loop_s = True
  def loop_queue(self):
    if self.loop_q: self.loop_q = False
    else: self.loop_q = True

bot_prefix = "."
with open('/home/suranwarnakulasooriya/Desktop/LaylaII_token.txt','r') as f:
    bot_token = f.read()
bot_owner = 640303674895368194
Q = Queue(14)
