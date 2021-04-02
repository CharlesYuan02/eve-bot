import discord
from discord.ext import commands


class Media(commands.Cog):

    def __init__(self, client):  # References whatever is passed through the client from discord
        self.client = client

    @commands.command(aliases=["video"])
    async def youtube(self, ctx, *, search):
        search_keyword = search.replace(" ", "_")
        html = urllib.request.urlopen(
            "https://www.youtube.com/results?search_query=" + search_keyword)
        video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
        await ctx.send("https://www.youtube.com/watch?v=" + video_ids[0])

    @commands.command(aliases=["photo", "picture", "show"])
    async def image(self, ctx, *, search):
        search = search.replace(" ", "_")
        html = urllib.request.urlopen(
            f"https://www.google.com/search?q={search}&source=lnms&tbm=isch")
        data = {'content': 'images src', 'src': re.findall('src="([^"]+)"', a)}
        await ctx.send(data['src'][0])


def setup(client):
    client.add_cog(Media(client))
