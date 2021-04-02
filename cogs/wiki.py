import discord
from discord.ext import commands


class Wikipedia(commands.Cog):

    def __init__(self, client):  # References whatever is passed through the client from discord
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
