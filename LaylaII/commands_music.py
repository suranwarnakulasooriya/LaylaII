# ==============================================================================
# music
# ==============================================================================

from init import *

# to search YouTube
from youtube_dl import YoutubeDL
from requests import get

from discord import FFmpegPCMAudio # to stream audio

# for music duration
from datetime import timedelta as td
import datetime

# set ytdl and ffmpeg options
ydl_opts = {
'format': 'bestaudio/best',
'postprocessors': [{
    'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
    'preferredquality': '192','noplaylist':'True'}]}

FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
'options': '-vn'}


def search(arg): # return title, url, and duration of top result of search
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True','cookies':'cookies.txt'}) as ydl:
        try: get(arg)
        except: info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else: info = ydl.extract_info(arg, download=False)
    return (info['title'], info['formats'][0]['url'], info['duration'])


def get_time(sec): # convert time from raw seconds into human time
    dur = str(td(seconds=sec))
    for i in range(len(dur)):
        if dur[i] not in ['0',':']:
            dur = dur[i:]; break
    for i in range(len(dur)):
        if dur[-i] == '.':
            dur = dir[:i-1]; break
    return dur


@withrepr(lambda x: 'Play the audio of a YouTube URL or from YouTube search.')
@client.command(aliases=['p'],pass_context=True)
async def play(ctx, *, query : str):

    if not Bot.connected: # connect to VC if not already
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        Bot.connected = True

    if ctx.author.voice and Bot.connected:

        if len(Q.queue) > 19:
            await ctx.send(embed=discord.Embed(description='Queue is maxed out.', color=0xe74c3c))
        else:

            if 'https' in query: # if query is a url, remove extraneous parts of url
                url = query
                try: url = url[:url.index('&')]
                except ValueError: pass

            # search youtube for query (searching a url will return the url)
            title, url, duration = search(query)
            dur = get_time(duration)

            # flavor text
            if len(Q.queue) > 0:
                await ctx.send(embed=discord.Embed(description=f"Queued {title} [{dur}] [{ctx.author.mention}]",color=0x99a3a4))
            else:
                await ctx.send(embed=discord.Embed(description=f"Now Playing {title} [{dur}] [{ctx.author.mention}]",color=0x99a3a4))

            Q.queue.append(Song(title,url,dur,ctx.author.mention)) # add song to queue

            try: ctx.guild.voice_client.play(FFmpegPCMAudio(url, **FFMPEG_OPTS)) # play song
            except: pass

    elif not ctx.author.voice:
        await ctx.send(embed=discord.Embed(description="You need to be in a voice channel.", color=0xe74c3c))


@withrepr(lambda x: 'Show the queue.')
@client.command(aliases=['q'],pass_context=True)
async def queue(ctx):
    message = "```"
    for i,song in enumerate(Q.queue):
      message += f"\n{i}) {song.title}  {song.length}"
    if Q.loop_s: message += "\nThe current song is being looped."
    message += '```'
    if message == '``````': await ctx.send(embed=discord.Embed(description='Queue is empty.',color=0x99a3a4))
    else: await ctx.send(message)


@withrepr(lambda x: 'Join the voice channel of the author.')
@client.command(aliases=['j'],pass_context=True)
async def join(ctx):
    if not Bot.connected and ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        Bot.connected = True
    elif not Bot.connected and not ctx.author.voice:
        await ctx.send(embed=discord.Embed(description='You need to be in a voice channel.', color=0xe74c3c))


@withrepr(lambda x: 'Leave the voice channel.')
@client.command(aliases=['fuckoff','die','getout','l'],pass_context=True)
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if ctx.guild.voice_client in client.voice_clients:
        await voice.disconnect()
        Bot.connected = False
        Q.queue = []
    else: await ctx.send(embed=discord.Embed(description='No voice channel to leave from.', color=0xe74c3c))


@withrepr(lambda x: 'Pause the current song.')
@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing: voice.pause()


@withrepr(lambda x: 'Resume the current song.')
@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused(): voice.resume()


@withrepr(lambda x: 'Stops the current song.')
@client.command(pass_context=True)
async def stop(ctx,manual=True):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()


@withrepr(lambda x: 'Starts the next song.')
@client.command(aliases=['nxt','n','start','skip'],pass_context=True)
async def next(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
    if len(Q.queue) > 0: Q.queue.pop(0)
    try:
        ctx.guild.voice_client.play(FFmpegPCMAudio(Q.queue[0].url, **FFMPEG_OPTS))
        await ctx.send(embed=discord.Embed(description=f"Now Playing {Q.queue[0].title} [{Q.queue[0].length}] [{Q.queue[0].request}]",color=0x99a3a4))
    except IndexError: await ctx.send(embed=discord.Embed(description="No more songs to play.", color=0xe74c3c))

@withrepr(lambda x: 'Removes a given index from the queue.')
@client.command(aliases=['r','rm','rmv','re','rem'],pass_context=True)
async def remove(ctx,index:int):
    try:
        if index != 0:
            song = Q.queue.pop(index)
            await ctx.send(embed=discord.Embed(description=f"Removed Index {index}: {song.title}", color=0x99a3a4))
        else: await ctx.send(embed=discord.Embed(description=f"Cannot remove index 0, use `{Bot.prefix}next`.", color=0xe74c3c))
    except: await ctx.send(embed=discord.Embed(description="There's no song at that index.", color=0xe74c3c))


@withrepr(lambda x: "Clear the queue.")
@client.command(aliases=['cl','c'],pass_context=True)
async def clear(ctx):
    Q.queue = []
    await ctx.send(embed=discord.Embed(description="Queue has been cleared.",color=0x99a3a4))
