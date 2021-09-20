# ==============================================================================
# build help command
# ==============================================================================

from commands_all import *

class Help:
    def __init__(self,cmd_types,cpp,media,music,misc):
        self.cmd_types = cmd_types

        embed = discord.Embed()
        embed.set_author(name="Help With What?")
        embed.set_footer(text="Use help <category> for a list of commands.")
        for type in self.cmd_types:
            embed.add_field(name=type[0],value=type[1],inline=False)

        self.embed = embed

        ###

        embed = discord.Embed()
        embed.set_author(name="All the copypastas.")

        for cmd in cpp:
            embed.add_field(name=cmd.name,value=cmd,inline=False)

        self.help_cpp = embed

        ###

        embed = discord.Embed()
        embed.set_author(name="Reaction images and videos.")

        for cmd in media:
            embed.add_field(name=cmd.name,value=cmd,inline=True)

        embed.set_footer(text="There are others that arent listed :).")

        self.help_media = embed

        ###

        embed = discord.Embed()
        embed.set_author(name="Other garbage I can do.")

        for cmd in misc:
            embed.add_field(name=cmd.name,value=cmd,inline=False)

        self.help_misc = embed

        ###

        embed = discord.Embed()
        embed.set_author(name="To fill the void in our hearts left by Groovy.")

        for cmd in music:
            embed.add_field(name=cmd.name,value=cmd,inline=True)

        embed.set_footer(text="If a song doesn't play or the queue is out of wack, clear the queue.")

        self.help_music = embed


help_command_ = Help([['Copypastas','Send meaningless walls of text.'],
                     ['Media','Reaction images and videos.'],
                     ['Music','RIP Groovy.'],
                     ['Misc',"Other random garbage."]],
                     [kira,napkin,neitzsche,space,penis],
                     [stfu,idontcare,nobodyasked,lmao,zook,nofucks,ugh,bullied,
                     zook2,anythingelse,hypno,cleanse,comedian,fish,stupid,jesus,
                     begone,gun,crusader,bequiet,dildo,circus,ymir,fail,l1984],
                     [disclaimer,play,pause,resume,stop,loop,np,next,queue,remove,clear,setcurrent,leave],
                     [hello,say,mock,wide,thicc,smol,aussie,leet])


@client.command()
async def help(ctx,*,arg=''):
    if arg == '':
        await ctx.send(embed=help_command_.embed)
    elif arg == 'copypastas':
        await ctx.send(embed=help_command_.help_cpp)
    elif arg == 'media':
        await ctx.send(embed=help_command_.help_media)
    elif arg == 'misc':
        await ctx.send(embed=help_command_.help_misc)
    elif arg == 'music':
        await ctx.send(embed=help_command_.help_music)
    else:
        await ctx.send(embed=discord.Embed(description=f'There is no category named {arg}. Valied categories are copypastas, media, music, and misc.'))
