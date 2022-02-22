import nextcord
from nextcord.ext import commands
import wikipedia


class Wikipedia(commands.Cog):

    def __init__(self, client): 
        self.client = client

    @commands.command()
    async def wiki(self, ctx, *, keywords):
        try:
            # Use repr to convert command object to string
            response = wikipedia.summary(repr(keywords), sentences=2)
            await ctx.send("Here is what I found: \n" + response)
        except:
            await ctx.send(f"Sorry, I couldn't find anything for {keywords}.")


def setup(client):
    client.add_cog(Wikipedia(client))
