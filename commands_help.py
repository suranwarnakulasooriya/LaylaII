# ==============================================================================
# build help command
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

from commands_media import *
from commands_music import *
from commands_ranking import *
from commands_misc import *

class Help: # class with all help panels
    def __init__(self,cmd_types,cpp,media,music,ranking,misc):
        self.cmd_types = cmd_types

        embed = discord.Embed()
        embed.set_author(name="Help With What?")
        embed.set_footer(text="Use help <category> for a list of commands.")
        for type in self.cmd_types:
            embed.add_field(name=type[0],value=type[1],inline=False)

        self.embed = embed

        # copypastas
        embed = discord.Embed()
        embed.set_author(name="All the copypastas.")

        for cmd in cpp:
            embed.add_field(name=cmd.name,value=cmd,inline=False)

        self.help_cpp = embed

        # media
        embed = discord.Embed()
        embed.set_author(name="Reaction images and videos.")

        for cmd in media:
            embed.add_field(name=cmd.name,value=cmd,inline=True)

        embed.set_footer(text="There are others that arent listed :).")

        self.help_media = embed

        # misc
        embed = discord.Embed()
        embed.set_author(name="Other garbage I can do.")

        for cmd in misc:
            embed.add_field(name=cmd.name,value=cmd,inline=False)

        self.help_misc = embed

        # music
        embed = discord.Embed()
        embed.set_author(name="To fill the void in our hearts left by Groovy.")

        for cmd in music:
            embed.add_field(name=cmd.name,value=cmd,inline=True)

        embed.set_footer(text="If a song doesn't play or the queue is out of wack, clear the queue.")

        self.help_music = embed

        # ranking
        embed = discord.Embed()
        embed.set_author(name="Imagine paying money to change the cooldown lmao.")

        for cmd in ranking:
            embed.add_field(name=cmd.name,value=cmd,inline=True)

        self.help_ranking = embed

# create help panels first
help_command_ = Help([['Copypastas','Send meaningless walls of text.'],
                     ['Media','Reaction images and videos.'],
                     ['Music','RIP Groovy.'],
                     ['Ranking','Amari bad.'],
                     ['Misc','Other random garbage.']],
                     [kira,napkin,neitzsche,space,penis],
                     [stfu,ungovernable,nobodyasked,lmao,zook,nofucks,ugh,bullied,
                     zook2,anythingelse,hypno,cleanse,comedian,fish,stupid,jesus,
                     begone,gun,crusader,bequiet,dildo,circus,ymir,fail,l1984],
                     [readme,play,pause,resume,stop,loop,np,next,queue,remove,clear,setcurrent,leave],
                     [rank,leaderboard,savedata,getcooldown,cooldown,givelevel],
                     [hello,say,mock,wide,thicc,smol,aussie,leet])

@client.command()
async def help(ctx,*,arg=''):
    if arg == '': await ctx.send(embed=help_command_.embed)
    elif arg == 'copypastas': await ctx.send(embed=help_command_.help_cpp)
    elif arg == 'media': await ctx.send(embed=help_command_.help_media)
    elif arg == 'misc': await ctx.send(embed=help_command_.help_misc)
    elif arg == 'music': await ctx.send(embed=help_command_.help_music)
    elif arg == 'ranking': await ctx.send(embed=help_command_.help_ranking)
    else:
        await ctx.send(embed=discord.Embed(description=f'There is no category named {arg}. Valid categories are copypastas, media, music, and misc.',color=0xe74c3c))
