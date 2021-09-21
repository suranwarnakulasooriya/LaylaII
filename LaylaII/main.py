# ==============================================================================
# run this file to run the bot
# ==============================================================================

from commands_help import *

@client.event
async def on_ready():
    print('\nLayla II is online.\n')

#@client.event
#async def on_member_join(member):
#    U[member] = User()

#@client.event
#async def on_message(ctx):
#    if ctx.author in U:
#        if U[ctx.author].valid():
#            U[ctx.author].xp += 1

if __name__ == '__main__':
    client.run(Bot.token)
