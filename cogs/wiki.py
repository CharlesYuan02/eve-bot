import nextcord
from nextcord.ext import commands
import wikipedia

class Wikipedia(commands.Cog):
    """
    A bot isn't complete without a wikipedia search command.
    """
    @staticmethod
    def purge_displaystyle(text, first_open_brace):
        depth = 1
        last_close_brace = first_open_brace + 1
        while depth:
            if text[last_close_brace] == "}":
                depth -= 1
            elif text[last_close_brace] == "{":
                depth += 1
            last_close_brace += 1
        return text[:first_open_brace] + text[last_close_brace:]

    def __init__(self, client): 
        self.client = client

    @commands.command(usage="<keywords", aliases=[])
    async def wiki(self, ctx, *, keywords):
        """
        Search wikipedia.
        """
        try:
            # Use repr to convert command object to string
            response = wikipedia.summary(repr(keywords), sentences=2)
            while response.find("{\\displaystyle") != -1:
                response = Wikipedia.purge_displaystyle(response, response.find("{\\displaystyle"))
            # remove extra spaces
            response = response.replace("\n", " ").replace("\r", " ").replace("\t", " ")
            while response.find("  ") != -1:
                response = response.replace("  ", " ")
            wiki_embed = nextcord.Embed(
                title = "Wikipedia Query",
                description = f"Query: {repr(keywords)}",
                colour = 0x0adbfc
            )
            wiki_embed.set_thumbnail(url="https://media.discordapp.net/attachments/952037974420385793/952038039457267712/Eve_Code_Ultimate_2.png")
            wiki_embed.set_footer(text="Github: https://github.com/Chubbyman2/eve-bot")
            wiki_embed.add_field(name="Here is what I found:", value="```" + response + "```")
            await ctx.send(embed=wiki_embed)
        except:
            await ctx.send(f"Sorry, I couldn't find anything for {keywords}.")


def setup(client):
    client.add_cog(Wikipedia(client))
