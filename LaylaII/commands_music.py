# ==============================================================================
# music
# ==============================================================================

from init import *
import youtube_dl
from discord import FFmpegPCMAudio
import os

def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

@client.command(aliases=['p'],pass_context=True)
async def play(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        voice.play(FFmpegPCMAudio('song.mp3'))
    else:
        await ctx.send('youre not in a voice channel yourself, curious')


@client.command()
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if ctx.guild.voice_client in client.voice_clients:
        await voice.disconnect()
    else: await ctx.send('how can i leave a channel im not in')

@client.command()
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing:
        voice.pause()
    else: ctx.send('its already silent dipshit')

@client.command()
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused():
        voice.resume()
    else: ctx.send('but im not paused tho')

@client.command()
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
