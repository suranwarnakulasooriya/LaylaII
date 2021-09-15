# ==============================================================================
# all commands
# ==============================================================================

from init import *
#from dad import *
from commands_copypastas import *
from commands_misc import *
from commands_images import *
from commands_videos import *
from commands_music import *

@client.command()
async def error(ctx):
    try:
        print(0/0)
    except:
        await ctx.send(embed=embeds.error())
