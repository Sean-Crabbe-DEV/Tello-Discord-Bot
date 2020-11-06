#################### Installing Discord.py
# Windows
# py -3 -m pip install -U discord.py[voice]
# Linux/macOS
# python3 -m pip install -U "discord.py[voice]"

#################### Installing 
# Windows
# py -3 -m  pip install asyncio
# Linux/macOS
# python3 -m pip install -U "asyncio"

#################### Installing youtube_dl
# Windows
# py -3 -m pip install youtube_dl
# Linux/macOS
# python3 -m pip install -U "youtube_dl"

# Imports Modules
import os
import sys
import time
import socket
import random
import asyncio
import discord
import platform
import threading
import youtube_dl
from discord import User
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot, Greedy
from discord import FFmpegPCMAudio
from youtube_dl import YoutubeDL

################## Discord Bot
client = discord.Client()
client = commands.Bot(command_prefix = '!')#Defines Prefix For Bot To Respond To
client.remove_command('help')

############################################ Events

################### On Ready
@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Navigateing The Skys'))
    print('Bot is online!')


################### On Member Join
@client.event
async def on_guild_join(guild):
    for channel in guild.text_channels:
        if channel.permissions_for(guild.me).send_messages:
            await channel.send(f"""{member.mention}server""")
        break

@client.event
async def on_member_remove(member):
    for channel in member.guild.channels:
        if str(channel) == "general": # We check to make sure we are sending the message in the general channel
            await channel.send_message(f"""{member.mention} has left the server""")

############################################ Commands
       
################### Ping
@client.command()
async def ping(ctx):
    await ctx.send(f'Pong! The ping is {round(client.latency * 1000, 2)}ms')

################### Server Info
@client.command(name='server')
async def serverinfo(context):
    guild = context.guild
    
    await context.send(f'Server Name: {guild.name}')
    await context.send(f'Server Size: {len(guild.members)}')
    await context.send(f'Server Name: {guild.owner.display_name}')
    
################### Drone Controls Help
@client.command()
async def controls(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.orange()
    )
    test_e.set_author(name="Tello Controls")
    test_e.add_field(name="!D command", value="Puts the tello into SDK mode", inline=False)
    test_e.add_field(name="!D takeoff", value="Drone auto takesoff", inline=False)
    test_e.add_field(name="!D land", value="Drone auto lands", inline=False)
    test_e.add_field(name="!D emergency", value="Stops all motors", inline=False)
    test_e.add_field(name="!D up x", value="Moves drone up by x cm", inline=False)
    test_e.add_field(name="!D down x", value="Moves drone down by x cm", inline=False)
    test_e.add_field(name="!D forward x", value="Moves drone forward by x cm", inline=False)
    test_e.add_field(name="!D back x", value="Moves drone back by x cm", inline=False)
    test_e.add_field(name="!D cw x", value="Rotates drone clockwise by x degrees", inline=False)
    test_e.add_field(name="!D ccw x", value="Rotates drone counter clockwise by x degrees", inline=False)
    test_e.add_field(name="!D flip x", value="Flips drone in x direction. l (left), r (right), f (forward) and b (back)", inline=False)
    test_e.add_field(name="!D speed x", value="Sets speed to x cm/s", inline=False)
    test_e.add_field(name="!D speed?", value="gets current speed (cm/s)", inline=False)
    test_e.add_field(name="!D battery?", value="get current battery percentage", inline=False)
    test_e.add_field(name="!D time?", value="get current fly time (s)", inline=False)
    test_e.add_field(name="!D height?", value="get height (cm)", inline=False)
    test_e.add_field(name="Tello SDK", value="https://bit.ly/2Zs5Pf4")

    await author.send(embed=test_e) #Sends the list of controls via the users Direct Message
    await ctx.send("Check You DM ") #Sends on message on the server telling them to check their Direct messages
    
################### Help
@client.command()
async def help(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.orange()
    )
    test_e.set_author(name="Tello ATC Help")
    test_e.add_field(name="!ping", value="This will give you your ping", inline=False)
    test_e.add_field(name="!controls", value="Displays a list of the drones controls", inline=False)
    test_e.add_field(name="!join", value="Bot will join the voice channel you ar in", inline=False)
    test_e.add_field(name="!leave", value=" # ", inline=False)
    test_e.add_field(name="!play", value=" # ", inline=False)
    test_e.add_field(name="!skip", value=" # ", inline=False)
    test_e.add_field(name="!admincmd", value="Displays a list of all the admin commands", inline=False)
    test_e.add_field(name="!D", value="Prefix for drone controls")

    await author.send(embed=test_e) #Sends the list of controls via the users Direct Message
    await ctx.send("Check You DM ") #Sends on message on the server telling them to check their Direct messages

################### Admin Help
@client.command()
async def admincmd(ctx):
    author = ctx.message.author

    test_e = discord.Embed(
        colour=discord.Colour.orange()
    )
    test_e.set_author(name="Admin Commands")
    test_e.add_field(name="!say", value="Repeats everything after say and deletes users message", inline=False)
    test_e.add_field(name="!kick @user", value="Kicks mentiond user", inline=False)
    test_e.add_field(name="!ban @user", value="Bans mentiond user", inline=False)
    test_e.add_field(name="!unban @user", value="Unbans mentiond user", inline=False)
    test_e.add_field(name="!D", value="Prefix for drone controls")

    await author.send(embed=test_e) #Sends the list of controls via the users Direct Message
    await ctx.send("Check You DM ") #Sends on message on the server telling them to check their Direct messages


############################################ Admin Commands

################### Say
@client.command()
@commands.has_permissions(administrator=True)
async def say(ctx, *, msg):
    await ctx.message.delete()
    await ctx.send("{}" .format(msg))

################### Clear
@client.command()
@commands.has_permissions(administrator=True)
async def clear(ctx, amount=5):
    await ctx.channel.purge(limit=amount + 1)


################### Kick
@client.command()
@commands.has_permissions(administrator=True)
async def kick(ctx, member : discord.Member,*, reason=None):
    await member.kick(reason=reason)

################### Ban
@client.command()
@commands.has_permissions(administrator=True)
async def ban(ctx, member : discord.Member,*, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")
    
################### Unban
@client.command()
@commands.has_permissions(administrator=True)
async def unban(ctx, *,member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator =member.split('#')
    
    for ban_entry in banned_users:
        user = ban_entry.user
        
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {member.mention}")
            return

############################################ Audio

################### Join
@client.command()
async def join(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()

    await voice.disconnect()

    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()
        print(f"The bot has connected to {channel}\n")

    await ctx.send(f"Joined {channel}")

        
################### Leave
@client.command()
async def leave(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(client.voice_clients, guild=ctx.guild)

    if voice and voice.is_connected():
        await voice.disconnect()
        print(f"The bot has left {channel}")
        await ctx.send(f"Left {channel}")
    else:
        print("Bot was told to leave voice channel, but was not in one")
        await ctx.send("Don't think I am in a voice channel")
        
################### Play

@client.command()
async def play(ctx, *,url: str):
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        await ctx.send("#")
        return
    await ctx.send("#")
    
    
    
    voice = get(client.voice_clients, guild=ctx.guild)
    
    ydl_opts = {
        'default_search': 'ytsearch',
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
            
        }],
    }
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        #r = ydl.extract_info(url ,download=False)
        #r = ydl.extract_info(f"ytsearch:'{url}'", download=False)
        ydl.download([url])
        
        #print(str(url))
        #title = r["title"]
        #print(title)
        
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'song.mp3')
    voice.play(discord.FFmpegPCMAudio("song.mp3"))
    voice.volume = 100
    voice.is_playing()
    await ctx.send(f"#")

############################################ Bot Token
#DO NOT SHARE!
client.run('NzQwNDYyMzc4NDMyMzMxODE4.XypXVA.8EhIXi8louDekQenSMGnzbZ3dxw')

#Stops the program instantly closing when its run outside of the IDLE / Shell
input("Press enter to close program")
