import discord, chalk
from discord.ext import commands
import time
import os
import asyncio
import gtts
from gtts import gTTS
import time
client = commands.Bot(command_prefix = "!")

queue = {}
dil = {}
discon = {}
wait = {}
@client.command(
    name='yardım',
    description='yardım',
    pass_context=True,
)
async def yardim(ctx):
    await ctx.send('Varsayılan dil tr (Türkçe).\n!dil dilKodu (Dili değiştirmek için kullanılır (örneğin en, de))\n!diller (Kullanılabilir dilleri gösterir)\n!söyle metin(Metni okur)\n!sus (Susar ve kanaldan çıkar)\n!yardım (Yardım mesajını gösterir)')
@client.command(
    name='sus',
    description='sus',
    pass_context=True,
)
async def dis(ctx):
    global discon
    discon[str(ctx.guild.id)] = True
@client.command(
    name='dil',
    description='dil',
    pass_context=True,
)
async def dilke(ctx, arg):
    global dil
    langs = gtts.tts.tts_langs()
    if arg in langs:
        dil[str(ctx.guild.id)] = str(arg)
        await ctx.send("Dil " + langs[arg] + " olarak değiştirildi.")
    else:
        await ctx.send("Girdiğiniz dil geçerli değil!")
@client.command(
    name='diller',
    description='diller',
    pass_context=True,
)
async def dillerd(ctx):
    langs = gtts.tts.tts_langs()
    await ctx.send("Kullanılabilir diller:\n" + str(langs))
@client.command(
    name='söyle',
    description='söyle',
    pass_context=True,
)
async def soyle(ctx, *args):
    global queue
    global dil
    global discon
    global wait
    if(str(ctx.guild.id) not in discon):
        discon[str(ctx.guild.id)] = False
    if(str(ctx.guild.id) not in dil):
        dil[str(ctx.guild.id)] = "tr"
    arg = ' '.join(args)
    if(arg==""):
        return
    if(len(arg) > 120):
        await ctx.send("Mesaj çok uzun!")
        return
    voice_channel=ctx.author.voice.channel
    if voice_channel!= None:
        voice = discord.utils.get(client.voice_clients, guild=ctx.guild)
        if voice == None:
            try:
                queue[str(ctx.guild.id)].append(arg)
            except:
                queue[str(ctx.guild.id)] = [arg]
            vc= await voice_channel.connect()
            while True:
                if(discon[str(ctx.guild.id)]):
                    await vc.disconnect()
                    discon[str(ctx.guild.id)] = False
                    queue[str(ctx.guild.id)] = []
                    break
                while len(queue[str(ctx.guild.id)]) != 0:
                    if(discon[str(ctx.guild.id)]):
                        await vc.disconnect()
                        discon[str(ctx.guild.id)] = False
                        queue[str(ctx.guild.id)] = []
                        break
                    arg = queue[str(ctx.guild.id)].pop(0)
                    sondil = str(dil[str(ctx.guild.id)])
                    tts = gTTS(arg, lang=sondil, tld='com')
                    tts.save(str(ctx.guild.id)+ '.mp3')
                    vc.play(discord.FFmpegPCMAudio(str(ctx.guild.id)+'.mp3'), after=lambda e: print('done', e))   
                    while vc.is_playing():
                        if(discon[str(ctx.guild.id)]):
                            queue[str(ctx.guild.id)] = []
                            break
                        await asyncio.sleep(1)
                    vc.stop()
                    os.remove(str(ctx.guild.id)+".mp3")
                    wait[str(ctx.guild.id)] = time.time()
                    if(discon[str(ctx.guild.id)]):
                        discon[str(ctx.guild.id)] = False
                        await vc.disconnect()
                        queue[str(ctx.guild.id)] = []
                        break
                await asyncio.sleep(1)
                if wait[str(ctx.guild.id)] + 120 < time.time():
                    await vc.disconnect()
                    queue[str(ctx.guild.id)] = []
                    break
        else:
            if(discon[str(ctx.guild.id)]):
                discon[str(ctx.guild.id)] = False
                await voice.disconnect()
                queue[str(ctx.guild.id)] = []
            else:
                try:
                    queue[str(ctx.guild.id)].append(arg)
                except:
                    queue[str(ctx.guild.id)] = [arg]
client.run('bot-token')