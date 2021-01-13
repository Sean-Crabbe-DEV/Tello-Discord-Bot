######################################## Tello ATC Discord Bot
#################### Written using python 3.8
####################
#################### Any server this is added to must have the role CurrentBotFlyers in to enable users to be able to fly the drone

#################### Tello Bot Join Links
## Use these links to add the bot to a discord server

## Main - https://discord.com/api/oauth2/authorize?client_id=740462378432331818&permissions=8&scope=bot

## Test - https://discord.com/api/oauth2/authorize?client_id=777861742528167946&permissions=8&scope=bot


#################### Installing Discord.py
# Windows
# py -3 -m pip install -U discord.py[voice]
# Linux/macOS
# python3 -m pip install -U "discord.py[voice]"


#################### Installing asyncio
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
import datetime
import platform
import threading
from discord import User
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import Bot, Greedy


############################################ Tello

################## Creats socket & Defines the local and tello ip addersses
host = ''
port = 9000
local_address = (host, port) # This is the address of the device running the code
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM) # Creates a socket that is used for the tello to drone two way communication
tello_address = ('192.168.10.1', 8889)  # this is the address of the tello & is where the drone commands are sent to
sock.bind(local_address)

################## Receive Drone Reply
def recv():
    count = 0
    while True:
        try:
            data, server = sock.recvfrom(1518) # Tells the code where to look for the drones reply
            # print(data.decode(encoding="utf-8"))
            droneData = data.decode(encoding="utf-8") # Decodes the data from utf-8 to text that can be understood by a human
            print(droneData) # Prints the decoded drone data in the python shell
        except Exception:
            print('\nExit . . .\n')
            break


recvThread = threading.Thread(target=recv)
recvThread.start()

############################################ Discord Bot

client = discord.Client()
client = commands.Bot(command_prefix='!')  # Defines Prefix For Bot To Respond To
client.remove_command('help')


############################################ Events

################### On Ready

@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('Navigateing The Skys')) # Sets the bots status on discord to
    print('Bot is online!')


################### Drone Controls Help

@client.command()
async def controls(ctx):
    author = ctx.message.author
    controls_e = discord.Embed(
        colour=discord.Colour.orange()

    )
    controls_e.set_author(name="Tello Controls")
    controls_e.add_field(name="!D command", value="Puts the tello into SDK mode", inline=False)
    controls.add_field(name="!D takeoff", value="Drone auto takesoff", inline=False)
    controls_e.add_field(name="!D land", value="Drone auto lands", inline=False)
    controls_e.add_field(name="!D emergency", value="Stops all motors", inline=False)
    controls_e.add_field(name="!D up x", value="Moves drone up by x cm", inline=False)
    controls_e.add_field(name="!D down x", value="Moves drone down by x cm", inline=False)
    controls_e.add_field(name="!D forward x", value="Moves drone forward by x cm", inline=False)
    controls_e.add_field(name="!D back x", value="Moves drone back by x cm", inline=False)
    controls_e.add_field(name="!D cw x", value="Rotates drone clockwise by x degrees", inline=False)
    controls_e.add_field(name="!D ccw x", value="Rotates drone counter clockwise by x degrees", inline=False)
    controls_e.add_field(name="!D flip x",
                         value="Flips drone in x direction. l (left), r (right), f (forward) and b (back)",
                         inline=False)
    controls_e.add_field(name="!D speed x", value="Sets speed to x cm/s", inline=False)
    controls_e.add_field(name="!D speed?", value="gets current speed (cm/s)", inline=False)
    controls_e.add_field(name="!D battery?", value="get current battery percentage", inline=False)
    controls_e.add_field(name="!D time?", value="get current fly time (s)", inline=False)
    controls_e.add_field(name="!D height?", value="get height (cm)", inline=False)
    controls_e.add_field(name="Tello SDK", value="https://bit.ly/2Zs5Pf4")

    await author.send(embed=controls_e)  # Sends the list of controls via the users Direct Message
    await ctx.send("Check You DM ")  # Sends on message on the server telling them to check their Direct messages

    time.sleep(20)

    await ctx.channel.purge(limit=2)


############################################ Commands - Tello Controls


################### Send Command To Drone
@client.command()
@commands.has_role(
    'CurrentBotFlyers')  # Tells the bot only people with the 'CurrentBotFlyers' role can use this command
async def D(ctx, *, msg):
    await ctx.send("Sending Command \"{}\" To The Tello".format(msg))
    print("Message Received From User")
    print("Sending Command \"{}\" To The Tello".format(msg))
    msg = msg.encode(encoding="utf-8")  # Encodes the message to utf-8 so it can be understood by the drone
    sent = sock.sendto(msg, tello_address)  # Sends the command to the drone using socket


############################################ Bot Token
################### Only Use one token at a time
################### DO NOT SHARE!

client.run(' ')  # Main Token (Tello ATC Bot)

# client.run(' ') # Test Token (Tello ATC Test Bot Token)

# Stops the program instantly closing when its run outside of the IDLE / Shell
input("Press enter to close program")

