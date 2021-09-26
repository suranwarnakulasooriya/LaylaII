# ==============================================================================
# ranking
# ==============================================================================

from init import *

@withrepr(lambda x: 'See your rank in this server.')
@client.command()
async def rank(ctx):
    if ctx.author.id in U:
        user = U[ctx.author.id]
        await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} is Level **{user.lvl}** with {user.xp} xp.\n[{user.nxp}/{Bot.rate*(user.lvl+1)}] until level {user.lvl+1}.",color=ctx.author.color))

@client.command(aliases=['cool'])
async def cooldown(ctx,c:int):
    if c < 0 or c > 10: # allowing 0 is intentional to make debugging easier
        await ctx.send(embed=discord.Embed(description="Cooldown out of range, give range between 1 and 10.",color=0xe74c3c))
    else:
        if ctx.author.guild_permissions.administrator:
            with open("cooldown.txt",'w') as f:
                f.write(str(c)); f.close()
            await ctx.send(embed=discord.Embed(description=f"Cooldown set from {Bot.cooldown} to {c}.",color=0x3ce74c))
            Bot.cooldown = c
        else:
            await ctx.send(embed=discord.Embed(description="You're not an admin. Denied.",color=0xe74c3c))

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
    for i,user in enumerate(server):
        desc += f'#{i+1}) <@!{user[0]}>, Level: **{U[user[0]].lvl}**, Xp: {user[1]}\n\n'
    embed = discord.Embed(title='Leaderboard',description=desc,color=0xb07bff)
    await ctx.send(embed=embed)

@client.command()
async def savedata(ctx):
    with open('users.txt','w') as f:
        lines = []
        for u in U: lines.append(f"{U[u].id} {U[u].xp} {U[u].lvl} {U[u].nxp}")
        for line in lines: f.write(line); f.write('\n')
        f.close()
    await ctx.send(embed=discord.Embed(description="User ranking data has been saved.",color=0x3ce74c))

@client.command()
async def givelevel(ctx,user:discord.User=None,lvl=0):
    if ctx.author.guild_permissions.administrator:
        try:
            U[user.id] = User(user.id,Bot,lvl*5,lvl,0)
            await ctx.send(embed=discord.Embed(description=f"Gave {user.mention} level {lvl} [{lvl*5} xp].",color=0x3ce74c))
        except:
            await ctx.send(embed=discord.Embed(description="Something went wrong, and it's your fault.",color=0xe74c3c))
    else:
        await ctx.send(embed=discord.Embed(description="You're not an admin. Denied.",color=0xe74c3c))
