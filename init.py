# ==============================================================================
# start everything up
# ==============================================================================

# discord.py
import discord
from discord.ext import commands
from discord.ext.commands import Cog
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

class Bot_Info: # class with basic bot info
    def __init__(self,token):
        self.token = token
        self.connected = False
        with open('data.txt','r') as f: data = f.read().split(); f.close()
        self.prefix = data[0]
        self.rate = int(data[1])
        self.cooldown = int(data[2])
        self.lvlroles = {}

async def roleup(message): # thresholds and role names
    author = U[message.author.id]
    user = message.author
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
        if client.user.mentioned_in(message) and '@here' not in message.content and '@everyone' not in message.content: # show prefix when mentioned
            await message.channel.send(f"My prefix is `{self.obj.prefix}`")
        if not message.author.bot:
            if message.author.id not in U: U[message.author.id] = User(message.author.id,self.obj)
            elif U[message.author.id].valid(self.obj.cooldown):
                U[message.author.id].xp += 1
                with open('users.txt','w') as f:
                    lines = []
                    for u in U: lines.append(f"{U[u].id} {U[u].xp} {U[u].lvl} {U[u].nxp}")
                    for line in lines: f.write(line); f.write('\n')
                    f.close()
                if U[message.author.id].lvlup():
                    await message.channel.send(embed=discord.Embed(description=f"{message.author.mention} has leveled up! Now level {U[message.author.id].lvl}. {U[message.author.id].nxp}/{self.obj.rate*(U[message.author.id].lvl+1)} until level {U[message.author.id].lvl+1}.",color=message.author.color))
                    await roleup(message)
        msg = message.content
        if 'british' in msg or 'britain' in msg or 'french' in msg or 'france' in msg or 'league of legends' in msg:
            await message.channel.send(embed=discord.Embed(description=f"{message.author.mention} has said a banned word, -69 trillion social credits.",color=0xe74c3c))

class Copypastas: # create copypastas
    def __init__(self):
        self.kira = "My name is Yoshikage Kira. I'm 33 years old. My house is in the northeast section of Morioh, where all the villas are, and I am not married. I work as an employee for the Kame Yu department stores, and I get home every day by 8 PM at the latest. I don't smoke, but I occasionally drink. I'm in bed by 11 PM, and make sure I get eight hours of sleep, no matter what. After having a glass of warm milk and doing about twenty minutes of stretches before going to bed, I usually have no problems sleeping until morning. Just like a baby, I wake up without any fatigue or stress in the morning. I was told there were no issues at my last check-up. I'm trying to explain that I'm a person who wishes to live a very quiet life. I take care not to trouble myself with any enemies, like winning and losing, that would cause me to lose sleep at night. That is how I deal with society, and I know that is what brings me happiness. Although, if I were to fight I wouldn't lose to anyone."
        self.napkin = "Suppose that you were sitting down at this table. The napkins are in front of you, which napkin would you take? The one on your ‘left’? Or the one on your ‘right’? The one on your left side? Or the one on your right side? Usually you would take the one on your left side. That is ‘correct’ too. But in a larger sense on society, that is wrong. Perhaps I could even substitute ‘society’ with the ‘Universe’. The correct answer is that ‘It is determined by the one who takes his or her own napkin first.’ …Yes? If the first one takes the napkin to their right, then there’s no choice but for others to also take the ‘right’ napkin. The same goes for the left. Everyone else will take the napkin to their left, because they have no other option. This is ‘society’… Who are the ones that determine the price of land first? There must have been someone who determined the value of money, first. The size of the rails on a train track? The magnitude of electricity? Laws and Regulations? Who was the first to determine these things? Did we all do it, because this is a Republic? Or was it Arbitrary? NO! The one who took the napkin first determined all of these things! The rules of this world are determined by that same principle of ‘right or left?’! In a Society like this table, a state of equilibrium, once one makes the first move, everyone must follow! In every era, this World has been operating by this napkin principle. And the one who ‘takes the napkin first’ must be someone who is respected by all. It’s not that anyone can fulfill this role… Those that are despotic or unworthy will be scorned. And those are the ‘losers’. In the case of this table, the ‘eldest’ or the ‘Master of the party’ will take the napkin first… Because everyone ‘respects’ those individuals."
        self.neitzsche = "God is dead. God remains dead. And we have killed him. How shall we comfort ourselves, the murderers of all murderers? What was holiest and mightiest of all that the world has yet owned has bled to death under our knives? Who will wipe this blood off us? What water is there for us to clean ourselves? What festivals of atonement, what sacred games shall we have to invent? Is not the greatness of this deed too great for us? Must we ourselves not become gods simply to appear worthy of it?"
        self.linux = """I'd just like to interject for a moment. What you're referring to as Linux, is in fact, GNU/Linux, or as I've recently taken to calling it, GNU plus Linux. Linux is not an operating system unto itself, but rather another free component of a fully functioning GNU system made useful by the GNU corelibs, shell utilities and vital system components comprising a full OS as defined by POSIX. Many computer users run a modified version of the GNU system every day, without realizing it. Through a peculiar turn of events, the version of GNU which is widely used today is often called "Linux", and many of its users are not aware that it is basically the GNU system, developed by the GNU Project. There really is a Linux, and these people are using it, but it is just a part of the system they use. Linux is the kernel: the program in the system that allocates the machine's resources to the other programs that you run. The kernel is an essential part of an operating system, but useless by itself; it can only function in the context of a complete operating system. Linux is normally used in combination with the GNU operating system: the whole system is basically GNU with Linux added, or GNU/Linux. All the so-called "Linux" distributions are really distributions of GNU/Linux."""
        self.sf1 = """So someone in a group asked me to tell them why I hate the ocean sunfish so much, and apparently it was ~too mean~ and was deleted. To perpetuate the truth and stand up for ethical journalism, I'm posting it here. [Rated NC-17 for language.] Disclaimer, I care about marine life more than I care about anything else, for real. Except this big dumb idiot. And it's not like an ~ironic~ thing, I mean it IS hilarious to me and they ARE THE BIGGEST JOKE PLAYED ON EARTH but I seriously fucking hate them. THE MOLA MOLA FISH (OR OCEAN SUNFISH) They are the world's largest boney fish, weighing up to 5,000 pounds. And since they have very little girth, that just makes them these absolutely giant fucking dinner plates that God must have accidentally dropped while washing dishes one day and shrugged his shoulders at because no one could have imagined this would happen. AND WITH NO PURPOSE. EVERY POUND OF THAT IS A WASTED POUND AND EVERY FOOT OF IT (10 FT BY 14 FT) IS WASTED SPACE. They are so completely useless that scientists even debate about how they move. They have little control other than some minor wiggling. Some say they must just push water out of their mouths for direction (?????). They COULD use their back fin EXCEPT GUESS WHAT IT DOESNT FUCKING GROW. It just continually folds in on itself, so the freaking cells are being made, this piece of floating garbage just doesn't put them where they need to fucking go. So they don't have swim bladders. You know, the one thing that every fish has to make sure it doesn't just sink to the bottom of the ocean when they stop moving and can stay the right side up. This creature. That can barely move to begin with. Can never stop its continuous tour of idiocy across the ocean or it'll fucking sink. EXCEPT. EXCEPT. When they get stuck on top of the water! Which happens frequently! Because without the whole swim bladder thing, if the ocean pushes over THE THINNEST BUT LARGEST MOST TOPPLE-ABLE FISH ON THE PLANET, shit outta luck!"""
        self.sf2 = """There is no creature on this earth that needs a swim bladder more than this spit in the face of nature, AND YET. Some scientists have speculated that when they do that, they are absorbing energy from the sun because no one fucking knows how they manage to get any real energy to begin with. So they need the sun I guess. But good news, when they end up stuck like that, it gives birds a chance to land on their goddamn island of a body and eat the bugs and parasites out of its skin because it's basically a slowly migrating cesspool. Pros and cons. "If they are so huge, they must at least be decent predators." No. No. The most dangerous thing about them is, as you may have guessed, their stupidity. They have caused the death of one person before. Because it jumped onto a boat. On a human. And in 2005 it decided to relive its mighty glory days and do it again, this time landing on a four-year-old boy. Luckily Byron sustained no injuries. Way to go, fish. Great job. They mostly only eat jellyfish because of course they do, they could only eat something that has no brain and a possibility of drifting into their mouths I guess. Everything they do eat has almost zero nutritional value and because it's so stupidly fucking big, it has to eat a ton of the almost no nutritional value stuff to stay alive. Dumb. See that ridiculous open mouth? (This is actually why this is my favorite picture of one, and I have had it saved to my phone for three years) "Oh no! What could have happened! How could this be!" Do not let that expression fool you, they just don't have the goddamn ability to close their mouths because their teeth are fused together, and ya know what, it is good it floats around with such a clueless expression on its face, because it is in fact clueless as all fuck."""
        self.sf3 = """They do SOMETIMES get eaten though. BUT HARDLY. No animal truly uses them as a food source, but instead (which has lead us to said photo) will usually just maim the fuck out of them for kicks. Seals have been seen playing with their fins like frisbees. Probably the most useful thing to ever come from them. "Wow, you raise some good points here, this fish truly is proof that God has abandoned us." Yes, thank you. "But if they're so bad at literally everything, why haven't they gone extinct." Great question. BECAUSE THIS THING IS SO WORTHLESS IT DOESNT REALIZE IT SHOULD NOT EXIST. IT IS SO UNAWARE OF LITERALLY FUCKING EVERYTHING THAT IT DOESNT REALIZE THAT IT'S DOING MAYBE THE WORST FUCKING JOB OF BEING A FISH, OR DEBATABLY THE WORST JOB OF BEING A CLUSTER OF CELLS THAN ANY OTHER CLUSTER OF CELLS. SO WHAT DOES IT DO? IT LAYS THE MOST EGGS OUT OF EVERYTHING. Besides some bugs, there are some ants and stuff that'll lay more. IT WILL LAY 300 MILLION EGGS AT ONE TIME. 300,000,000. IT SURVIVES BECAUSE IT WOULD BE STATISTICALLY IMPROBABLE, DARE I SAY IMPOSSIBLE, THAT THERE WOULDNT BE AT LEAST ONE OF THOSE 300,000,000 (that is EACH time they lay eggs) LEFT SURVIVING AT THE END OF THE DAY. And this concludes why I hate the fuck out of this complete failure of evolution, the Ocean Sunfish. If I ever see one, I will throw rocks at it."""
        self.beans = """**My (25 M) girlfriend (26 F) baked all the beans, now I consider to end our relations? What does I do?**
Hello,
My girlfriend and me have done dating for 5 month. I thought "This girl is very good," and became of love with her.
Yet even so, on this Monday, I comed home and found she as baked all my beans.
Yes, all. Oh brother.
In my cupboard I store several bag of bean, to make soft and to bake on some days, to have a bit of baked bean on my dinner. Or, heck, a lunch too some days.
But on the Monday I find this girlfriend baked all the beans. I say "Why do you bake my beans", and she say something as "I bakes them good to save time, so I bakes them all now."
I am astonished and full of dissmay. I say "I canfr not eat all the beans", she say she is froze many of the beans so as we can unfrozen the on a later day and eat some at a time.
But, if a bean is froze and unfrozed, the very good and very nice flavor of bean is gone far.
A bean is best if baked fresh as a Sunday Pie. Not to be froze and unfroze!
I told my girfriend I am so sad of this, as to my opinion the baking of the beans and to freeze them has ruin all my beans. She say I am "gone haywire" by my enragement and sad manners.
But I hates what she did to my beans.
On the days before Monday I thought "Will we marry the girlfriend? Well it might be so."
But now I am so sad she baked them beans. I am consider to end our relations and not be the boyfriend and girlfriend any more. But, is my idea wrong? Could my girlfriend make promise to not bake the beans? I do not know what doing to do and how to feel forgiving on her.
What can I do on this situation I said here? (In the text I write above this.)
Thank you."""
        self.olympic = """would you rather have...?
**Soulmate **                                                      **Royal Mail Triple Screw Steamer Olympic**
- cant drive                                                    - top speed of 23 knots and highly maneuverable
- can get injured, mortal                             - safety rated for 6 compartment flooding, double hull, 68 lifeboats, survives 4 collisions
- annoying friends                                        - crew can and will mutiny if not given proper treatment
- annoying inlaws                                         - had 2 badass sisters and 2 German running mates
- will cheat on you if you get drafted       - a war veteran
- disloyal in general                                     - serves for 24 years
- attractiveness debatable                         - 2 grand staircases, cafe parisien, full length promenade deck, most beautiful ship on the seas
- coward                                                        - sinks a U-boat preparing to fire on her, saves sinking ships in danger zones, fitted with guns during wartime
- will die and be forgotten                         - nicknamed 'Old Reliable' and scrapped to build the Queen Mary which still exists
- bad fashion sense                                     - dazzle camouflage to confuse enemies while also being absolute drip
- smol                                                             - largest ship in the world 
- scared of weapons                                   - torpedo proof, rammed and sank a U-boat, unsinkable (not even a warship)"""
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
        if self.nxp >= self.rate:
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
#with open('/home/suranwarnakulasooriya/Desktop/LaylaII_token.txt','r') as f: bot_token = f.read(); f.close() # read token from local file
bot_token = os.environ['TOKEN'] # read token as environment variable
Bot = Bot_Info(bot_token)

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
Roles = ['Invisible','Pink','Black','Gray','White','Brown','Purple','Lunar','Blue','Blurple','Ice','Turquoise','Green','Yellow','Orange','Red'] # valid color roles

# embed colors
grey = 0x99a3a4
red = 0xe74c3c
green = 0x3ce74c
purple = 0xb07bff

# initialize Discord client
intents = discord.Intents.default()
intents.presences = True
intents.members = True
activity = discord.Activity(name='your every move', type=discord.ActivityType.watching)
client = commands.Bot(command_prefix=Bot.prefix,help_command=None,activity=activity,intents=intents)
client.add_cog(Log(client,Bot))
