# ==============================================================================
# copypastas
# ==============================================================================

from init import *

# command kira
@withrepr(lambda x: "My name is Yoshikage Kira...")
@client.command()
async def kira(ctx):
    await ctx.send(copypastas.kira)

# command napkin
@withrepr(lambda x: 'Suppose you were sitting down at this table...')
@client.command()
async def napkin(ctx):
    await ctx.send(copypastas.napkin)

# command neitzche
@withrepr(lambda x: 'God is dead...')
@client.command()
async def neitzsche(ctx):
    await ctx.send(copypastas.neitzsche)

# command space
@withrepr(lambda x: 'A big block of nothing.')
@client.command()
async def space(ctx):
    await ctx.send(copypastas.space)

# command penis
@withrepr(lambda x: "A horrible penis joke.")
@client.command()
async def penis(ctx):
    await ctx.send('penis')
    await ctx.send(f'hey {ctx.author.mention} why are you looking at penis??')
