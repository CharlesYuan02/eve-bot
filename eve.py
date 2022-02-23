import asyncio
from distutils import command
from bs4 import BeautifulSoup
import datetime
import nextcord
from nextcord.ext import commands
import os
import pytz
import random
from requests_html import HTMLSession
import time
import urllib.request


class Eve():
    def __init__(self):
        self.client = commands.Bot(command_prefix="eve ", help_command=None)
        self.praxis_lock = True
        self.praxis = False
        self.praxis_time = None


    def main(self):
        @self.client.event  # Cuz client holds instance of Bot
        async def on_ready():  # When the bot has everything it needs and is ready
            await self.client.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.playing, name="with her sister Lilith"))
            print("Eve, online and ready!")


        @self.client.command()
        async def help(ctx):
            await ctx.send("To see a full list of my commands and how to use them, please refer to my personal webpage.")
            await ctx.send("https://charles-yuan.netlify.app/eve.html")
            await ctx.send("```General/Admin Commands: \n\thelp - Displays this message \n\tclear - Clears a specified number of preceding lines \
                \n\tkick - Kicks a specified user \n\tban - Bans a specified user \n\tunban - Unbans a specified user \n\tload - Loads a specified cog \
                \n\tunload - Unloads a specified cog \n\tpoke - Sends a dm to a specified user with your user signature \
                \n\tgive_flowers - Sends flowers to a specified user \n\tpm - Sends a private message to a specified user \
                \n\tapm - Sends an anonymous private message to a specified user \n\thyperactive - Unleashes Eve's hyperactive skill: Odin Spear \
                \nCog Commands: \n\tq - Ask Eve a question; chatbot feature \n\t8ball - Ask Eve a random yes/no question, and she will reply from a list of responses \
                \n\tyoutube - Eve will return the first video she finds on Youtube given a query \n\tneko - Returns a picture of a neko \
                \n\twiki - Returns the first 3 sentences of the Wikipedia entry given a query \n\thug - Sends a gif of a hug to a specified user \
                \n\tkill - Sends a gruesome gif of a death to a specified user \n\tshit_on - Eve will insult the specified user \
                \n\tdefine - Returns the definition(s) of a word if found \n\tsynonym - Returns the synonym(s) of a word if found \
                \n\tantonym - Returns the antonym(s) of a word if found \
                \nSkynet Commands: \n\tpasscode - 'Sarah Connor' \n\tlock - Forces the passcode to be re-entered. Can only be used by my master \
                \n\tadmin_lock - Completely locks down Skynet commands. Can only be unlocked by my master \n\tskynet_list - Displays a list of Skynet commands \
                \n\tlist_cities - Returns a list of all the cities available for nuking \n\tskynet - Nukes a specified city(s) from the list \
                \n\tskynet_all - Nukes all the cities on the list \n\tskynet_purge - Continuously nukes all the cities on the list until there are no survivors```")


        @self.client.command()
        async def load(ctx, extension):  # The extension is the cog you wish to load
            self.client.load_extension(f"cogs.{extension}")
            print("Cog has been successfully loaded.")
            if extension == "nuke":
                await ctx.send("Nuke loaded.")


        @self.client.command()
        async def unload(ctx, extension):
            self.client.unload_extension(f"cogs.{extension}")
            print("Cog has been successfully unloaded.")


        @self.client.event
        async def on_member_join(member):
            print(f"{member} has joined the server.")


        @self.client.event
        async def on_member_remove(member):
            print(f"{member} has left the server.")


        @self.client.command()
        async def kick(ctx, member: nextcord.Member, *, reason=None):
            await member.kick(reason=reason)


        @self.client.command()
        async def ban(ctx, member: nextcord.Member, *, reason=None):
            await member.ban(reason=reason)
            await ctx.send(f"Banned {member.mention}")
        

        @self.client.command()
        # Can't do nextcord.Member, because it can't convert a string to a member object
        async def unban(ctx, *, member):
            banned_users = await ctx.guild.bans()
            member_name, member_discriminator = member.split("#")  # Splits account name at #

            for ban_entry in banned_users:
                user = ban_entry.user

                if (user.name, user.discriminator) == (member_name, member_discriminator):
                    await ctx.guild.unban(user)
                    await ctx.send(f"Unbanned {user.mention}.")
                    return


        @self.client.event
        async def on_message(message):
            message_content = message.content.lower()
            message_content = message_content.split()

            if message.content == "test":
                msg = "Test successful."
                await message.channel.send(msg)

            # Unloads the nuke cog so unwitting admins don't see it 
            if "eve help" in message.content:
                try:
                    self.client.unload_extension("cogs.nuke")
                except:
                    pass
            
            await self.client.process_commands(message) # The magic command
        

        @self.client.command()
        async def test(ctx):
            await ctx.send("Test successful.")


        @self.client.command()
        async def poke(ctx, member: nextcord.Member = None):
            if member is not None:
                channel = member.dm_channel
                if channel is None:  # If user has never talked to Eve
                    channel = await member.create_dm()
                await channel.send(f"{ctx.author.name} poked you!")
            else:
                await ctx.send("Please use @mention to poke someone")

        
        # Private message
        @self.client.command()
        async def pm(ctx, member: nextcord.Member = None, *, message):
            if member is not None:
                channel = member.dm_channel
                if channel is None:  # If user has never talked to Eve
                    channel = await member.create_dm()
                await channel.send(f'{message}\n-{ctx.author.name}')
            else:
                await ctx.send("Please use @mention to message someone")


        # Anonymous private message
        @self.client.command()
        async def apm(ctx, member: nextcord.Member = None, *, message):
            if member is not None:
                channel = member.dm_channel
                if channel is None:
                    channel = await member.create_dm()
                await channel.send(f'{message}')
            else:
                await ctx.send("Please use @mention to message someone")


        @self.client.command(aliases=["delete", "del", "remove"])
        async def clear(ctx, amount=10):  # Clears a specified number of lines
            await ctx.channel.purge(limit=amount)


        # Gives flowers
        @self.client.command(aliases=["give_flower", "give_rose", "give_roses", "send_flower", "send_flowers", "send_roses", "send_rose"])
        async def give_flowers(ctx, member):
            if str(ctx.author) == "Chubbyman#3362":
                await ctx.send(f"{member}, here is a :rose:, courtesy of your beloved Claire Clayton.")
            else:
                await ctx.send(f"{member}, here is a :rose:, courtesy of your beloved {ctx.author}.")


        # Unleashes Hyperactive skill
        @self.client.command(aliases=["odin_spear", "hyperactive_skill"])
        async def hyperactive(ctx):
            await ctx.send("https://media.giphy.com/media/fFmgzgndHLvfovfK9B/giphy.gif")
            time.sleep(3)
            await ctx.send("https://media.giphy.com/media/bk0pqOHhjfVGphL6Y1/giphy.gif")

        
        @self.client.command(aliases=["howeeb"])
        async def howweeb(ctx):
            await ctx.send(f"According to my calculations, you are {round(random.random() * 100, 1)}% weeb.")


        # Every hour, Eve will send the message "Fuck Praxis"
        @self.client.command()
        async def fuck_praxis(ctx):
            EST = pytz.timezone("US/Eastern")

            if not self.praxis_lock:
                if not self.praxis:
                    self.praxis = True
                    self.praxis_time = datetime.datetime.now(EST).strftime("%H:%M:%S")
                    await ctx.send(f"Praxis bullying has commenced at {self.praxis_time} EST.")
                elif self.praxis:
                    self.praxis = False
                    self.praxis_time = datetime.datetime.now(EST).strftime("%H:%M:%S")
                    await ctx.send(f"Praxis bullying has been stopped at {self.praxis_time} EST.")

                while self.praxis:
                    await ctx.send("Fuck Praxis.")
                    # Asyncio is useful because it allows other tasks to be run while .sleep() is active
                    await asyncio.sleep(3600)
            else:
                await ctx.send("Apologies, Praxis bullying is locked.")
                return


        @self.client.command(aliases=["praxis_lock", "unlock_praxis", "praxis_unlock"])
        async def lock_praxis(ctx):
            if str(ctx.author) == "Chubbyman#3362" and self.praxis_lock:
                self.praxis_lock = False
                await ctx.send("Praxis bullying is now unlocked.")
                return
            elif str(ctx.author) == "Chubbyman#3362" and not self.praxis_lock:
                self.praxis_lock = True
                await ctx.send("Praxis bullying is now locked.")
                return
            else:
                await ctx.send("Apologies, you cannot use this command.")

        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                # Cuts cog_example.py to cog_example
                self.client.load_extension(f"cogs.{filename[:-3]}")
        
        # Yes, order matters; you have to run this last
        TOKEN = os.environ["TOKEN"]
        self.client.run(TOKEN)


if __name__ == "__main__":
    eve = Eve()
    eve.main()
