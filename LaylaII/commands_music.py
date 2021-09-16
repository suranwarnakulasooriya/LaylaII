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

@withrepr(lambda x: 'Play the audio of a YouTube URL.')
@client.command(aliases=['p'],pass_context=True)
async def play(ctx, url : str):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')

        voice.play(FFmpegPCMAudio('song.mp3'))

    else:
        await ctx.send('youre not in a voice channel yourself, curious')

@withrepr(lambda x: 'Leave the voice channel.')
@client.command(aliases=['fuckoff','die','getout'],pass_context=True)
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if ctx.guild.voice_client in client.voice_clients:
        await voice.disconnect()
    else: await ctx.send('how can i leave a channel im not in')

@withrepr(lambda x: 'Pauses the current song.')
@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing: voice.pause()
    else: await ctx.send('its already silent dipshit')

@withrepr(lambda x: 'Resume the current song after pausing.')
@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused(): voice.resume()
    else: await ctx.send('but im not paused tho')

@withrepr(lambda x: 'Stops the current song and removes it from queue.')
@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
