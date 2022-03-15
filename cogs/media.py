import nextcord
from nextcord.ext import commands
import urllib.parse
import urllib.request
import re


class Media(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(usage="<search>", aliases=["video"])
    async def youtube(self, ctx, *, search):
        """
        Search for a video on youtube.com.
        """
        search_keyword = search.replace(" ", "_")
        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])


def setup(client):
    client.add_cog(Media(client))
