import nextcord
from nextcord.ext import commands
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
        definition = soup.find(class_="one-click-content css-nnyc96 e1q3nk1v1")
        return definition, soup
    except:
        return None, None


class Dictionary(commands.Cog):
    """
    Dictionary definitions
    """

    def __init__(self, client):
        self.client = client

    @commands.command(usage="<word>", aliases=["definition", "def"])
    async def define(self, ctx, *, word):
        """
        Define a word.
        """

        # First check how many words there are
        words = word.split()
        if len(words) == 1 and dictionary.meaning(words[0]) != None:
            word = words[0]
            await ctx.send("One second...")
            nouns = []
            verbs = []
            adjectives = []
            adverbs = []

            # Create embed
            dict_embed = nextcord.Embed(
            title = "Dictionary Definition",
            description = f"Query: {word}",
            colour = 0x0adbfc
            )
            dict_embed.set_thumbnail(url="https://media.discordapp.net/attachments/952037974420385793/952038039457267712/Eve_Code_Ultimate_2.png")
            dict_embed.set_footer(text="Github: https://github.com/Chubbyman2/eve-bot")

            if word.lower() == "praxis":
                nouns.append(
                    "the worst course in the Engineering Science program")
            elif word.lower() == "calculus":
                nouns.append(
                    "the most rigorous course in the Engineering Science program")

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

                dict_embed.add_field(name="Nouns", value="```-" + "\n-".join(nouns) + "```", inline=False)

            if len(verbs) != 0:
                for verb in verbs:
                    temp = verb
                    for letter in verb:
                        if letter == "(":
                            verb += ")"
                            verbs[verbs.index(temp)] = verb
                dict_embed.add_field(name="Verbs", value="```-" + "\n-".join(verbs) + "```", inline=False)

            if len(adjectives) != 0:
                for adjective in adjectives:
                    temp = adjective
                    for letter in adjective:
                        if letter == "(":
                            adjective += ")"
                            adjectives[adjectives.index(temp)] = adjective
                dict_embed.add_field(name="Adjectives", value="```-" + "\n-".join(adjectives) + "```", inline=False)

            if len(adverbs) != 0:
                for adverb in adverbs:
                    temp = adverb
                    for letter in adverb:
                        if letter == "(":
                            adverb += ")"
                            adverbs[adverbs.index(temp)] = adverb
                dict_embed.add_field(name="Adverbs", value="```-" + "\n-".join(adverbs) + "```", inline=False)
            
            await ctx.send(embed=dict_embed)

        # If it's more than one word
        else:
            await ctx.send("One second...")

            # Create embed
            embed_query = " ".join(words)
            dict_embed = nextcord.Embed(
            title = "Dictionary Definition",
            description = f"Query: {embed_query}",
            colour = 0x0adbfc
            )
            dict_embed.set_thumbnail(url="https://media.discordapp.net/attachments/952037974420385793/952038039457267712/Eve_Code_Ultimate_2.png")
            dict_embed.set_footer(text="Github: https://github.com/Chubbyman2/eve-bot")

            if get_definition(words)[0] == None:
                try:
                    word = get_definition(words)[1].find(class_="kw")
                    word = word.get_text()
                    words = word.split(" ")

                    if get_definition(words)[0] != None:
                        definition = get_definition(words)[0]
                        definition = definition.get_text()
                        dict_embed.add_field(name="Definition", value="```" + str(definition) + "```", inline=False)
                        await ctx.send(embed=dict_embed)
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
                dict_embed.add_field(name="Definition", value="```" + str(definition) + "```", inline=False)
                await ctx.send(embed=dict_embed)


def setup(client):
    client.add_cog(Dictionary(client))
