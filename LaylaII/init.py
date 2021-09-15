# ==============================================================================
# import libraries and set up client
# ==============================================================================

from bot_info import *

Bot = Bot_Info(bot_prefix,bot_token,bot_owner)
copypastas = Copypastas()
embeds = Embeds()

activity = discord.Activity(name='the world falling apart', type=discord.ActivityType.watching)
client = commands.Bot(command_prefix=Bot.prefix,help_command=None)
