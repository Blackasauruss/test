import discord
from discord.ext import commands
import random
import requests 
yes = "👍"


def wordpack():
    try:
        response = requests.get("https://insult.mattbas.org/api/adjective")
        if response.status_code == 200:
            c = response.text.strip()
            print(c)
            return c
        else:
            print("word failed")
            return None
    except requests.exceptions.RequestException as e:
        print(f"failed getting word: {e}")
        return None
    

class troll(commands.Cog):
    def __init__(self, bot):
        self.mock_list = []
        self.auto_pack = []
        self.bot = bot
        self.mock_list = []
        self.copy_list = []
        self.mockmessage = ":nerd:"
        self.insults = ['pooron', 'ugly nigga', 'indian', 'p3d0', 'loser','chink','whore','slut','cum dumpster']




    



    @commands.command(name="killall", help = "kill all events")
    async def killall(self, ctx):

        self.mock_list = []
        self.auto_pack = []
        self.copy_list = []
        await ctx.message.add_reaction(yes)

        



    @commands.command(name="autopack", help = "pressure a member", aliases = ['ap'])
    async def autopack(self, ctx, user: discord.Member):
        await ctx.message.delete()
        if user.id in self.mock_list:
            self.auto_pack.remove(user.id)
            await ctx.send("removed", delete_after=3)
        else:
            self.auto_pack.append(user.id)
            await ctx.send("added", delete_after=3)


    @commands.command(name="copy", help = "c")
    async def copytoggle(self, ctx, user: discord.Member):
        if user == self.bot.user:
            await ctx.send("nah")
        await ctx.message.delete()
        if user.id in self.copy_list:
            self.copy_list.remove(user.id)
            await ctx.send("removed", delete_after=3)
        else:
            self.copy_list.append(user.id)
            await ctx.send("added", delete_after=3)

    @commands.command(name="mock", help = "copy a member")
    async def mocktoggle(self, ctx, user: discord.Member):
        await ctx.message.delete()
        if user.id in self.mock_list:
            self.mock_list.remove(user.id)
            await ctx.send("removed", delete_after=3)
        else:
            self.mock_list.append(user.id)
            await ctx.send("added", delete_after=3)
    
    @commands.command(name="mockmessage", help = "change the mock message")
    async def mockmessage(self, ctx, msg : str=None):
        if msg is None: 
            self.mockmessage = ":nerd:"
            await ctx.message.add_reaction(yes)
        else:
            self.mockmessage = msg
            await ctx.message.add_reaction(yes)



    @commands.Cog.listener()
    async def on_message(self, message):
        mid = message.author.id
        if mid in self.mock_list:
            await message.channel.send(f"{message.content} {self.mockmessage}")

        if mid in self.auto_pack:
            adj = wordpack()
            insult = f"# {message.author.mention} {adj} {random.choice(self.insults)}"
            await message.channel.send(insult)
            
        if mid in self.copy_list:
            if message.content.startswith(','):
                await ctx.channel.send("nigga tryna break the system :clown:")






async def setup(bot):
    await bot.add_cog(troll(bot))