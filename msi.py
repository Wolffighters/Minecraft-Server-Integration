#import Packages
import random
from typing import AnyStr
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext.commands import has_permissions, MissingPermissions
from discord.ext.commands.core import check
from discord.utils import find
from datetime import datetime, timedelta
from discord import Interaction
from discord import Message
import asyncio
import os
import termcolor

import configparser

import subprocess
from subprocess import Popen, PIPE

config = configparser.ConfigParser()
config.read("config.ini")

#from rcon.source import rcon
from async_mcrcon import MinecraftClient

OwnerID = 434137979674689546
logChannel = 1175746088305700865
#You will have to manually change the rcon IP, Port and Password. You will also have to manually change the system path to start the server. All of this is to prevent attacks.

import json


#Client (The Bot)

intents = discord.Intents.all()
intents.message_content = True
prefix = "."
client = commands.Bot(command_prefix=prefix, intents=intents)

#AdminRole = discord.utils.find(lambda r: r.name == 'msiAdmin', Message.author.role)
ip = config.get("myvars","configset_ip")
port = config.get("myvars","configset_port")
mods = config.get("myvars","configset_mods")
running = config.get("otherVars","isrunning")

#ADMIN_ROLE = config.get("otherVars", 'DISCORD_ADMIN_ROLE')
ADMIN_ROLE = "msiAdmin"
if (port == ""):
    ipnport = (f"{ip}")
else:
    ipnport = (f"{ip}:{port}")

if (mods == ""):
    mods = ("There are no mods on this server.")
else:
    mods = mods

#Turning On/Off
@client.event
async def on_ready():
    wolfbot_channel = client.get_channel(logChannel)
    await wolfbot_channel.send('Hello!')
    game = discord.Game("Hello There")
    await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name='Hello There', url='https://www.youtube.com/watch?v=dQw4w9WgXcQ'))
    await client.tree.sync()
    print("Ready!")

@client.event
async def on_disconnect():
    wolfbot_channel = client.get_channel(logChannel)
    await wolfbot_channel.send('Goodbye!')



@client.command(aliases=['clear','Clear'])
async def _clear(ctx, amount=2):
        if (ctx.message.author.guild_permissions.administrator): #does work, cant use ctx in slash commands though
            await ctx.send(f"{amount -1} Messages has been removed!", delete_after=5)
            await ctx.channel.purge(limit=amount + 1)
        else:
            if (ctx.message.author.id == OwnerID):
                await ctx.send(f"{amount -1} Messages has been removed!", delete_after=5)
                await ctx.channel.purge(limit=amount + 1)
            else:
                await ctx.send("You are missing Administrator permission(s) to run this command.")


@client.command(aliases=['SpamPing','SP','sp','spam'])
async def spamping(ctx, user: discord.User, amount=2):
    if ADMIN_ROLE in [y.name.lower() for y in author.roles]: #dosent work
        print("|==========================================================|")
        print(f"{ctx.message.author.id} or {ctx.message.author} ran spamping {amount} times.")
        for _ in range(amount):
            await ctx.send(user.mention)
        message = f"You have been SpamPinged {user.mention} {amount + 1} times"
        await ctx.send(message)
    if (ctx.message.author.id == OwnerID):
        print("|==========================================================|")
        print(f"{ctx.message.author.id} or {ctx.message.author} ran spamping {amount} times.")
        for _ in range(amount):
            await ctx.send(user.mention)
        message = f"You have been SpamPinged {user.mention} {amount + 1} times"
        await ctx.send(message)
    else:
        await ctx.send("You are not allowed to run this command.")
        print("|==========================================================|")
        print(f"{ctx.message.author.id} or {ctx.message.author} ran spamping without correct permissions.")


@client.tree.command(name="help", description="Shows Help info and commands")
async def help(interaction: discord.Interaction):
    print("|==========================================================|")
    print(f"{interaction.user.id} or {interaction.user} ran /help")
    await interaction.response.send_message(f"```ansi\n[2;31m[2;37mMade by Wolffighters, formally known as Wolffighters#0383, find me at Wolffighters.dev![0m[2;31m\n\n[2;31mStart [0m- Starts the server\n[2;31mStop [0m- Stops the server if no players are online\n[2;31mForceStop [0m- Stops the server even if players are online, [2;33mowner/admins only[0m\n[2;31mSay [0m- Sends a message in chat via rcon, mentioning the user who sent it and [2;31mtheir [0mmessage\n[2;31mRcon_command [0m- Runs any command on the server. [2;33mOwner/admins only. [0m\n[2;31mList [0m- Gets currently online players\n[2;31mInfo [0m- Gets info about the server for users, includes mods they need and ip and port (if used) \n[2;31mHelp [0m- Shows this message.\n[2;32m-------------------------------------------[0m\n[2;33mPrefix is {prefix}[0m\n[2;31m{prefix}clear[0m [2;34m(amount)[0m - Deletes [2;34m(amount)[0m of messages. [2;33mOwner/admins only[0m\n[2;31m{prefix}spamping[0m [2;34m(user)[0m [2;34m(amount)[0m - Pings [2;34m(user)[0m [2;34m(amount)[0m of times. [2;33mOwner/admins only[0m\n[2;32m-------------------------------------------[0m\n[2;33mClear [2;32mand [0m[2;33mSpamPing[0m are likely to be [2;31mdeprecated[0m!\n[2;35mIf[0m the command [2;31mhangs [0mthe server is [2;35mnot on[0m!\n[2;35mIf[0m the bot is [2;31moffline[0m, the commands will [2;35malso hang[0m.\n```")

@client.tree.command(name="rcon_command", description="Runs a command on console")
async def rcon_command(interaction: discord.Interaction, name: str):
    if "msiAdmin" in interaction.user.roles: #dosent work, on the right track though
        async with MinecraftClient(ip, port, password) as mc:
            output = await mc.send(name)
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran rcon_command")
        print(output)
        await interaction.response.send_message(output)
    elif (interaction.user.id == OwnerID+1):
        async with MinecraftClient(ip, port, password) as mc:
            output = await mc.send(name)
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran rcon_command")
        print(output)
        await interaction.response.send_message(output)
    else:
        await interaction.response.send_message("Last time I checked, you didn't have permission to perform this command.")
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran rcon_command without correct permissions.")



@client.tree.command(name="list", description="Lists currently online players on the Minecraft server")
async def list(interaction: discord.Interaction):
    async with MinecraftClient(ip, port, password) as mc:
        output = await mc.send("/list")
    print("|==========================================================|")
    print(f"{interaction.user.id} or {interaction.user} ran /list")
    print(output)
    await interaction.response.send_message(output)

@client.tree.command(name="say", description="Sends a message using /say")
async def say(interaction: discord.Interaction, name: str):
    if (name.__contains__('@')):
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran /say")
        print(f"{interaction.user.id} or {interaction.user} said {name}")
        print(f"{name} contains @, which is not allowed. The command was stopped.")
        await interaction.response.send_message(f"Please do not use the symbol @ in your message")
    else:
        async with MinecraftClient(ip, port, password) as mc:
            output = await mc.send(f"/say {interaction.user} says: {name}")
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran /say")
        print(f"{interaction.user.id} or {interaction.user} said {name}")
        await interaction.response.send_message(f"Completed successfully. Message sent: {name}")

@client.tree.command(name="info", description="Gets server info")
async def info(interaction: discord.Interaction):
    print("|==========================================================|")
    print(f"{interaction.user.id} or {interaction.user} ran /info")
    await interaction.response.send_message(f"```ansi\nIP: {ipnport} \nMODS: {mods}\n```")

@client.tree.command(name="start", description="Starts the server")
async def start(interaction: discord.Interaction):
    if (running == "True"):
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran /start")
        print(f"Server is already online!")
        await interaction.response.send_message(f"```ansi\nServer is already online!\n```")
    else:
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran /start")
        print(f"Server is offline!")
        os.system('wt.exe -d "C:\\Users\\User\\Documents\\Servers\\Origins 1.20.2" -p "command prompt" --title "server" cmd /k start.bat')
        config.set("otherVars","isrunning", "True")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print(f"Starting the server now...")
        await interaction.response.send_message(f"```ansi\nServer starting now.\n```")

@client.tree.command(name="stop", description="Stops the server")
async def stop(interaction: discord.Interaction):
    async with MinecraftClient(ip, port, password) as mc:
        output = await mc.send("/list")

    if "There are 0" not in output:
        await interaction.response.send_message("```ansi\nThere are currently players online, you may not stop the server.\n```")
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran stop whilst players were still online.")
        return True

    async with MinecraftClient(ip, port, password) as mc:
        output = await mc.send("/stop")
    config.set("otherVars","isrunning", "False")
    with open('config.ini', 'w') as configfile:
        config.write(configfile)
    print("|==========================================================|")
    print(f"{interaction.user.id} or {interaction.user} ran stop")
    print(output)
    await interaction.response.send_message("```ansi\nstopping server now.\n```")

@client.tree.command(name="forcestop", description="Force stops the server")
async def forcestop(interaction: discord.Interaction):
    if ADMIN_ROLE in [y.name.lower() for y in author.roles]: #dosent work
        async with MinecraftClient(ip, port, password) as mc:
            output = await mc.send(stop)
        config.set("otherVars","isrunning", "False")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran forcestop")
        print(output)
        await interaction.response.send_message(output)
    if (interaction.user.id == OwnerID):
        async with MinecraftClient(ip, port, password) as mc:
            output = await mc.send(stop)
        config.set("otherVars","isrunning", "False")
        with open('config.ini', 'w') as configfile:
            config.write(configfile)
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran forcestop")
        print(output)
        await interaction.response.send_message(output)
    else:
        await interaction.response.send_message("```ansi\nLast time I checked, you didn't have permission to perform this command.\n```")
        print("|==========================================================|")
        print(f"{interaction.user.id} or {interaction.user} ran forcestop without correct permissions.")
client.run(token)