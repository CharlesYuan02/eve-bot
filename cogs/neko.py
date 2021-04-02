import discord
from discord.ext import commands


# As suggested by Amaterasu#1541
class Neko(commands.Cog):

    def __init__(self, client):  # References whatever is passed through the client from discord
        self.client = client

    @commands.command(aliases=["nyaa", "meow", "mew"])
    async def neko(self, ctx):
        list_of_nekos = ["https://ih1.redbubble.net/image.608339956.2125/flat,750x,075,f-pad,750x1000,f8f8f8.jpg",
                         "https://i.imgur.com/9FHKGun.jpg",
                         "https://img-9gag-fun.9cache.com/photo/a24mbjw_460s.jpg",
                         "https://i.pinimg.com/736x/ba/f8/8f/baf88f7dd2183726b3c70dd8f3879273.jpg",
                         "https://i.pinimg.com/originals/70/30/a8/7030a89a403da9480243366b9b07d816.jpg",
                         "https://i.imgur.com/TNq7L9o.jpg",
                         "https://i.redd.it/zorblfl150e11.jpg",
                         "https://fsb.zobj.net/crop.php?r=t80iYxYSeqBl5720rOztlpYa6QBTO_X64Q_UicCAep8vM8ubcIuk6J7DxptWZB6uN2VBW1YOXML1kSO6csNx7H4wv1Roz0VEaXDnsfTZIkLZDZ-5iVuFVMZHVpui8n5e7oUL3lcAZ-K2DlQv",
                         "https://media1.tenor.com/images/7bd33e9dc290d7feadfae4a3353805c1/tenor.gif?itemid=13436976",
                         "https://i.pinimg.com/originals/f5/91/1b/f5911b6b69ca9a114372a5cf890807a6.gif",
                         "https://media.tenor.com/images/ed1c69aa20cd18d6efb92e9a7e8a1404/tenor.gif",
                         "https://media1.tenor.com/images/a66d5af4be501deb2ac4ab513a34af17/tenor.gif?itemid=16054619",
                         "https://pa1.narvii.com/6260/c870d95b4429b1e27da5e5bbc926bf1ebf0f7c17_hq.gif"]

        await ctx.send(random.choice(list_of_nekos))


def setup(client):
    client.add_cog(Neko(client))
