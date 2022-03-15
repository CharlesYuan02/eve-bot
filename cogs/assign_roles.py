import nextcord
from nextcord.ext import commands


class AssignRoles(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        reaction = payload.emoji
        channel = await self.client.fetch_channel(payload.channel_id)
        guild = await self.client.fetch_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)
        announcements_channel = self.client.get_channel(944266932956315708)
        testing_channel = self.client.get_channel(944272641878028299)

        if channel != announcements_channel and channel != testing_channel:
            return

        if str(reaction) == "<:Lacia:944271608711872583>":
            mi_role = nextcord.utils.get(guild.roles, name="MI Major")
            await user.add_roles(mi_role)
        elif str(reaction) == "<:Vivy:944271916426985532>":
            ai_role = nextcord.utils.get(guild.roles, name="AI Minor")
            await user.add_roles(ai_role)
        elif str(reaction) == "<:Miku:944272417180774420>":
            guest_role = nextcord.utils.get(guild.roles, name="Guest")
            await user.add_roles(guest_role)
        elif str(reaction) == "<:Eve:944297441723830314>":
            tester_role = nextcord.utils.get(guild.roles, name="Beta Tester")
            await user.add_roles(tester_role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        reaction = payload.emoji
        channel = await self.client.fetch_channel(payload.channel_id)
        guild = await self.client.fetch_guild(payload.guild_id)
        user = await guild.fetch_member(payload.user_id)
        announcements_channel = self.client.get_channel(944266932956315708)
        testing_channel = self.client.get_channel(944272641878028299)

        if channel != announcements_channel and channel != testing_channel:
            return

        if str(reaction) == "<:Lacia:944271608711872583>":
            mi_role = nextcord.utils.get(guild.roles, name="MI Major")
            await user.remove_roles(mi_role)
        elif str(reaction) == "<:Vivy:944271916426985532>":
            ai_role = nextcord.utils.get(guild.roles, name="AI Minor")
            await user.remove_roles(ai_role)
        elif str(reaction) == "<:Miku:944272417180774420>":
            guest_role = nextcord.utils.get(guild.roles, name="Guest")
            await user.remove_roles(guest_role)
        elif str(reaction) == "<:Eve:944297441723830314>":
            tester_role = nextcord.utils.get(guild.roles, name="Beta Tester")
            await user.remove_roles(tester_role)

    @commands.command(usage="", aliases=["assign_role", "get_role", "get_roles"])
    async def assign_roles(self, ctx):
        """
        Send a message to assign roles with reactions.
        """
        if str(ctx.author) == "Chubbyman#3362":
            await ctx.channel.purge(limit=1)
            message = await ctx.send("Server Roles! Select one to gain access to the relevant channels." +
                                     "\n\nReact With:\n<:Lacia:944271608711872583> for <@&944256384235606027>" +
                                     "\n<:Vivy:944271916426985532> for <@&944257914162516019>" +
                                     "\n<:Miku:944272417180774420> for <@&944277387032543343>" +
                                     "\n<:Eve:944297441723830314> for <@&944297684133642352>")
            await message.add_reaction(emoji="<:Lacia:944271608711872583>")
            await message.add_reaction(emoji="<:Vivy:944271916426985532>")
            await message.add_reaction(emoji="<:Miku:944272417180774420>")
            await message.add_reaction(emoji="<:Eve:944297441723830314>")
        else:
            await ctx.send("Apologies, you do not have permission to use this command.")


def setup(client):
    client.add_cog(AssignRoles(client))
