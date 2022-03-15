import nextcord
from nextcord.ext import commands


class Nuke(commands.Cog):
    """
    I'm sure this won't backfire
    """

    def __init__(self, client): 
        self.client = client
        self.nuke = False

    @commands.command(usage="<passcode>", aliases=[])
    @commands.is_owner()
    async def nuke(self, ctx, *, passcode):
        """
        Nuke the server.
        """
        passcode = passcode.lower()
        if "genocidal" in passcode and "organ" in passcode:
            self.nuke = True
        elif "lucia" in passcode and "sukrova" in passcode:
            self.nuke = False
        else:
            await ctx.send("Incorrect passcode.")

        while self.nuke:
            await ctx.send("Death to @everyone")


def setup(client):
    client.add_cog(Nuke(client))
