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

# set ytdl and ffmpeg options
ydl_opts = {
'format': 'bestaudio/best',
'postprocessors': [{
    'key': 'FFmpegExtractAudio',
    'preferredcodec': 'mp3',
    'preferredquality': '192',
    'noplaylist':'True',
    }]}

FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
'options': '-vn'}
        
def is_connected(ctx):
    voice_client = get(ctx.bot.voice_clients, guild=ctx.guild)
    return voice_client and voice_client.is_connected()

def search(arg):
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True'}) as ydl:
        try: requests.get(arg)
        except: info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
        else: info = ydl.extract_info(arg, download=False)
    return (info, info['formats'][0]['url'])

def get_title(url):
    json = simplejson.load(urllib.request.urlopen(url))
    title = json['entry']['title']['$t']
    return title

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
        _video, url = search(query)
        await ctx.send(f'Now playing: `{list(_video.values())[1]}`.') # flavor text
        ctx.guild.voice_client.play(FFmpegPCMAudio(url, **FFMPEG_OPTS))

    elif ctx.author.voice and not Bot.connected:
        await ctx.send('im not joined yet')
    elif not ctx.author.voice and Bot.connected:
        await ctx.send('youre not in a voice channel yourself')


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
    voice.stop()
