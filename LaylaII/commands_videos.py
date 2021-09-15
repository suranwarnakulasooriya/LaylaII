# ==============================================================================
# video commands
# ==============================================================================

from init import *


# command reality

# command stfu
@withrepr(lambda x: "please stfu")
@client.command()
async def stfu(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/682040935403618438/845840723873366026/video0.mp4")

# command idontcare
@withrepr(lambda x: "i dont care if you didnt ask")
@client.command()
async def idontcare(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/682040935403618438/845834553734201444/I_dont_care_if_you_didnt_ask.mp4")

# command nobodyasked
@withrepr(lambda x: "nobody asked~ you are so dumb~")
@client.command()
async def nobodyasked(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/682040935403618438/845834281392537630/video0.mp4")

# command lmao
@withrepr(lambda x: "muta laughs at that shit")
@client.command()
async def lmao(ctx):
    await ctx.send("https://cdn.discordapp.com/attachments/682040935403618438/845839179685298266/videoplayback_6.mp4")
