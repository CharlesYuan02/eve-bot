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
            wiki_embed = nextcord.Embed(
                title = "Wikipedia Query",
                description = f"Query: {repr(keywords)}",
                colour = 0x0adbfc
            )
            wiki_embed.set_thumbnail(url="https://media.discordapp.net/attachments/952037974420385793/952038039457267712/Eve_Code_Ultimate_2.png")
            wiki_embed.set_footer(text="Github: https://github.com/Chubbyman2/eve-bot")
            wiki_embed.add_field(name="Here is what I found:", value=response)
            await ctx.send(embed=wiki_embed)
        except:
            await ctx.send(f"Sorry, I couldn't find anything for {keywords}.")


def setup(client):
    client.add_cog(Wikipedia(client))
