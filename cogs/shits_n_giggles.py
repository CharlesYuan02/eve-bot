import nextcord
from nextcord.ext import commands
import random


class Gifs(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(usage="<member>", aliases=["give_hug"])
    async def hug(self, ctx, *, member):
        """
        Give someone a hug ❤️
        """
        hug_library = ["https://i.pinimg.com/originals/db/31/46/db31461539daa3f046e41168d47efc67.gif",
                       "https://acegif.com/wp-content/uploads/anime-hug.gif",
                       "https://media3.giphy.com/media/PHZ7v9tfQu0o0/giphy.gif",
                       "https://i.imgur.com/nrdYNtL.gif",
                       "https://25.media.tumblr.com/b9de103a15264130db466e71040538c0/tumblr_mum0c9GbHl1sibpv8o1_500.gif",
                       "https://media0.giphy.com/media/lrr9rHuoJOE0w/source.gif",
                       "https://i.pinimg.com/originals/85/72/a1/8572a1d1ebaa45fae290e6760b59caac.gif"]
        await ctx.send(f"{member}, did you need a hug?")
        await ctx.send(f"{random.choice(hug_library)}")
        print(repr(member))

    @commands.command(usage="<member>", aliases=["murder", "stab", "mutilate", "crucify", "decapitate"])
    async def kill(self, ctx, *, member:nextcord.Member):
        """
        Kill your enemies.
        """
        kill_library = ["https://i.imgur.com/Xkyuz6f.gif",
                        "https://thumbs.gfycat.com/ConstantMeaslyAphid-size_restricted.gif",
                        "https://38.media.tumblr.com/tumblr_lwp9gvzM4n1qd4f2uo1_500.gif",
                        "https://i.gifer.com/8Lnq.gif",
                        "https://i.pinimg.com/originals/2b/40/18/2b40185d04e8e6b774f7612623a5ae30.gif"]
        if await self.bot.is_owner(member):
            await ctx.send("No.")
        else:
            await ctx.send(f"{member.mention}, prepare to die!")
            await ctx.send(f"{random.choice(kill_library)}")

    @commands.command(usage="<member>", aliases=["bully"])
    async def shit_on(self, ctx, *, member:nextcord.Member):
        """
        Screw that guy.
        """
        if await self.bot.is_owner(member):
            await ctx.send("No.")
        else:
            await ctx.send(f"Fuck you {member.mention}.")


def setup(client):
    client.add_cog(Gifs(client))
