# ==============================================================================
# ranking
# ==============================================================================

from init import *

@withrepr(lambda x: 'See your rank in this server.')
@client.command()
async def rank(ctx):
    if ctx.author.id in U:
        user = U[ctx.author.id]
        await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} is level {user.lvl} with {user.xp} xp. {user.nxp}/{5*(user.lvl+1)} until level {user.lvl+1}.",color=ctx.author.color))

@client.command()
async def uh(ctx):
    await ctx.send(ctx.author.id)

@client.command()
async def cooldown(ctx,c:int):
    if c < 0 or c > 10: # allowing 0 is intentional for debug purposes
        await ctx.send(embed=discord.Embed(description="Cooldown out of range, give range between 1 and 10.",color=0xe74c3c))
    else:
        with open("cooldown.txt",'w') as f:
            f.write(str(c))
        await ctx.send(embed=discord.Embed(description=f"Cooldown set from {Bot.cooldown} to {c}.",color=0x3ce74c))
        Bot.cooldown = c

@client.command(aliases=['getcool','getcd'])
async def getcooldown(ctx):
    await ctx.send(embed=discord.Embed(description=f"Cooldown is currently {Bot.cooldown} seconds.",color=0x99a3a4))

@client.command(aliases=['leads','lead','leaders'])
async def leaderboard(ctx):
    server = []
    for user in U:
        server.append((U[user].id,U[user].xp))
    server = sorted(server,key=lambda x:x[1],reverse=True)[:min(10,len(server))]
    desc = ''
    for user in server:
        desc += f'<@!{user[0]}>: level {U[user[0]].lvl}, {user[1]} exp.\n'
    await ctx.send(embed=discord.Embed(title="Leaderboard",description=desc,color=0xb07bff))
