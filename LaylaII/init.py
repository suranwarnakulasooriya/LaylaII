# ==============================================================================
# import libraries and set up client
# ==============================================================================

from bot_info import *

Q = Queue()
stopwatch = Stopwatch()
copypastas = Copypastas()

activity = discord.Activity(name='your every move', type=discord.ActivityType.watching)
client = commands.Bot(command_prefix=Bot.prefix,help_command=None)
client.add_cog(Log(client,Bot))
