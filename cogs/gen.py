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
 


async def setup(bot):
    await bot.add_cog(general(bot))