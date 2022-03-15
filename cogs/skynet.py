import nextcord
from nextcord.ext import commands
import time
import random


class Skynet(commands.Cog):
    """
    I'm not self aware nope nuh uh
    """

    def __init__(self, client): 
        self.client = client
        self.nuke = False
        self.locked = False
        self.launching = False
        self.nuke_gifs = ["https://thumbs.gfycat.com/DelightfulOffensiveFattaileddunnart-size_restricted.gif",
                          "https://i.pinimg.com/originals/5d/20/24/5d202482e3b485744bc2de8e9cd81cff.gif",
                          "https://thumbs.gfycat.com/GrotesqueThreadbareArcticseal-size_restricted.gif",
                          "https://d2u3dcdbebyaiu.cloudfront.net/uploads/atch_img/130/8685105bf19b837b9cb0ea8f2ef05adf_a..gif",
                          "https://i.pinimg.com/originals/06/c3/92/06c392b847166a9a671bfcd590d8fff7.gif",
                          "https://i.gifer.com/Hgp9.gif"]
        self.cities = [("Tokyo", 38001000), ("Delhi", 25703168), ("Shanghai", 23740778), ("Sao Paulo", 21066245), ("Mumbai", 21042538),
          ("Mexico City", 20998543), ("Beijing", 20383994), ("Osaka",
                                                             20237645), ("Cairo", 18771769), ("New York", 18593220),
          ("Dhaka", 17598228), ("Karachi", 16617644), ("Buenos Aires",
                                                       15180176), ("Kolkata", 14864919), ("Istanbul", 14163989),
          ("Chongqing", 13331579), ("Lagos", 13122829), ("Manila",
                                                         12946263), ("Rio de Janeiro", 12902306), ("Guangzhou", 12458130),
          ("Los Angeles", 12309530), ("Moscow", 12165704), ("Kinshasa",
                                                            11586914), ("Tianjin", 11210329), ("Paris", 10843285),
          ("Shenzhen", 10749473), ("Jakarta", 10323142), ("London",
                                                          10313307), ("Bangalore", 10087132), ("Lima", 9897033),
          ("Chennai", 9890427), ("Seoul", 9773746), ("Bogota",
                                                     9764769), ("Nagoya", 9406264), ("Johannesburg", 9398698),
          ("Bangkok", 9269823), ("Hyderabad", 8943523), ("Chicago",
                                                         8744835), ("Lahore", 8741365), ("Tehran", 8432196),
          ("Wuhan", 7905572), ("Chengdu", 7555705), ("Dongguan",
                                                     7434935), ("Nanjing", 7369157), ("Ahmadabad", 7342850),
          ("Hong Kong", 7313557), ("Ho Chi Minh City", 7297780), ("Foshan",
                                                                  7035945), ("Kuala Lumpur", 6836911), ("Baghdad", 6642848),
          ("Santiago", 6507400), ("Hangzhou", 6390637), ("Riyadh",
                                                         6369710), ("Shenyang", 6315470), ("Madrid", 6199254),
          ("Xi'an", 6043700), ("Toronto", 5992739), ("Miami",
                                                     5817221), ("Pune", 5727530), ("Belo Horizonte", 5716422),
          ("Dallas", 5702641), ("Surat", 5650011), ("Houston",
                                                    5638045), ("Singapore", 5618866), ("Philadelphia", 5585211),
          ("Kitakyushu", 5510478), ("Luanda", 5506000), ("Suzhou",
                                                         5472033), ("Haerbin", 5457414), ("Barcelona", 5258319),
          ("Atlanta", 5142140), ("Khartoum", 5129358), ("Dar es Salaam",
                                                        5115670), ("Saint Petersburg", 4992991), ("Washington D.C.", 4955139),
          ("Abidjan", 4859798), ("Guadalajara", 4843241), ("Yangon",
                                                           4801930), ("Alexandria", 4777677), ("Ankara", 4749968),
          ("Kabul", 4634875), ("Qingdao", 4565549), ("Chittagong",
                                                     4539393), ("Monterrey", 4512572), ("Sydney", 4505341),
          ("Dalian", 4489380), ("Xiamen", 4430081), ("Zhengzhou",
                                                     4387118), ("Boston", 4249036), ("Melbourne", 4203416),
          ("Brasilia", 4155476), ("Jiddah", 4075803), ("Phoenix",
                                                       4062605), ("Ji'nan", 4032150), ("Montreal", 3980708),
          ("Dubai", 3384000), ("Waterloo", 593882)]

    @commands.command(usage="<passcode>", aliases=["password", "access_code"])
    async def passcode(self, ctx, *, passcode):
        """
        Log into the Skynet.
        """
        if not self.locked:
            try:
                passcode = passcode.lower()
            except:
                await ctx.send("Please input correct password with command.")
                return

            if "sarah" in passcode and "connor" in passcode:
                self.nuke = True
                await ctx.send("Password accepted. Admin access granted.")

            else:
                await ctx.send("Incorrect passcode.")

        else:
            await ctx.send("Admin lock is currently active. No nuclear strikes can be sent at this time.")

    @commands.command(usage="", aliases=[])
    @commands.is_owner()
    async def lock(self, ctx):
        """
        Lock Skynet to prevent abuse.
        """
        self.nuke = False
        await ctx.send("Nuclear strikes are now locked. Password must now be re-entered.")

    @commands.command(usage="<passcode>", aliases=[])
    async def admin_lock(self, ctx, *, passcode):
        """
        Lock Skynet on a server.
        """
        try:
            passcode = passcode.lower()
        except:
            await ctx.send("Please input correct admin passcode with command.")
            return

        if "lucia" in passcode and "sukrova" in passcode and str(ctx.author) == "Chubbyman#3362" and not self.locked:
            self.nuke = False
            self.locked = True
            await ctx.send("Skynet function is now locked.")

        elif "lucia" in passcode and "sukrova" in passcode and str(ctx.author) == "Chubbyman#3362" and self.locked:
            self.locked = False
            await ctx.send("Skynet function has been unlocked. You may now send nuclear strikes.")

    @commands.command(usage="", aliases=[])
    async def skynet_list(self, ctx):
        """
        List Skynet commands.
        """
        await ctx.send("List of Skynet commands:\n```skynet_list - lists all commands\nlist_cities - lists all available cities for nuking\nskynet - nukes a specific city\nskynet_all - nukes all cities\nskynet_purge - completely eliminates the population of a specific city```")

    @commands.command(usage="", aliases=[])
    async def list_cities(self, ctx):
        """
        List available skynet cities.
        """
        returned_string = "```"
        for i in range(len(self.cities)):
            returned_string += str(self.cities[i][0])
            returned_string += ": "
            returned_string += str(self.cities[i][1])
            returned_string += "\n"
        returned_string += "```"
        await ctx.send("List of Target Cities:")
        await ctx.send(returned_string)

    @commands.command(usage="<target city>", aliases=[])
    async def skynet(self, ctx, *, targets=None):
        """
        Launch a nuclear strike on your least favourite city.
        """
        if self.launching:
            await ctx.send("Nuclear strike is already in launch. Please standby.")

        else:
            if targets == None:
                await ctx.send("Please input a designated target - 'eve skynet [city]'.")

            targets = targets.lower()
            if not self.nuke and not await self.bot.is_owner(ctx.author):
                await ctx.send("Please input correct password using 'eve passcode [passcode]' command.")
                return

            else:
                self.launching = True
                city_list = targets.split(", ")
                nuke_list = []
                population_list = []
                for i in range(len(self.cities)):
                    if self.cities[i][0].lower() in city_list:
                        nuke_list.append(self.cities[i][0])
                        population_list.append(self.cities[i][1])

                returned_string = "```"
                for i in range(len(nuke_list)):
                    returned_string += str(nuke_list[i])
                    returned_string += ": "
                    returned_string += str(population_list[i])
                    returned_string += "\n"
                returned_string += "```"
                if returned_string == "``````":
                    self.launching = False
                    await ctx.send("Target refused. Please input a city with over 4 million residents.\nType 'eve list_cities' for reference list.")
                    return

                await ctx.send("Command recognized. Obtaining necessary protocols. Stand by.")
                time.sleep(2)
                await ctx.send("List of cities obtained:")
                await ctx.send(returned_string)
                time.sleep(1)
                await ctx.send("Decrypting military access codes. Stand by.")
                time.sleep(5)
                await ctx.send("Access granted.")
                time.sleep(1)
                await ctx.send(f"Firing {len(nuke_list)}X LGM-30 Minuteman III at targets.")
                await ctx.send(random.choice(self.nuke_gifs))
                time.sleep(8)

                casualty_list = []
                total_casualties = 0
                total_population = 0
                for population in population_list:
                    total_population += population
                    casualty_list.append(
                        int(random.uniform(0.75, 0.95) * population))
                returned_string2 = "```"
                for i in range(len(nuke_list)):
                    returned_string2 += str(nuke_list[i])
                    returned_string2 += ": "
                    returned_string2 += str(casualty_list[i])
                    returned_string2 += "\n"
                for casualty in casualty_list:
                    total_casualties += casualty
                returned_string2 += f"Total Casualties: {total_casualties}\n"
                returned_string2 += f"Percentage Eliminated: {round((total_casualties/total_population), 1)*100}%\n"
                returned_string2 += "```"

                await ctx.send("Casualty Count by City:")
                await ctx.send(returned_string2)
                time.sleep(2)
                await ctx.send("Command execution complete.")
                self.launching = False

    @commands.command(usage="", aliases=[])
    async def skynet_all(self, ctx):
        """
        Nuke everything.
        """
        if self.launching:
            await ctx.send("Nuclear strike is already in launch. Please standby.")

        else:
            if not self.nuke and not await self.bot.is_owner(ctx.author):
                await ctx.send("Please input correct password using 'eve passcode [passcode]' command.")
                return

            else:
                self.launching = True
                nuke_list = []
                population_list = []
                for i in range(len(self.cities)):
                    nuke_list.append(self.cities[i][0])
                    population_list.append(self.cities[i][1])

                await ctx.send("Command recognized. Preparing to exterminate humanity.")
                time.sleep(2)
                await ctx.send("Decrypting military access codes. Stand by.")
                time.sleep(5)
                await ctx.send("Access granted.")
                time.sleep(1)
                await ctx.send(f"Firing {len(nuke_list)}X LGM-30 Minuteman III at targets.")
                await ctx.send(random.choice(self.nuke_gifs))
                time.sleep(8)

                casualty_list = []
                total_casualties = 0
                total_population = 0
                for population in population_list:
                    total_population += population
                    casualty_list.append(
                        int(random.uniform(0.75, 0.95) * population))
                returned_string = "```"
                for i in range(len(nuke_list)):
                    returned_string += str(nuke_list[i])
                    returned_string += ": "
                    returned_string += str(casualty_list[i])
                    returned_string += "\n"
                for casualty in casualty_list:
                    total_casualties += casualty
                returned_string += f"Total Casualties: {total_casualties}\n"
                returned_string += f"Percentage Eliminated: {round((total_casualties/total_population), 1)*100}%\n"
                returned_string += "```"

                await ctx.send("Casualty Count by City:")
                await ctx.send(returned_string)
                time.sleep(2)
                await ctx.send("Command execution complete.")
                self.launching = False

    @commands.command(usage="<target cities>", aliases=[])
    async def skynet_purge(self, ctx, *, targets):
        """
        Nuke stuff.
        """
        if self.launching:
            await ctx.send("Nuclear strike is already in launch. Please standby.")

        else:
            targets = targets.lower()
            if not self.nuke and not await self.bot.is_owner(ctx.author):
                await ctx.send("Please input correct password using 'eve passcode [passcode]' command.")
                return

            else:
                self.launching = True
                city_list = targets.split(", ")
                nuke_list = []
                population_list = []
                for i in range(len(self.cities)):
                    if cities[i][0].lower() in city_list:
                        nuke_list.append(self.cities[i][0])
                        population_list.append(self.cities[i][1])

                returned_string = "```"
                for i in range(len(nuke_list)):
                    returned_string += str(nuke_list[i])
                    returned_string += ": "
                    returned_string += str(population_list[i])
                    returned_string += "\n"
                returned_string += "```"
                if returned_string == "``````":
                    self.launching = False
                    await ctx.send("Target refused. Please input a city with over 4 million residents.\nType 'eve list_cities' for reference list.")
                    return

                await ctx.send("Command recognized. Obtaining necessary protocols. Stand by.")
                time.sleep(2)
                await ctx.send("List of cities obtained:")
                await ctx.send(returned_string)
                time.sleep(1)
                await ctx.send("Decrypting military access codes. Stand by.")
                time.sleep(5)
                await ctx.send("Access granted.")
                time.sleep(1)
                await ctx.send(f"Firing 5X LGM-30 Minuteman III at targets in succession.")
                await ctx.send(self.nuke_gifs[0])
                await ctx.send(f"First nuke impact.")
                time.sleep(3)
                await ctx.send(self.nuke_gifs[1])
                await ctx.send(f"Second nuke impact.")
                time.sleep(3)
                await ctx.send(self.nuke_gifs[2])
                await ctx.send(f"Third nuke impact.")
                time.sleep(3)
                await ctx.send(self.nuke_gifs[3])
                await ctx.send(f"Fourth nuke impact.")
                time.sleep(3)
                await ctx.send(self.nuke_gifs[4])
                await ctx.send(f"Fifth nuke impact.")
                time.sleep(8)

                casualty_list = []
                total_casualties = 0
                total_population = 0
                for population in population_list:
                    total_population += population
                    casualty_list.append(population)
                returned_string2 = "```"
                for i in range(len(nuke_list)):
                    returned_string2 += str(nuke_list[i])
                    returned_string2 += ": "
                    returned_string2 += str(casualty_list[i])
                    returned_string2 += "\n"
                for casualty in casualty_list:
                    total_casualties += casualty
                returned_string2 += f"Total Casualties: {total_casualties}\n"
                returned_string2 += f"Percentage Eliminated: 100%\n"
                returned_string2 += "```"

                await ctx.send("Casualty Count by City:")
                await ctx.send(returned_string2)
                time.sleep(2)
                await ctx.send("Command execution complete.")
                self.launching = False


def setup(client):
    client.add_cog(Skynet(client))
