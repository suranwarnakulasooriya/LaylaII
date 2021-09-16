# ==============================================================================
# music
# ==============================================================================

from init import *
import youtube_dl
from youtube_dl import YoutubeDL
from discord import FFmpegPCMAudio
import os
#import urllib.parse, urllib.request, re
import requests
from requests import get
import subprocess
import asyncio
import urllib
import simplejson
from bs4 import BeautifulSoup

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

@withrepr(lambda x: 'Play the audio of a YouTube URL.')
@client.command(aliases=['p'],pass_context=True)
async def play(ctx, *, query : str):
    if ctx.author.voice and ctx.guild.voice_client in client.voice_clients:

        # join vc of the message author
        #channel = ctx.author.voice.channel
        #if ctx.guild.voice_client not in client.voice_clients:
        #voice = await channel.connect()

        # set ytdl options
        ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            'noplaylist':'True',
            }],
        }
        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        if False:
            # if request is a URL
            if 'https' in query:
                url = query
                # get url without references to playlists or timestamps
                try: url = url[:url.index('&')]
                except ValueError: pass
                print('url:'+url)


            # if not, it is a search
            else:
                #id = subprocess.check_output(['youtube-dl',f'ytsearch:{query}','--get-id'])[:-1].decode('utf-8')
                #url = f'www.youtube.com/watch?v={id}'
                video, url = search(query)
                #await ctx.send(f'Now playing: {info['title']}.')
                print('url:'+url)

        if 'https' in query:
            url = query
            # get url without references to playlists or timestamps
            try: url = url[:url.index('&')]
            except ValueError: pass
            print('url:'+url)
        video, url = search(query)


        #await ctx.send(f'Now playing: {get_title(url)}.')
        #ctx.guild.voice_client.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
        ctx.guild.voice_client.play(FFmpegPCMAudio(url, **FFMPEG_OPTS))

    elif ctx.author.voice and not Bot.connected:
        await ctx.send('im not joined yet')
    elif not ctx.author.voice and Bot.connected:
        await ctx.send('youre not in a voice channel yourself')

if False:
    @withrepr(lambda x: 'Play audio from YouTube search.')
    @client.command(aliases=['p'],pass_context=True)
    async def search(ctx,*,query:str):
        #cmd = ['youtube-dl', f'ytsearch:{query}', '--get-id']
        #output = subprocess.Popen( cmd, stdout=subprocess.PIPE ).communicate()[0]
        id = subprocess.check_output(['youtube-dl',f'ytsearch:{query}','--get-id'])[:-1].decode('utf-8')
        await ctx.send(f'www.youtube.com/watch?v={id}')
        #print(os.system(f"youtube-dl 'ytsearch:{query}' --get-id"))
        #print('what')
        #await ctx.send(f'https://www.youtube.com/watch?v={id}')



        '''
        FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

        video, source = search(query)
        voice = get(bot.voice_clients, guild=ctx.guild)

        #await join(ctx, voice)
        await ctx.send(f'aaa')

        voice.play(FFmpegPCMAudio(source, **FFMPEG_OPTS), after=lambda e: print('done', e))
        voice.is_playing()
        '''



        '''
        ydl_opts = {
        'format': 'bestaudio/best',
        'noplaylist': True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            }],
        }


        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                get(search)
            except:
                video = ydl.extract_info(f"ytsearch:{search}", download=False)['entries'][0]
            else:
                video = ydl.extract_info(arg, download=False)

        await ctx.send(video)
        '''


        '''
        ytdl = youtube_dl.YoutubeDL(ydl_opts)

        video = youtube_dl.extract_info(search, download = False)

        if 'entries' in video:
            video_format = video['entries'][0]["formats"][0]
        elif 'formats' in video:
            video_format = video["formats"][0]

        url = video["webpage_url"]
        stream_url = video_format["url"]

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # save song to song.mp3
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                os.rename(file, 'song.mp3')

        ctx.guild.voice_client.play(FFmpegPCMAudio('song.mp3'))
        '''

        '''
        query = urllib.parse.urlencode({
            'search_query':search
        })
        htm_content = urllib.request.urlopen(
            'http://www.youtube.com/results?' + query
        )
        search_results = re.findall('href=\"\\/watch\\?v=(.{11})',htm_content.read().decode())
        await ctx.send('https://www.youtube.com/watch?v='+search_results[0])
        '''

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
@client.command(pass_context=True)
async def stop(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop()
