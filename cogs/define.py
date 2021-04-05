import discord
from discord.ext import commands
from PyDictionary import PyDictionary  # install Pydictionary
dictionary = PyDictionary()


class Dictionary(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["definition"])
    async def define(self, ctx, *, word):
        if dictionary.meaning(word) == None:
            await ctx.send(f"Apologies, I could not find the definition for {word}.")
            return
        await ctx.send("One second...")
        nouns = []
        verbs = []
        adjectives = []
        adverbs = []

        for key in dictionary.meaning(word):
            if key == "Noun":
                for definition in dictionary.meaning(word)[key]:
                    nouns.append(definition)
            elif key == "Verb":
                for definition in dictionary.meaning(word)[key]:
                    verbs.append(definition)
            elif key == "Adjective":
                for definition in dictionary.meaning(word)[key]:
                    adjectives.append(definition)
            elif key == "Adverb":
                for definition in dictionary.meaning(word)[key]:
                    adverbs.append(definition)

        if len(nouns) != 0:
            for noun in nouns:
                temp = noun
                for letter in noun:
                    if letter == "(":
                        noun += ")"
                        nouns[nouns.index(temp)] = noun

            await ctx.send("```Nouns: \n-" + "\n-".join(nouns) + "```")

        if len(verbs) != 0:
            for verb in verbs:
                temp = verb
                for letter in verb:
                    if letter == "(":
                        verb += ")"
                        verbs[verbs.index(temp)] = verb
            await ctx.send("```Verbs: \n-" + "\n-".join(verbs) + "```")

        if len(adjectives) != 0:
            for adjective in adjectives:
                temp = adjective
                for letter in adjective:
                    if letter == "(":
                        adjective += ")"
                        adjectives[adjectives.index(temp)] = adjective
            await ctx.send("```Adjectives: \n-" + "\n-".join(adjectives) + "```")

        if len(adverbs) != 0:
            for adverb in adverbs:
                temp = adverb
                for letter in adverb:
                    if letter == "(":
                        adverb += ")"
                        adverbs[adverbs.index(temp)] = adverb
            await ctx.send("```Adverbs: \n-" + "\n-".join(adverbs) + "```")

    @commands.command()
    async def synonym(self, ctx, *, word):
        if dictionary.synonym(word) == None:
            await ctx.send(f"Apologies, I could not find any synonyms for {word}.")
            return
        await ctx.send("One second...")
        synonyms = []
        for synonym in dictionary.synonym(word):
            synonyms.append(synonym)
        await ctx.send("```Synonyms: \n-" + "\n-".join(synonyms) + "```")

    @commands.command(aliases=["opposite"])
    async def antonym(self, ctx, *, word):
        if dictionary.antonym(word) == None:
            await ctx.send(f"Apologies, I could not find any antonyms for {word}.")
            return
        await ctx.send("One second...")
        antonyms = []
        for antonym in dictionary.antonym(word):
            antonyms.append(antonym)
        await ctx.send("```Antonyms: \n-" + "\n-".join(antonyms) + "```")


def setup(client):
    client.add_cog(Dictionary(client))
