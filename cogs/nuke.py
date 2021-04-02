import discord
from discord.ext import commands

nuke = False
abort = False


class Nuke(commands.Cog):

    def __init__(self, client):  # References whatever is passed through the client from discord
        self.client = client

    @commands.command()
    async def nuke(self, ctx, *, passcode):
        passcode = passcode.lower()
        if str(ctx.author) == "Chubbyman#3362":
            if "genocidal" in passcode and "organ" in passcode:
                global nuke
                nuke = True

            elif "lucia" in passcode and "sukrova" in passcode:
                global abort
                abort = True

            else:
                await ctx.send("Incorrect passcode.")

        else:
            await ctx.send("Sorry, you are not permitted to use this command.")

        while nuke == True and abort != True:
            await ctx.send("Death to @everyone")


def setup(client):
    client.add_cog(Nuke(client))
