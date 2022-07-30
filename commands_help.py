# ==============================================================================
# build help command
# ==============================================================================

from commands_music import *

class Help: # class with all help panels
    def __init__(self,cmds):
        # music
        embed = discord.Embed()
        embed.set_author(name="To fill the void in our hearts left by Groovy.")
        for cmd in cmds:
            embed.add_field(name=cmd.name,value=cmd,inline=True)
        embed.set_footer(text="If a song doesn't play or the queue is out of wack, clear the queue.")
        self.help_music = embed

# create help panels
help_command_ = Help([readme,search,result,play,pause,resume,stop,loop,jump,np,next,queue,move,remove,clear,setcurrent,disconnect,leave])

@client.command()
async def help(ctx,*,arg=''):
    await ctx.send(embed=help_command_.help_music)