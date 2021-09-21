# ==============================================================================
# ranking
# ==============================================================================

from init import *





@withrepr(lambda x: 'See your rank in this server.')
@client.command()
async def rank(ctx):
    if ctx.author.id in U:
        user = U[ctx.author.id]
        await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} is level {user.lvl} with {user.xp} xp and {user.nxp} new xp.",color=ctx.author.color))

@client.command()
async def uh(ctx):
    await ctx.send(ctx.author.id)

@client.command()
async def cooldown(ctx,c:int):
    if c < 0 or c > 10:
        await ctx.send(embed=discord.Embed(description="Cooldown out of range, give range between 1 and 10.",color=0xe74c3c))
    else:
        with open("cooldown.txt",'w') as f:
            f.write(str(c))
        await ctx.send(embed=discord.Embed(description=f"Cooldown set from {Bot.cooldown} to {c}.",color=0x3ce74c))
        Bot.cooldown = c

@client.command(aliases=['getcool','getcd'])
async def getcooldown(ctx):
    await ctx.send(embed=discord.Embed(description=f"Cooldown is currently {Bot.cooldown} seconds.",color=0x99a3a4))
