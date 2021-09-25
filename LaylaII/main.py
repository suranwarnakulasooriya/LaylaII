# ==============================================================================
# run this file to run the bot
# ==============================================================================

from commands_help import *

@client.event
async def on_ready():
    print('\nLayla II is online.\n')

if __name__ == '__main__':
    client.run(Bot.token)
    savedata()
