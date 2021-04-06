import discord
from discord.ext import commands
from bs4 import BeautifulSoup
import urllib.request
from PyDictionary import PyDictionary  # install Pydictionary
dictionary = PyDictionary()


def get_definition(words):
    word = "-".join(words)
    url = "https://www.dictionary.com/browse/" + word
    try:
        htmlfile = urllib.request.urlopen(url)
        soup = BeautifulSoup(htmlfile, "lxml")
        definition = soup.find(class_="one-click-content css-ibc84h e1q3nk1v1")
        return definition, soup
    except:
        return None, None


def get_synonyms(words):
    word = "-".join(words)
    url = "https://www.dictionary.com/browse/" + word
    try:
        htmlfile = urllib.request.urlopen(url)
        soup = BeautifulSoup(htmlfile, "lxml")
        synonyms = soup.find(class_="css-1kva0eo e15p0a5t1")
        return synonyms, soup
    except:
        return None, None


class Dictionary(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=["definition"])
    async def define(self, ctx, *, word):

        # First check how many words there are
        words = word.split()
        if len(words) == 1 and dictionary.meaning(words[0]) != None:
            word = words[0]
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

        # If it's more than one word
        else:
            await ctx.send("One second...")
            if get_definition(words)[0] == None:
                try:
                    word = get_definition(words)[1].find(class_="kw")
                    word = word.get_text()
                    words = word.split(" ")

                    if get_definition(words)[0] != None:
                        definition = get_definition(words)[0]
                        definition = definition.get_text()
                        await ctx.send("```Definition: \n" + str(definition) + "```")
                        return

                    else:
                        await ctx.send(f"Apologies, I could not find the definition for {' '.join(words)}.")
                        return

                except AttributeError:
                    await ctx.send(f"Apologies, I could not find the definition for {' '.join(words)}.")
                    return

            else:
                definition = get_definition(words)[0]
                definition = definition.get_text()
                await ctx.send("```Definition: \n" + str(definition) + "```")

    @commands.command()
    async def synonym(self, ctx, *, word):
        words = word.split()
        if len(words) == 1 and dictionary.synonym(words[0]) != None:
            word = words[0]
            await ctx.send("One second...")
            synonyms = []
            for synonym in dictionary.synonym(word):
                synonyms.append(synonym)
            await ctx.send("```Synonyms: \n-" + "\n-".join(synonyms) + "```")

        # If it's more than one word
        else:
            await ctx.send("One second...")
            if get_definition(words)[0] == None:
                try:
                    word = get_definition(words)[1].find(class_="kw")
                    word = word.get_text()
                    words = word.split(" ")

                    if get_synonyms(words)[0] != None:
                        synonyms = get_synonyms(words)[0]
                        synonyms = synonyms.get_text()
                        await ctx.send("```Synonyms: \n" + str(synonyms) + "```")
                        return

                    else:
                        await ctx.send(f"Apologies, I could not find any synonyms for {' '.join(words)}.")
                        return

                except AttributeError:
                    await ctx.send(f"Apologies, I could not find any synonyms for {' '.join(words)}.")
                    return

            else:
                synonyms = get_synonyms(words)[0]
                synonyms = synonyms.get_text()
                await ctx.send("```Synonyms: \n" + str(synonyms) + "```")

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
