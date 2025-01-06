import discord
from discord.ext import commands
import random
import requests 
yes = "👍"
no = "❌"
import sqlite3

conn = sqlite3.connect('settings.db')
c = conn.cursor()

# Create the triggers table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS trigger (
                    trigger TEXT UNIQUE PRIMARY KEY, 
                    response TEXT NOT NULL)''')
conn.commit()


class general(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.reacts = {}

    @commands.command(name = "clearreacts", aliases = ['cr'])
    async def clearreacts(self, ctx):
        self.reacts = {}

    @commands.command(name="addgif", aliases = ['ag'], help = 'add a gif responder')
    async def addgif(self, ctx, trigger: str, gif: str):
        await ctx.message.delete()
        try:
            c.execute("INSERT INTO trigger (trigger, response) VALUES (?, ?)", (trigger, gif))
            conn.commit()
            await ctx.send("added", delete_after=3)
        except Exception as e:
            await ctx.message.add_reaction(no)
            print (f"error adding gif - {e}")
    
    @commands.command(name = "reacts")
    async def reactss(self, ctx, user: discord.User, react):
        try: 
            self.reacts[user.id] = react 
            await ctx.message.add_reaction(yes)
        except Exception as e:
            print(e)
            await ctx.message.add_reaction(no)


    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:

            c.execute("SELECT trigger, response FROM trigger")
            triggers = c.fetchall()

            for trigger, response in triggers:
                if f".{trigger.lower()}" == message.content.lower():
                    await message.delete()
                    print(f".{trigger.lower()}")
                
                #check if replied to 
                    if message.reference:
                        ogmsg = await message.channel.fetch_message(message.reference.message_id)
                        await ogmsg.reply(response)
                    else:

                        await message.channel.send(response)
        if message.author.id in self.reacts.keys():
            react = self.reacts[message.author.id]
            await message.add_reaction(react)


async def setup(bot):
    await bot.add_cog(general(bot))