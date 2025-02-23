import discord
from discord.ext import commands
import random
import requests

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
    


class pack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bold = False
        self.insults = ['pooron', 'ugly nigga', 'indian', 'p3d0', 'loser','chink','whore','slut','cum dumpster']

    def packbible():
        try:
            with open("pack.txt", "r") as file:
                lines = file.readlines()
            return [line.strip() for line in lines]
        except FileNotFoundError:
            print("pack.txt not found!")
            return []


    @commands.command(name = "pressure", aliases = ['p'])
    async def pressure(self, ctx, user: discord.User, times : int=None):
        if times == None: times = 15

        for i in range(times):
            option = random.choice([1,2])
            if option == 1:
                packbibles = self.packbible()
            else:
                adj = wordpack()
                packmessage = f"# {user.mention} {adj} {random.choice(self.insults)}"

            await ctx.send(packmessage)

    @commands.command(name = "bold", aliases = ['b'], help = "toggles bold messages")
    async def boldtoggle(self, ctx, tog: str):
        if tog == True:
            self.bold = True
        else: self.bold = False
        


    @commands.command(name = "ladder", aliases = ['l'], help = "normal ladder")
    async def ladder(self, ctx, *, message: str):
        await ctx.message.delete()
        words = message.split()  
        for word in words:
            await ctx.send(word) 



    @commands.command(name = "boldladder", aliases = ['bl'], help = "ladder a string")
    async def boldladder(self, ctx, *, message: str):
        await ctx.message.delete()
        words = message.split()  
        for word in words:
            await ctx.send(f"# {word}")

    @commands.command(name="pingladder", aliases = ['pl'], help ="ping and ladder")
    async def pingladder(self, ctx, user: discord.User,*, msg : str):
        words = msg.split()
        await ctx.message.delete()
        for word in words: 
            await ctx.send(f'# {user.mention} {word}')


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot:
            if self.bold == True:
                boldmessage = f"# {message.content}"
                await ctx.message.edit(boldmessage)


    

            


    

async def setup(bot):
    await bot.add_cog(pack(bot))