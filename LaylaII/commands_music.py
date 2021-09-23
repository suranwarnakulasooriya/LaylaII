# ==============================================================================
# music
# ==============================================================================

from init import *

# set ytdl and ffmpeg options
ydl_opts = {
'format': 'bestaudio/best',
'postprocessors': [{
    'key': 'FFmpegExtractAudio','preferredcodec': 'mp3',
    'preferredquality': '192','noplaylist':'True'}]}

FFMPEG_OPTS = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
'options': '-vn'}

def retrieve(arg): # return title, url, and duration of top result of search
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True','cookies':'cookies.txt'}) as ydl:
        info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
    return (info['title'], info['formats'][0]['url'], info['duration'])


def get_time(sec): # convert time from raw seconds into human time
    dur = str(td(seconds=sec))
    for i in range(len(dur)):
        if dur[i] not in ['0',':']:
            dur = dur[i:]; break
    for i in range(len(dur)):
        if dur[-i] == '.':
            dur = dir[:i-1]; break
    if len(dur) == 1: dur = '0:0'+dur
    elif len(dur) == 2: dur = '0:'+dur
    return dur


#@client.command(pass_context=True)
async def search(ctx,*,query): # get top 10 search results
    results = []
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True','cookies':'cookies.txt'}) as ydl:
        for i in range(10):
            results.append(ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][i])
            await ctx.send(results[-1]['title'])
    message = ''
    for result in results:
        message += '\n'+result['title']


@withrepr(lambda x: 'Play the audio of a YouTube URL or from YouTube search. Aliases = p.')
@client.command(aliases=['p'],pass_context=True)
async def play(ctx, *, query : str):

    if not ctx.author.voice:
        await ctx.send(embed=discord.Embed(description="You need to be in a voice channel.",color=0xe74c3c))

    elif not Bot.connected: # connect to VC if not already
        try:
            channel = ctx.author.voice.channel
            voice = await channel.connect()
            Bot.connected = True
        except: await ctx.send(embed=discord.Embed(description="You need to be in a voice channel.",color=0xe74c3c))

    if ctx.author.voice and Bot.connected:

        if len(Q.queue) > 19:
            await ctx.send(embed=discord.Embed(description='Queue is maxed out.',color=0xe74c3c))
        else:

            if 'https' in query: # if query is a url, remove extraneous parts of url
                url = query
                try: url = url[:url.index('&')]
                except ValueError: pass

            # search youtube for query (searching a url will return the url)
            title, url, duration = retrieve(query)
            dur = get_time(duration)

            # flavor text
            #if len(Q.queue) > 0 and Q.current != len(Q.queue)-1:
            #    await ctx.send(embed=discord.Embed(description=f"Now Playing {title} [{dur}] [{ctx.author.mention}]",color=0x3ce74c))
            #    stopwatch.Start()
            if len(Q.queue) == Q.current == 0:
                await ctx.send(embed=discord.Embed(description=f"Now Playing {title} [{dur}] [{ctx.author.mention}]",color=0x3ce74c))
                stopwatch.Reset(); stopwatch.Start()
                Q.loop = False
            else:
                await ctx.send(embed=discord.Embed(description=f"Queued {title} [{dur}] [{ctx.author.mention}]",color=0x99a3a4))

            Q.queue.append(Song(title,url,dur,ctx.author.mention,duration)) # add song to queue

            if Q.current == len(Q.queue)-1:
                try: ctx.guild.voice_client.play(FFmpegPCMAudio(url, **FFMPEG_OPTS)) # play song
                except: pass


@withrepr(lambda x: 'Show the queue. Aliases = q.')
@client.command(aliases=['q'],pass_context=True)
async def queue(ctx):
    message = "```"
    for i,song in enumerate(Q.queue):
        if i == Q.current:
            message += f"\n{i}) {song.title}  {get_time(song.rawtime-stopwatch.GetTime())} <=="
        else:
            message += f"\n{i}) {song.title}  {song.length}"
    if Q.loop: message += "\nThe current song is being looped."
    message += '```'
    if message == '``````' or message == '```\nThe current song is being looped.```': await ctx.send(embed=discord.Embed(description='Queue is empty.',color=0x99a3a4))
    else: await ctx.send(message)


@withrepr(lambda x: 'Join the voice channel of the author. Aliases = j.')
@client.command(aliases=['j'],pass_context=True)
async def join(ctx):
    if not Bot.connected and ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        Bot.connected = True
    elif not Bot.connected and not ctx.author.voice:
        await ctx.send(embed=discord.Embed(description='You need to be in a voice channel.',color=0xe74c3c))


@withrepr(lambda x: 'Leave the voice channel. Aliases = die,l.')
@client.command(aliases=['fuckoff','die','getout','l'],pass_context=True)
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if ctx.guild.voice_client in client.voice_clients:
        await voice.disconnect()
        Bot.connected = False
        Q.queue = []
        Stopwatch.Reset()
    else: await ctx.send(embed=discord.Embed(description='No voice channel to leave from.',color=0xe74c3c))


@withrepr(lambda x: 'Pause the current song.')
@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing(): voice.pause(); stopwatch.Pause()
    else: await ctx.send(embed=discord.Embed(description='Already paused.',color=0xe74c3c))


@withrepr(lambda x: 'Resume the current song.')
@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused(): voice.resume(); stopwatch.Resume()
    else: await ctx.send(embed=discord.Embed(description='Not already paused.',color=0xe74c3c))

@withrepr(lambda x: 'Stops the current song.')
@client.command(pass_context=True)
async def stop(ctx,manual=True):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop(); stopwatch.Reset()
    if Q.loop: Q.loop = False


@withrepr(lambda x: 'Starts the next song. Aliases = nxt,n,start,skip.')
@client.command(aliases=['nxt','n','start','skip'],pass_context=True)
async def next(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    voice.stop(); stopwatch.Reset()
    if not Q.loop:
        Q.current += 1
    try:
        ctx.guild.voice_client.play(FFmpegPCMAudio(Q.queue[Q.current].url, **FFMPEG_OPTS))
        await ctx.send(embed=discord.Embed(description=f"Now Playing {Q.queue[Q.current].title} [{Q.queue[Q.current].length}] [{Q.queue[Q.current].request}]",color=0x3ce74c))
        stopwatch.reset(); stopwatch.Start()
    except IndexError: await ctx.send(embed=discord.Embed(description="No more songs to play.",color=0xe74c3c))


@withrepr(lambda x: 'Removes a given index from the queue. Aliases = r,rm,rmv.')
@client.command(aliases=['r','rm','rmv'],pass_context=True)
async def remove(ctx,index:int):
    try:
        if index != Q.current:
            song = Q.queue.pop(index)
            if index < Q.current and index >= 0: Q.current -= 1
            await ctx.send(embed=discord.Embed(description=f"Removed Index {index}: {song.title}",color=0x99a3a4))
        else:
            await ctx.send(embed=discord.Embed(description="Pls don't do that.",color=0xe74c3c))
    except: await ctx.send(embed=discord.Embed(description="There's no song at that index.",color=0xe74c3c))


@withrepr(lambda x: "Clear the queue (use if queue is broken). Aliases = cl,c.")
@client.command(aliases=['cl','c'],pass_context=True)
async def clear(ctx):
    Q.queue = []
    Q.current = 0
    await ctx.send(embed=discord.Embed(description="Queue has been cleared.",color=0x99a3a4))


@withrepr(lambda x: 'Toggle song loop.')
@client.command(pass_context=True)
async def loop(ctx):
    if Q.loop: Q.loop = False; await ctx.send(embed=discord.Embed(description='Loop stopped.',color=0x99a3a4))
    else: Q.loop = True; await ctx.send(embed=discord.Embed(description='Now looping current song.',color=0x99a3a4))

@withrepr(lambda x: "See the current song.")
@client.command(aliases=['nowplaying'],pass_context=True)
async def np(ctx):
    if len(Q.queue) == 0:
        await ctx.send(embed=discord.Embed(description='No song playing.',color=0x99a3a4))
    elif stopwatch.GetTime() >= Q.queue[Q.current].rawtime:
        await ctx.send(embed=discord.Embed(description='No song playing.',color=0x99a3a4))
    else:
        p = int(stopwatch.GetTime()/Q.queue[Q.current].rawtime*25)
        bar = '▬'*p + ':purple_circle:' + '▬'*(25-p)
        await ctx.send(embed=discord.Embed(description=f"""{Q.queue[Q.current].title} [{Q.queue[Q.current].request}] [{get_time(stopwatch.GetTime())}/{Q.queue[Q.current].length}]\n
        {bar}""",color=0x99a3a4))

@withrepr(lambda x: "Manually set the current song if it isn't correct.")
@client.command(pass_context=True)
async def setcurrent(ctx,index:int):
    if index < len(Q.queue):
        Q.current = index
        await ctx.send(embed=discord.Embed(description=f"Current Song Set to Index {index}: {Q.queue[Q.current].title} [{Q.queue[Q.current].length}] [{Q.queue[Q.current].request}]"))
    else: await ctx.send(embed=discord.Embed(description="There's no song at that index.",color=0xe74c3c))

@withrepr(lambda x: "READ ME PLEASE.")
@client.command(pass_context=True)
async def readme(ctx):
    embed = discord.Embed(title='DISCLAIMER',description="""The music commands are subject to bugs that are outside of my control. Here's how to get around them.\n
    If the bot says it started playing something but there's no audio, wait a little longer, the time it takes to begin streaming audio varies. If the audio never starts, requeue the song and skip to it (.next).\n
    Sometimes the audio prematurely cuts off, this might be because the video is buffering, so wait for a little bit. If the song doesn't continue, requeue the song and skip to it.\n
    Sometimes the current song (marked by <== in the queue) is not accurate. Try to use .setcurrent to correct it. If it doesnt work, clear the queue.\n
    As far as I know, clearing the queue always solves these issues. Using .leave also clears the queue.
    .remove -1 is the fastest way to remove the last song in the queue.
    Please don't disconnect the bot from voice. Just use .leave. Disconnecting the bot forces me to restart it, don't make me do that.
    I would also advice against sending commands in quick succession, just to be safe.""",color=0xb07bff)
    embed.set_footer(text='Always remember: this bot is better than Rythm.')
    await ctx.send(embed=embed)
