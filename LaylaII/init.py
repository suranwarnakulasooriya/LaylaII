# ==============================================================================
# import libraries and set up client
# ==============================================================================

from bot_info import *

Q = Queue()
stopwatch = Stopwatch()
copypastas = Copypastas()

bot_prefix = "."
with open('/home/suranwarnakulasooriya/Desktop/LaylaII_token.txt','r') as f:
    bot_token = f.read()
Bot = Bot_Info(bot_prefix,bot_token)

activity = discord.Activity(name='your every move', type=discord.ActivityType.watching)
client = commands.Bot(command_prefix=Bot.prefix,help_command=None)
