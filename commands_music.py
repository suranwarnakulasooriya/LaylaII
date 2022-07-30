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
'options': '-y -vn'}

def retrieve(arg): # return title, url, and duration of top result of search
    with YoutubeDL({'format': 'bestaudio', 'noplaylist':'True','agelimit':'18'}) as ydl:
        info = ydl.extract_info(f"ytsearch:{arg}", download=False)['entries'][0]
    return (info['title'], info['formats'][0]['url'], info['duration'])

def to_seconds(timestr): # convert hh:mm:ss to raw seconds
    seconds = 0
    for part in timestr.split(':'):
        seconds = seconds*60 + int(part, 10)
    return seconds

def get_time(sec,Q=False,l=0,ln=65): # convert time from raw seconds into hh:mm:ss
    dur = str(td(seconds=sec))
    for i in range(len(dur)):
        if dur[i] not in ['0',':']:
            dur = dur[i:]; break
    for i in range(len(dur)):
        if dur[-i] == '.':
            dur = dir[:i-1]; break
    # always at least show the single minutes
    if len(dur) == 1: dur = '0:0'+dur
    elif len(dur) == 2: dur = '0:'+dur
    # if this is for the queue (or search), make sure the time is always aligned
    if Q:
        if len(dur) > 8: dur = 'OVER'
        dur = ' '*(ln-l-len(dur)) + dur
        while l+len(dur) < ln+3: dur = ' '+dur
    return dur

def trim_title(name,l=62): # trim the title if it is too long (to keep times aligned in queue)
    if len(name) > l: return name[:l-2]+'...'
    else: return name

def wrap_index(index,L): # make index positive if it is negative
    if 0 <= index < len(L): return index
    elif 0 > index: return len(L)+index

async def enqueue(ctx,query): # effectively the play command but separate since it's used in result and play
    if not ctx.author.voice:
        await ctx.send(embed=discord.Embed(description="You need to be in a voice channel.",color=red,footer="Glory to The Party!"))

    elif not Bot.connected: # connect to VC if not already
        try:
            await ctx.author.voice.channel.connect(); Bot.connected = True
        except: await ctx.send(embed=discord.Embed(description="Something went wrong.",color=red,footer="Glory to The Party!"))

    if Bot.connected:
        if len(Q.queue) > 19:
            await ctx.send(embed=discord.Embed(description='Queue is maxed out.',color=red))
        else:
            if 'https' in query and '&' in query: # if query is a url, remove extraneous parts of url (timestamps and/or playlist info)
                query = query[:query.index('&')]

            # search youtube for query (searching a url will return the url so code can be reused)
            title, url, duration = retrieve(query)
            dur = get_time(duration,False)
            if len(Q.queue) == Q.current == 0:
                await ctx.send(embed=discord.Embed(description=f"Now Playing {title} [{dur}] [{ctx.author.mention}]",color=green,footer="Glory to The Party!"))
                stopwatch.Reset(); stopwatch.Start()
                Q.loop = False
            else: await ctx.send(embed=discord.Embed(description=f"Queued {title} [{dur}] [{ctx.author.mention}]",color=grey,footer="Glory to The Party!"))

            Q.queue.append(Song(title,url,dur,ctx.author.mention,duration)) # add song to queue
            if Q.current == len(Q.queue)-1:
                try: ctx.guild.voice_client.play(FFmpegPCMAudio(url, **FFMPEG_OPTS),after=lambda e:stopwatch.Reset()) # play song
                except: pass

@withrepr(lambda x: "Get top 10 search results.")
@client.command(pass_context=True)
async def search(ctx,*,query): # return title, duration, and url of top 10 search results
    info = YoutubeSearch(query,max_results=10).to_dict()
    msg = '```'
    for e,i in enumerate(info):
        msg += f"{e}) {trim_title(i['title'],60)}  {get_time(to_seconds(i['duration']),True,len(trim_title(i['title'],60)),63)}\n"
    msg += '```'
    # sometimes the search comes up empty for no reason, searching the same thing again fixes it
    if msg == '``````': await ctx.send(embed=discord.Embed(description='Search failed. Search the same thing again and it should work ¯\_(ツ)_/¯.',color=red,footer="Glory to The Party!"))
    else:
        msg += 'To play a song from this list, use result <index>.'
        await ctx.send(msg)
        Q.search = []
        for song in info: Q.search.append('https://www.youtube.com'+song['url_suffix'])


@withrepr(lambda x: "Play the index of a search result. Alias = res.")
@client.command(aliases=['res'],pass_context=True)
async def result(ctx,index:int):
    if Q.search == []:
        await ctx.send(embed=discord.Embed(description="There are no search results, use search to get some.",color=red,footer="Glory to The Party!"))
    elif index < 0 or index > 9:
        await ctx.send(embed=discord.Embed(description="Index out of range.",color=red,footer="Glory to The Party!"))
    else:
        await enqueue(ctx,Q.search[index])


@withrepr(lambda x: 'Play the audio of a YouTube URL or from YouTube search. Alias = p.')
@client.command(aliases=['p'],pass_context=True)
async def play(ctx, *, query : str):
    await enqueue(ctx,query)


@withrepr(lambda x: 'Show the queue. Alias = q.')
@client.command(aliases=['q'],pass_context=True)
async def queue(ctx):
    if len(Q.queue) == 0: await ctx.send(embed=discord.Embed(description='Queue is empty.',color=grey,footer="Glory to The Party!"))
    else:
        message = "```"
        for i,song in enumerate(Q.queue):
            if i > 9: l = len(trim_title(song.title))+1
            else: l = len(trim_title(song.title))
            if i == Q.current:
                message += f"\n{i}) {trim_title(song.title)}  {get_time(song.rawtime-stopwatch.GetTime(),True,l)} <=="
                if Q.loop: message += ' loop'
            else: message += f"\n{i}) {trim_title(song.title)}  {get_time(song.rawtime,True,l)}"
        message += '```'
        await ctx.send(message)


@withrepr(lambda x: 'Join the voice channel of the author. Alias = j.')
@client.command(aliases=['j'],pass_context=True)
async def join(ctx):
    if not Bot.connected and ctx.author.voice:
        channel = ctx.author.voice.channel
        voice = await channel.connect()
        Bot.connected = True
    elif not Bot.connected and not ctx.author.voice:
        await ctx.send(embed=discord.Embed(description='You need to be in a voice channel.',color=red,footer="Glory to The Party!"))


@withrepr(lambda x: 'Leave the voice channel. Aliases = die,l.')
@client.command(aliases=['fuckoff','die','getout','l'],pass_context=True)
async def leave(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if ctx.guild.voice_client in client.voice_clients and ctx.author.voice:
        await voice.disconnect()
        Bot.connected = False
        Q.queue = []; stopwatch.Reset(); Q.current = 0
    else: await ctx.send(embed=discord.Embed(description='No voice channel to leave from.',color=red,footer="Glory to The Party!"))


@withrepr(lambda x: 'Pause the current song.')
@client.command(pass_context=True)
async def pause(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_playing(): voice.pause(); stopwatch.Pause()
    else: await ctx.send(embed=discord.Embed(description='Already paused.',color=red,footer="Glory to The Party!"))


@withrepr(lambda x: 'Resume the current song.')
@client.command(pass_context=True)
async def resume(ctx):
    voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
    if voice.is_paused(): voice.resume(); stopwatch.Resume()
    else: await ctx.send(embed=discord.Embed(description='Not already paused.',color=red,footer="Glory to The Party!"))


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
    if not Q.loop: Q.current += 1
    try:
        ctx.guild.voice_client.play(FFmpegPCMAudio(Q.queue[Q.current].url, **FFMPEG_OPTS),after=lambda e:stopwatch.Reset())
        await ctx.send(embed=discord.Embed(description=f"Now Playing {Q.queue[Q.current].title} [{Q.queue[Q.current].length}] [{Q.queue[Q.current].request}]",color=green,footer="Glory to The Party!"))
        stopwatch.Reset(); stopwatch.Start()
    except IndexError: Q.current -=1; await ctx.send(embed=discord.Embed(description="No more songs to play.",color=red,footer="Glory to The Party!"))


@withrepr(lambda x: 'Removes a given index from the queue. Aliases = r,rm,rmv.')
@client.command(aliases=['r','rm','rmv'],pass_context=True)
async def remove(ctx,index:int):
    try:
        if index != Q.current:
            song = Q.queue.pop(index)
            if index < Q.current and index >= 0: Q.current -= 1
            await ctx.send(embed=discord.Embed(description=f"Removed Index {index}: {song.title}",color=grey,footer="Glory to The Party!"))
        else: await ctx.send(embed=discord.Embed(description="Pls don't do that.",color=red,footer="Glory to The Party!"))
    except: await ctx.send(embed=discord.Embed(description="There's no song at that index.",color=red,footer="Glory to The Party!"))


@withrepr(lambda x: "Clear the queue (use if queue is broken). Aliases = cl,c.")
@client.command(aliases=['cl','c'],pass_context=True)
async def clear(ctx):
    Q.queue = []; Q.current = 0; Q.search = []
    await ctx.send(embed=discord.Embed(description="Queue has been cleared.",color=grey,footer="Glory to The Party!"))


@withrepr(lambda x: 'Toggle song loop.')
@client.command(pass_context=True)
async def loop(ctx):
    if Q.loop: Q.loop = False; await ctx.send(embed=discord.Embed(description='Loop stopped.',color=grey,footer="Glory to The Party!"))
    else: Q.loop = True; await ctx.send(embed=discord.Embed(description='Now looping current song.',color=grey,footer="Glory to The Party!"))


@withrepr(lambda x: "See the current song.")
@client.command(aliases=['nowplaying'],pass_context=True)
async def np(ctx):
    if len(Q.queue) == 0: await ctx.send(embed=discord.Embed(description='No song playing.',color=grey,footer="Glory to The Party!"))
    elif stopwatch.GetTime() >= Q.queue[Q.current].rawtime: await ctx.send(embed=discord.Embed(description='No song playing.',color=grey,footer="Glory to The Party!"))
    else:
        p = int(stopwatch.GetTime()/Q.queue[Q.current].rawtime*25)
        bar = '▬'*p + ':purple_circle:' + '▬'*(25-p)
        await ctx.send(embed=discord.Embed(description=f"""{Q.queue[Q.current].title} [{Q.queue[Q.current].request}] [{get_time(stopwatch.GetTime(),False)}/{Q.queue[Q.current].length}]\n
        {bar}""",color=grey,footer="Glory to The Party!"))


@withrepr(lambda x: "Manually set the current song if it isn't correct.")
@client.command(pass_context=True)
async def setcurrent(ctx,index:int):
    if index < len(Q.queue):
        Q.current = index
        await ctx.send(embed=discord.Embed(description=f"Current Song Set to Index {index}: {Q.queue[Q.current].title} [{Q.queue[Q.current].length}] [{Q.queue[Q.current].request}]",footer="Glory to The Party!"))
    else: await ctx.send(embed=discord.Embed(description="There's no song at that index.",color=red,footer="Glory to The Party!"))


@withrepr(lambda x: "Move a song in the queue.")
@client.command(aliases=['mv'],pass_context=True)
async def move(ctx,a:int,b:int):
    if a < len(Q.queue) and b < len(Q.queue) and a != Q.current and b != Q.current:
        Q.queue.insert(b,Q.queue[a])
        t = Q.queue[a].title
        if a < Q.current and b > Q.current: Q.current -= 1
        elif a > Q.current and b < Q.current: Q.current += 1
        if a > b:
            Q.queue.pop(a+1)
        else:
            Q.queue.pop(a)
        await ctx.send(embed=discord.Embed(description=f"Moved index {a} ({t}) to position {b}.",footer="Glory to The Party!"))


@withrepr(lambda x: "Jump to a position in the queue.")
@client.command(pass_context=True)
async def jump(ctx,index:int):
    try:
        index = wrap_index(index,Q.queue)
        _ = Q.queue[index]
        if index != Q.current: Q.loop = False
        Q.current = index
        voice = discord.utils.get(client.voice_clients,guild=ctx.guild)
        voice.stop(); stopwatch.Reset()
        ctx.guild.voice_client.play(FFmpegPCMAudio(Q.queue[Q.current].url, **FFMPEG_OPTS),after=lambda e:stopwatch.Reset())
        await ctx.send(embed=discord.Embed(description=f"Now Playing {Q.queue[Q.current].title} [{Q.queue[Q.current].length}] [{Q.queue[Q.current].request}]",color=green,footer="Glory to The Party!"))
        stopwatch.Start()
    except IndexError: await ctx.send(embed=discord.Embed(description="There's no song at that index.",color=red,footer="Glory to The Party!"))


@withrepr(lambda x: "Tell the bot that its not connected (use if manually disconnected).")
@client.command(pass_context=True)
async def disconnect(ctx):
  if Bot.connected: await ctx.send(embed=discord.Embed(description="Disconnected.",color=green,footer="Glory to The Party!")); Bot.connected = False

@withrepr(lambda x: "Clear all items in the queue before the curent song.")
@client.command(pass_context=True)
async def buffer(ctx):
    Q.queue = Q.queue[Q.current:]
    await ctx.send(embed=discord.Embed(description="Queue buffered.",color=green))
    Q.current = 0

@withrepr(lambda x: "READ ME PLEASE.")
@client.command(pass_context=True)
async def readme(ctx):
    embed = discord.Embed(title='DISCLAIMER',description="""The music commands are subject to bugs that are outside of my control. Here's how to get around them.\n
    If the bot says it started playing something but there's no audio, wait a little longer, the time it takes to begin streaming audio varies.
    If the audio never starts, it might have been randomly denied (it should say the song is over in the queue), requeue the song and skip to it (.next).\n
    Sometimes the audio prematurely cuts off, this might be because the video is buffering, so wait for a little bit. If the song doesn't continue, requeue the song and skip to it.\n
    Sometimes the current song (marked by <== in the queue) is not accurate. Try to use .setcurrent to correct it. If it doesnt work, clear the queue.\n
    As far as I know, clearing the queue always solves these issues. Using .leave also clears the queue. The results for the search commands are inconsistent.
    .remove -1 is the fastest way to remove the last song in the queue. The search panel occasionally comes up empty, this is also a package issue, just search the same thing again.
    If the bot isnt joining voice but says its queued music, use .connect to toggle the connection and it might still think it is conneced. Disconnecting the bot forces me to restart it, don't make me do that.
    I would also advise against sending commands in quick succession, just to be safe.""",color=purple,footer="Glory to The Party!")
    embed.set_footer(text='Always remember: this bot is better than Rythm.')
    await ctx.send(embed=embed)
