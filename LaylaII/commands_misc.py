# ==============================================================================
# misc commands
# ==============================================================================

from init import *

# command hello
@withrepr(lambda x: 'check the aliveness of the bot')
@client.command()
async def hello(ctx):
    await ctx.send(embed=discord.Embed(title='Hi there hello.',color=0xb07bff))

# command forcequit
@client.command()
async def forcequit(ctx):
    if ctx.message.author.id == Bot.owner:
        await ctx.send('Forcequitted by owner.')
        sys.exit()

# command say
@withrepr(lambda x: 'say whatever cursed shit you want it to')
@client.command()
async def say(ctx, *, msg):
    await ctx.send(msg)

# command mock
@withrepr(lambda x: 'make text look lIkE tHiS')
@client.command()
async def mock(ctx, *, msg):
    msg = msg.lower()
    new = ''
    for i in range(len(msg)):
        if i%2 == 1: new += msg[i].upper()
        else: new += msg[i]

    await ctx.send(new)

@withrepr(lambda x: 'make text look   l i k e   t h i s')
@client.command()
async def wide(ctx, *, msg):
    r = ''
    for i in msg:
        if i == '': r += '   '
        else: r += i+' '
    await ctx.send(r)


thiccDicct = {
'a':'卂',
'b':'乃',
'c':'匚',
'd':'刀',
'e':'乇',
'f':'下',
'g':'厶',
'h':'卄',
'i':'工',
'j':'丁',
'k':'长',
'l':'乚',
'm':'从',
'n':'ん',
'o':'口',
'p':'尸',
'q':'㔿',
'r':'尺',
's':'丂',
't':'丅',
'u':'凵',
'v':'リ',
'w':'山',
'x':'乂',
'y':'丫',
'z':'乙',
' ':'　'}

@withrepr(lambda x: 'make text look 乚工长乇　丅卄工丂')
@client.command()
async def thicc(ctx, *, msg):
    r = ''
    msg = msg.lower()
    for i in msg:
        try:
            r += thiccDicct[i]
        except KeyError:
            r += i
    await ctx.send(r)

aussieDict = {
'a':'ɐ',
'b':'q',
'c':'ɔ',
'd':'p',
'e':'ǝ',
'f':'ɟ',
'g':'ƃ',
'h':'ɥ',
'i':'ᴉ',
'j':'ɾ',
'k':'ʞ',
'l':'l',
'm':'ɯ',
'n':'u',
'o':'o',
'p':'d',
'q':'b',
'r':'ɹ',
's':'s',
't':'ʇ',
'u':'n',
'v':'ʌ',
'w':'ʍ',
'x':'x',
'y':'ʎ',
'z':'z',
'A':'∀',
'B':'ꓭ',
'C':'Ɔ',
'D':'p',
'E':'Ǝ',
'F':'Ⅎ',
'G':'פ',
'H':'H',
'I':'I',
'J':'ſ',
'K':'ʞ',
'L':'˥',
'M':'W',
'N':'N',
'O':'O',
'P':'Ԁ',
'Q':'Q',
'R':'ɹ',
'S':'S',
'T':'┴',
'U':'∩',
'V':'Λ',
'W':'M',
'X':'X',
'Y':'λ',
'Z':'Z',}

@withrepr(lambda x: 'make text look sᴉɥʇ ǝʞᴉlˢ')
@client.command()
async def aussie(ctx, *, msg):
    r = ''
    msg = msg[::-1]
    for i in msg:
        try:
            r += aussieDict[i]
        except KeyError:
            r += i
    await ctx.send(r)

smolDict = {
'a':'ᵃ',
'b':'ᵇ',
'c':'ᶜ',
'd':'ᵈ',
'e':'ᵉ',
'f':'ᶠ',
'g':'ᵍ',
'h':'ʰ',
'i':'ᶦ',
'j':'ʲ',
'k':'ᵏ',
'l':'ˡ',
'm':'ᵐ',
'n':'ⁿ',
'o':'ᵒ',
'p':'ᵖ',
'q':'ᑫ',
'r':'ʳ',
's':'ˢ',
't':'ᵗ',
'u':'ᵘ',
'v':'ᵛ',
'w':'ʷ',
'x':'ˣ',
'y':'ʸ',
'z':'ᶻ',
'A':'ᴬ',
'B':'ᴮ',
'C':'ᶜ',
'D':'ᴰ',
'E':'ᴱ',
'F':'ᶠ',
'G':'ᴳ',
'H':'ᴴ',
'I':'ᴵ',
'J':'ᴶ',
'K':'ᴷ',
'L':'ᴸ',
'M':'ᴹ',
'N':'ᴺ',
'O':'ᴼ',
'P':'ᴾ',
'Q':'Q',
'R':'ᴿ',
'S':'ˢ',
'T':'ᵀ',
'U':'ᵁ',
'V':'ν',
'W':'ᵂ',
'X':'ˣ',
'Y':'ʸ',
'Z':'ᶻ',}

@withrepr(lambda x: 'make text look ˡᶦᵏᵉ ᵗʰᶦˢ')
@client.command()
async def smol(ctx, *, msg):
    r = ''
    for i in msg:
        try:
            r += smolDict[i]
        except KeyError:
            r += i
    await ctx.send(r)

leetDict = {
'a':'4',
'b':'8',
'e':'3',
'h':'#',
'l':'1',
'o':'0',
'r':'Я',
's':'5',
't':'7',
'z':'2',}

@withrepr(lambda x: 'make text look 1ik3 7#i5')
@client.command()
async def leet(ctx, *, msg):
    r = ''
    msg = msg.lower()
    for i in msg:
        try:
            r += leetDict[i]
        except KeyError:
            r += i
    await ctx.send(r)
