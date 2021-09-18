# ==============================================================================
# music
# ==============================================================================

from init import *

# to search YouTube
from youtube_dl import YoutubeDL
from requests import get

from discord import FFmpegPCMAudio # to stream audio

# to get details of video
import urllib
import simplejson

# for music duration
from datetime import timedelta as td
from datetime import datetime
#from time import clock

# set ytdl and ffmpeg options
ydl_opts = {
'format': 'bestaudio/best',
'postprocessors': [{
    'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
    'preferredquality': '192','noplaylist':'True'}]}

FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
'options': '-vn'}

def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def search(arg):
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True','cookies':'cookies.txt'}) as ydl:
        try: get(arg)
        except: info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else: info = ydl.extract_info(arg, download=False)
    return (info['title'], info['formats'][0]['url'], info['duration'])

def get_title(url):
    json = simplejson.load(urllib.request.urlopen(url))
    title = json['entry']['title']['$t']
    return title

def get_time(sec):
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
    if ctx.author.voice and Bot.connected:

        if 'https' in query: # if query is a url, remove extraneous parts of url
            url = query
            try: url = url[:url.index('&')]
            except ValueError: pass
            #print('url:'+url)

        # search youtube for query (searching a url will return the url)
        title, url, dur = search(query)
        dur = get_time(dur)
        print(all)
        await ctx.send(embed=discord.Embed(description=f"Queued {title} [{dur}] [{ctx.author.mention}]",
        color=0x99a3a4)) # flavor text
        await Q.add_song(Song(title,url,dur,ctx.author.mention))
        ctx.guild.voice_client.play(FFmpegPCMAudio(url, **FFMPEG_OPTS),after=lambda e:skip(ctx))
        #Bot.playtime = datetime.now()

    elif ctx.author.voice and not Bot.connected:
        await ctx.send('im not joined yet')
    elif not ctx.author.voice and Bot.connected:
        await ctx.send('youre not in a voice channel yourself')

@withrepr(lambda x: 'See the current playing song.')
@client.command(pass_context=True)
async def np(ctx):
        #await ctx.send(f"{get_time(datetime.now()-Bot.playtime)}/{get_time(Bot.playtime)}")
        await ctx.send(embed=embeds.error())

@withrepr(lambda x: 'Show the queue.')
@client.command(aliases=['q'],pass_context=True)
async def queue(ctx):
    message = "```"
    for i,song in enumerate(Q.queue):
      message += f"\n{i}) {song.title}  {song.length}"
    if Q.loop_s: message += "\nThe current song is being looped."
    if Q.loop_q: message += "\mThe queue is being looped."
    message += '```'
    await ctx.send(message)


@withrepr(lambda x: 'Join the voice channel of the author.')
@client.command(aliases=['j'],pass_context=True)
async def join(ctx):
    if not Bot.connected and ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        Bot.connected = True
    else: await ctx.send('something went wrong')


@withrepr(lambda x: 'Leave the voice channel.')
@client.command(aliases=['fuckoff','die','getout','l'],pass_context=True)
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if ctx.guild.voice_client in client.voice_clients:
        await voice.disconnect()
        Bot.connected = False
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
@client.command(aliases=['stop'],pass_context=True)
async def skip(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    ctx.guild.voice_client.stop()
    Q.queue.pop(0)
    ctx.guild.voice_client.play(FFmpegPCMAudio(Q.queue[0].url, **FFMPEG_OPTS))

@withrepr(lambda x: 'Removes a certain index from the queue.')
@client.command(aliases=['r','rm','rmv'],pass_context=True)
async def remove(ctx,index:int):
    try:
        Q.queue.pop(index)
        if index == 0:
            ctx.guild.voice_client.stop()
            ctx.guild.voice_client.play(FFmpegPCMAudio(Q.queue[0].url, **FFMPEG_OPTS))
    except: await ctx.send("There's no song at that index.")
