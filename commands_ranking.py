# ==============================================================================
# ranking
# ==============================================================================

# ==============================================================================
'''
MIT License

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

from init import *

@withrepr(lambda x: 'See your rank in this server.')
@client.command()
async def rank(ctx):
    if ctx.author.id in U:
        user = U[ctx.author.id]
        await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention} is Level **{user.lvl}** with {user.xp} xp.\n[{user.nxp}/{Bot.rate*(user.lvl+1)}] until level {user.lvl+1}.",color=ctx.author.color))

@withrepr(lambda x: 'Change the message cooldown (admin only).')
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

@withrepr(lambda x: 'See the current cooldown.')
@client.command(aliases=['getcool','getcd'])
async def getcooldown(ctx):
    await ctx.send(embed=discord.Embed(description=f"Cooldown is currently {Bot.cooldown} seconds.",color=0x99a3a4))

@withrepr(lambda x: 'See the top 10 most active users.')
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

@withrepr(lambda x: 'Assign a level to a user (admin only).')
@client.command()
async def givelevel(ctx,user:discord.User=None,lvl=0):
    if ctx.author.guild_permissions.administrator:
        try:
            U[user.id] = User(user.id,Bot,lvl*Bot.rate,lvl,0)
            await ctx.send(embed=discord.Embed(description=f"Gave {user.mention} level {lvl} [{lvl*Bot.rate} xp].",color=0x3ce74c))
            await roleup(ctx)
        except:
            await ctx.send(embed=discord.Embed(description="Something went wrong.",color=0xe74c3c))
    else:
        await ctx.send(embed=discord.Embed(description="You're not an admin. Denied.",color=0xe74c3c))

@withrepr(lambda x: 'Change the rate at which users level up (admin only).')
@client.command()
async def changerate(ctx,rate:int):
    if ctx.author.guild_permissions.administrator:
        if rate < 10 or rate > 800:
            await ctx.send(embed=discord.Embed(description="Rate out of range, pick a range between 10-800",color=0xe74c3c))
        else:
            with open('rate.txt','w') as f: f.write(str(rate)); f.close()
            Bot.rate = rate
            for user in U: U[user].rate = rate
            await ctx.send(embed=discord.Embed(description=f"Changed level up rate to {rate}.",color=0x3ce74c))
    else:
        await ctx.send(embed=discord.Embed(description="You're not an admin. Denied.",color=0xe74c3c))

@withrepr(lambda x: 'See the current rate.')
@client.command()
async def getrate(ctx):
    await ctx.send(embed=discord.Embed(description=f"Level up rate is currently {Bot.rate} messages.",color=0x99a3a4))

@withrepr(lambda x: "See all valid colors.")
@client.command()
async def colors(ctx):
    msg = 'Valid colors are: '
    for role in Roles: msg += role+', '
    msg += '.'
    await ctx.send(embed=discord.Embed(description=msg,color=0x99a3a4))
    
@withrepr(lambda x: 'Change your color role.')
@client.command()
async def setcolor(ctx,role:str):
    try:
        if role in Roles:
            user = ctx.author
            for r in Roles:
                await user.remove_roles(discord.utils.get(ctx.guild.roles,name=r))
            await user.add_roles(discord.utils.get(ctx.guild.roles,name=role))
            await ctx.send(embed=discord.Embed(description=f"Changed color to {role}.",color=0x3ce74c))
        else: await ctx.send(e,bed=discord.Embed(description="Role not valid.",color=0xe74c3c))
    except: await ctx.send(embed=discord.Embed(description="Something went wrong.",color=0xe74c3c))
