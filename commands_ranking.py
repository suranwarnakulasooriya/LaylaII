# ==============================================================================
# ranking
# ==============================================================================

from init import *

@withrepr(lambda x: 'See your rank in this server.')
@client.command()
async def rank(ctx,u:discord.User=None):
    if u == None: u = ctx.author
    if u.id in U:
        user = U[u.id]
        await ctx.send(embed=discord.Embed(description=f"{u.mention} is Level **{user.lvl}** with {user.xp} xp.\n[{user.nxp}/{user.nextxp()}] until level {user.lvl+1}.",color=u.color))

@withrepr(lambda x: 'Change the message cooldown (admin only).')
@client.command(aliases=['cool'])
async def cooldown(ctx,c:int):
    if ctx.author.guild_permissions.administrator:
        if c < 0 or c > 10: # allowing 0 is intentional to make debugging easier
            await ctx.send(embed=discord.Embed(description="Cooldown out of range, give range between 1 and 10.",color=red))
        else:
            with open("data.txt",'w') as f: f.write(f"{Bot.prefix} {Bot.rate} {c}"); f.close()
            await ctx.send(embed=discord.Embed(description=f"Cooldown set from {Bot.cooldown} to {c}.",color=green))
            Bot.cooldown = c
    else:
        await ctx.send(embed=discord.Embed(description="You're not an admin. Denied.",color=red))

@withrepr(lambda x: 'See the current cooldown.')
@client.command(aliases=['getcool','getcd'])
async def getcooldown(ctx):
    await ctx.send(embed=discord.Embed(description=f"Cooldown is currently {Bot.cooldown} seconds.",color=grey))

@withrepr(lambda x: 'See the top 10 most active users.')
@client.command(aliases=['leads','lead','leaders'])
async def leaderboard(ctx,all=''):
    if all.lower() == 'all': all = True
    else: all = False
    server = []
    for user in U:
        server.append((U[user].id,U[user].xp))
    if not all: m = 10
    elif all and len(server) <= 30: m = 31
    elif all and len(server) > 30: m = 30
    server = sorted(server,key=lambda x:x[1],reverse=True)[:min(m,len(server))]
    desc = ''
    for i,user in enumerate(server):
        desc += f'#{i+1}) <@!{user[0]}>, Level: **{U[user[0]].lvl}**, Xp: {user[1]}\n\n'
    embed = discord.Embed(title=f'Leaderboard - Top {min(m,len(server))}',description=desc,color=purple)
    await ctx.send(embed=embed)

@withrepr(lambda x: 'Assign a level to a user (admin only).')
@client.command()
async def givelevel(ctx,user:discord.User=None,lvl=0):
    if ctx.author.guild_permissions.administrator:
        try:
            xp = sum([x**2 for x in range(lvl+1)])+20*(lvl!=0)
            U[user.id] = User(user.id,Bot,xp,lvl,0)
            await ctx.send(embed=discord.Embed(description=f"Gave {user.mention} level {lvl} [{xp} xp].",color=green))
            await roleup(ctx)
        except:
            await ctx.send(embed=discord.Embed(description="Something went wrong.",color=red))
    else:
        await ctx.send(embed=discord.Embed(description="You're not an admin. Denied.",color=red))

@withrepr(lambda x: 'Assign xp to a user (admin only).')
@client.command()
async def givexp(ctx,user:discord.User=None,xp=0):
    if ctx.author.guild_permissions.administrator:
        try:
            lvl = U[user.id].lvl
            up = sum([x**2 for x in range(lvl+2)])+20*(lvl!=0)
            low = sum([x**2 for x in range(lvl+1)])+20*(lvl!=0)
            if low <= xp < up:
                await ctx.send(embed=discord.Embed(description=f"Gave {user.mention} xp {xp}.",color=green))
                U[user.id].xp = xp
                U[user.id].nxp = xp-low
            else: await ctx.send(embed=discord.Embed(description=f"Xp out of range ({low}-{up}) for this level ({lvl})."))
        except:
            await ctx.send(embed=discord.Embed(description="Something went wrong.",color=red))
    else:
        await ctx.send(embed=discord.Embed(description="You're not an admin. Denied.",color=red))

@withrepr(lambda x: "See all valid colors.")
@client.command()
async def colors(ctx):
    msg = 'Valid colors are: '
    for role in Roles: msg += role+', '
    msg += '.'
    await ctx.send(embed=discord.Embed(description=msg,color=grey))

@withrepr(lambda x: 'Change your color role.')
@client.command()
async def setcolor(ctx,role:str):
    try:
        if role in Roles:
            user = ctx.author
            for r in Roles:
                await user.remove_roles(discord.utils.get(ctx.guild.roles,name=r))
            await user.add_roles(discord.utils.get(ctx.guild.roles,name=role))
            await ctx.send(embed=discord.Embed(description=f"Changed color to {role}.",color=green))
        else: await ctx.send(e,bed=discord.Embed(description="Role not valid.",color=red))
    except: await ctx.send(embed=discord.Embed(description="Something went wrong.",color=red))
