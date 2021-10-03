import discord
from discord.ext import commands
from discord.utils import get

from pymongo import MongoClient
from asyncio import sleep

#music
from discord.ext import tasks
from discord.voice_client import VoiceClient
import youtube_dl
from random import choice
import asyncio

import sys
sys.path.append(".")
import serverJoin as serverJoin
import set as set
import embeds as embeds
import toDo as toDo
import imageToText as imageToText
import wolfram as wolfR
import sad as sad
import chatbot as chatbot

from dotenv import load_dotenv
from os import getenv
load_dotenv() 
MONGO_KEY = getenv("MONGO")
BOT_TOKEN_KEY = getenv("TOKEN")

#MONGO STUFF
cluster=MongoClient(MONGO_KEY, tls=True, tlsAllowInvalidCertificates=True)

#BACKGROUND BOT TASKS
def get_prefix(client,message):
    serverCollection = cluster["Servers"][str(message.guild.id)] 
    serverInfoPost = serverCollection.find_one({"_id":"SERVER INFO"})
    prefix = serverInfoPost["Prefix"]
    return prefix

client = commands.Bot(command_prefix = get_prefix)

#====== SETUP =====

#ON READY
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.listening, name="HYONK!"))
    print('Ready')

#ON SERVER JOIN
@client.event
async def on_guild_join(guild):
    await serverJoin.joinServer(guild,cluster["Servers"])

#===== TEST TRACKER ADMINS =====
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def settodo(ctx):
    await ctx.message.add_reaction("☑")
    await sleep(1)
    await ctx.message.delete() 
    await toDo.setChannel(ctx,client,cluster["Servers"])

@settodo.error
async def settodo_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Only server admins may set the to do channel!")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def settitle(ctx,*,title):
    await ctx.message.add_reaction("☑")
    await sleep(1)
    await ctx.message.delete() 
    await toDo.setTitle(ctx,title,client,cluster["Servers"])

@settitle.error
async def settitle_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Only server admins may set the weekly title!")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def add(ctx,day,*,item):
    await ctx.message.add_reaction("☑")
    await sleep(1)
    await ctx.message.delete()
    await toDo.add(ctx,day,item,client,cluster["Servers"])

@add.error
async def add_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Only server admins may add items!")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def remove(ctx,day,itemNumber:int):
    await ctx.message.add_reaction("☑")
    await sleep(1)
    await ctx.message.delete()
    await toDo.remove(ctx,day,itemNumber,client,cluster["Servers"])

@remove.error
async def remove_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Only server admins may remove items!")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def edit(ctx,day,itemNumber:int,*,edit):
    await ctx.message.add_reaction("☑")
    await sleep(1)
    await ctx.message.delete() 
    await toDo.edit(ctx,day,itemNumber,edit,client,cluster["Servers"])

@edit.error
async def edit_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Only server admins may edit items!")

@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def reset(ctx):
    await ctx.message.add_reaction("☑")
    await sleep(1)
    await ctx.message.delete() 
    await toDo.reset(ctx,cluster["Servers"])

@reset.error
async def reset_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        errorMsg = await ctx.send("Only server admins may rest the to do list!")
        await sleep(1)
        await ctx.message.delete() 
        await errorMsg.delete()

#===== MUSIC ====
youtube_dl.utils.bug_reports_message = lambda: ''

youtubeDLFormatOptions = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpegOptions = {'options': '-vn'}
youtubeDL = youtube_dl.YoutubeDL(youtubeDLFormatOptions)

class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: youtubeDL.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else youtubeDL.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpegOptions), data=data)

@client.command(pass_context=True, aliases=['j'])
async def join(ctx):
    connected = ctx.author.voice
    if not connected:
        await ctx.send("You need to be connected in a voice channel to use this command!")
        return
    global vc
    vc = await connected.channel.connect()
    
@client.command(pass_context=True, aliases=['dc'])
async def disconnect(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.disconnect()

@client.command(name='play', aliases=['p'])
async def play(ctx,*, url):
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    else:
        channel = ctx.message.author.voice.channel

    try:
        await channel.connect()
    except:
        print("")

    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        voice.stop()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(url, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' % e) if e else None)

    await ctx.send('`Now playing:` {}'.format(player.title))

@client.command(pass_context=True)
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.pause()
        await ctx.send("⏸ Music paused")
    else:
        await ctx.send("❗ Music is not playing right now")

@client.command(pass_context=True)
async def resume(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_paused():
        voice.resume()
        await ctx.send("▶ Resumed music")
    else:
        await ctx.send("❗ Music is not paused right now")

@client.command(pass_context=True)
async def stop(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("🛑 Music stopped")
    else:
        await ctx.send("❗ Nothing is playing right now")

#==== STUDY TOOLS =====

@client.command(pass_context=True)
async def imagetotext(ctx):
    prompt = await ctx.channel.send('Upload your image.')

    
    def check(m):
            return m.author.id == ctx.author.id and m.channel == ctx.channel

    try:
        image = await client.wait_for('message', check=check, timeout=10.0)
    except asyncio.TimeoutError:
        return await ctx.channel.send(f'Sorry, you took too long.')
    
    try:
        textResult = await imageToText.imageToText(image.attachments[0].url)
        if textResult != "" and textResult.isspace() == False:
            await ctx.send(f"{ctx.message.author.mention} The following text was extracted from your image:")
            await ctx.send(f"`{textResult}`")
        else:
            await ctx.send(f"{ctx.message.author.mention} No text was extracted from your image, try a different image or taking a clearer image.")
    except:
        await ctx.send("No image detected")

pinned = []

@client.command()
async def pin(ctx):
    messages = []
    async for message in ctx.channel.history(limit=2):
        messages.append(message)
    if len(pinned) == 50:
        pinned.pop(0)
    try:
        await messages[1].pin()
        pinned.append(messages[1])
        await messages[1].add_reaction("📌")
        await messages[1].add_reaction("❌")
        await ctx.channel.purge(limit=2)
    except:
        print("cannot pin")

@client.event
async def on_reaction_add(reaction, user):
    temp_message = reaction.message
    if user != client.user:
        if str(reaction.emoji) == "❌":
            await reaction.message.unpin()
            await reaction.message.remove_reaction("❌", user)
            await reaction.message.remove_reaction("📌", user)
            await reaction.message.remove_reaction("📌", client.user)
            await reaction.message.remove_reaction("❌", client.user)
    if user != client.user:
        if str(reaction.emoji) == "📌":
            await reaction.message.pin()
            await reaction.message.add_reaction("📌")
            await reaction.message.add_reaction("❌")

@client.command(pass_context=True)
async def question(ctx,*,question):
    print(question)
    answer = await wolfR.wolfram(question)
    await ctx.send(answer)

#==== FUN COMMANDS ====
#SCREAM
@client.command(pass_context=True)
async def scream(ctx):
    await ctx.send(sad.scream())

#CRY
@client.command(pass_context=True)
async def cry(ctx):
    await ctx.send(sad.cry())

#====== GENERAL =====
#CHATBOT
@client.event
async def on_message(ctx):
    mention = f'<@!{client.user.id}>'
    if mention in ctx.content or "study goose" in ctx.content.lower():
        message = ctx.content.replace(f'<@!{client.user.id}>',"")
        message = message.lower()
        message = message.replace("study goose","")

        #allows bot to access sync function from an async function
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, chatbot.response, message)

        await ctx.channel.send(result)
    await client.process_commands(ctx)


#HELP
client.remove_command("help")
@client.command(invoke_without_command = True)
async def help(ctx,cmd=None):
    print("help")
    await ctx.send(embed=embeds.help(cmd,get_prefix(client,ctx)))

#SET PREFIX
@client.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def setprefix(ctx,newPrefix):
    if len(newPrefix)<=5 and len(newPrefix)>=1:
        set.prefix(ctx,newPrefix,cluster["Servers"])
        await ctx.send(f"My new prefix is `{newPrefix}`.")
    else:
        await ctx.send("Prefixes can only be 1-5 characters in length.")
    
@setprefix.error
async def setprefix_error(ctx,error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Only server admins may edit my prefix!")
    
#SUGGEST
@client.command(pass_context=True)
async def suggest(ctx,*,suggestion):
    if len(suggestion)>5:
        channel = client.get_channel(867188026982268968)
        embed=discord.Embed(title=f"{ctx.author} aka {ctx.author.display_name}", description=suggestion)
        embed.set_thumbnail(url=ctx.author.avatar_url)
        await channel.send(embed=embed)

#ERROR ================================================================================================================
@client.event
async def on_command_error(ctx,error):
    if isinstance(error,commands.BadArgument):
        await ctx.send("❓  Invalid argument entered.")
    elif isinstance(error,commands.MissingRequiredArgument):
        await ctx.send("❓  Missing argument(s).")

client.run(BOT_TOKEN_KEY)