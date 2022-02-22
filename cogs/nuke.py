import nextcord
from nextcord.ext import commands


class Nuke(commands.Cog):

    def __init__(self, client): 
        self.client = client
        self.nuke = False

    @commands.command()
    async def nuke(self, ctx, *, passcode):
        passcode = passcode.lower()
        if str(ctx.author) == "Chubbyman#3362":
            if "genocidal" in passcode and "organ" in passcode:
                self.nuke = True
            elif "lucia" in passcode and "sukrova" in passcode:
                self.nuke = False
            else:
                await ctx.send("Incorrect passcode.")

        else:
            await ctx.send("Sorry, you are not permitted to use this command.")

        while self.nuke:
            await ctx.send("Death to @everyone")


def setup(client):
    client.add_cog(Nuke(client))
