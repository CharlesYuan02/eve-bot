import bs4
from bs4 import BeautifulSoup
import discord  # install discord, install -U discord.py (update!)
from discord.ext import commands
import docx  # install python-docx
import json
import os
import random
import re
import requests
from requests_html import HTMLSession
import time
import urllib.parse
import urllib.request
import wikipedia


TOKEN = os.environ["TOKEN"]
client = commands.Bot(command_prefix="eve ")  # Prefix can be anything
roast = False
mak = False


@client.command()
async def load(ctx, extension):  # The extension is the cog you wish to load
    client.load_extension(f"cogs.{extension}")
    print("Cog has been successfully loaded.")
    if extension == "nuke":
        await ctx.send("Nuke loaded.")


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f"cogs.{extension}")
    print("Cog has been successfully unloaded.")


@client.event  # Cuz client holds instance of Bot
async def on_ready():  # When the bot has everything it needs and is ready
    await client.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.playing, name="with her sister Lilith"))
    print("Eve, online and ready!.")


@client.event
async def on_member_join(member):  # All in documentation
    print(f"{member} has joined the server.")


@client.event
async def on_member_remove(member):
    print(f"{member} has left the server.")


@client.event
async def on_message(message):
    global roast
    message_content = message.content.lower()
    message_content = message_content.split()
    greetings_library = ["hello", "hey", "yo", "hi", "greetings"]
    sample_greetings = ["Hello there!", "Heyo!", "'Sup dude",
                        "What's cookin', good lookin'?", "Yo", "Hieeee!"]
    roast_John = ["u dumb", "bad", "u will die alone",
                  "no one likes u", "good luck graduating from engsci lol", "loser"]
    for greeting in greetings_library:
        if greeting in message_content and "eve" in message_content and len(message_content) == 2:
            msg = random.choice(sample_greetings)
            await message.channel.send(msg)
            break
    if message.content == "test":
        msg = "Test successful."
        await message.channel.send(msg)
    if str(message.author) == "mak13789#4418" and mak:
        await message.add_reaction("<:cringe:704351813570396202>")
    if (str(message.author) == "Euler's formula#0741" or str(message.author) == "mak13789#4418" or str(message.author) == "Amaterasu#1541") and roast:
        msg = random.choice(roast_John)
        await message.channel.send(msg)
    if "eve help" in message.content:
        try:
            client.unload_extension("cogs.nuke")
        except:
            pass
    if "roast" in message_content and ("mak" in message_content or "john" in message_content or "amaterasu" in message_content):
        # Remember that messages also include Eve's own!
        roast = True
        await message.channel.send("Understood")
    if "stop roast" in message.content and str(message.author) == "Chubbyman#3362":
        roast = False
        await message.channel.send("Yessir")
    if ("aint that right" in message.content or "amirite" in message.content or "right" in message.content or "arent you" in message.content) and "eve" in message.content and str(message.author) == "Chubbyman#3362":
        affirmations = ["Yup", "Yeah", "Mm hmm", "Yuppers", "Yes, sir"]
        await message.channel.send(random.choice(affirmations))
    else:
        pass
    await client.process_commands(message)  # The magic command


@ client.command()
async def kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)


@ client.command()
async def ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.send(f"Banned {member.mention}")


@ client.command()
# Can't do discord.Member, because it can't convert a string to a member object
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split(
        "#")  # Splits account name at #

    for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"Unbanned {user.mention}.")
            return


@ client.command()
async def poke(ctx, member: discord.Member = None):
    if member is not None:
        channel = member.dm_channel
        if channel is None:  # If user has never talked to Eve
            channel = await member.create_dm()
        await channel.send(f"{ctx.author.name} poked you!")
    else:
        await ctx.send("Please use @mention to poke someone")


# Private message
@ client.command()
async def pm(ctx, member: discord.Member = None, *, message):
    if member is not None:
        channel = member.dm_channel
        if channel is None:  # If user has never talked to Eve
            channel = await member.create_dm()
        await channel.send(f'{message}\n-{ctx.author.name}')
    else:
        await ctx.send("Please use @mention to message someone")


# Anonymous private message
@ client.command()
async def apm(ctx, member: discord.Member = None, *, message):
    if member is not None:
        channel = member.dm_channel
        if channel is None:
            channel = await member.create_dm()
        await channel.send(f'{message}')
    else:
        await ctx.send("Please use @mention to message someone")


@ client.command()
async def clear(ctx, amount=10):  # Clears a specified number of lines
    await ctx.channel.purge(limit=amount)


# Gives flowers
@ client.command(aliases=["give_flower", "give_rose", "give_roses", "send_flower", "send_flowers", "send_roses", "send_rose"])
async def give_flowers(ctx, member):
    if str(ctx.author) == "Chubbyman#3362":
        await ctx.send(f"{member}, here is a :rose:, courtesy of your beloved Claire Clayton.")
    else:
        await ctx.send(f"{member}, here is a :rose:, courtesy of your beloved {ctx.author}.")


# Unleashes Hyperactive skill
@ client.command(aliases=["odin_spear", "hyperactive_skill"])
async def hyperactive(ctx):
    await ctx.send("https://media.giphy.com/media/fFmgzgndHLvfovfK9B/giphy.gif")
    time.sleep(3)
    await ctx.send("https://media.giphy.com/media/bk0pqOHhjfVGphL6Y1/giphy.gif")


@ client.command()
async def mak(ctx):
    await ctx.send("<:cringe:704351813570396202>")


@ client.command()
async def mak_toggle(ctx):
    global mak
    if (str(ctx.author) == "Chubbyman#3362" or str(ctx.author) == "Lizard#5779") and not mak:
        mak = True
        await ctx.send("Initiating mak bullying mode.")
    elif (str(ctx.author) == "Chubbyman#3362" or str(ctx.author) == "Lizard#5779") and mak:
        mak = False
        await ctx.send("Deactivating mak bullying mode.")


if __name__ == "__main__":
    for filename in os.listdir("cogs"):
        if filename.endswith(".py"):
            # Cuts cog_example.py to cog_example
            client.load_extension(f"cogs.{filename[:-3]}")

    # Put the token here
    client.run(TOKEN)
