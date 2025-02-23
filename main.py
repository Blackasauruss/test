import discord
from discord.ext import commands
import os

# Set up the bot with command prefix


bot = commands.Bot(command_prefix=".", self_bot = True)

# Define the path to the cogs folder
COGS_FOLDER = "cogs"


y = "✅"
x = "❌"
@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

    # Load all cogs from the 'cogs' folder
    for filename in os.listdir(COGS_FOLDER):
        if filename.endswith(".py"):
            cog_name = filename[:-3]  # Strip the '.py' extension
            try:
                await bot.load_extension(f"cogs.{cog_name}")
                print(f"Loaded cog: {cog_name}")
            except Exception as e:
                print(f"Failed to load cog {cog_name}: {e}")

@bot.command(name='h')
async def helps(ctx, cog: str = None): 
    if cog is None:
        # Show all cogs if no cog is specified
        loaded_cogs = [f"{cog_name}" for cog_name in bot.cogs]
        help_message = '```'+"cogs:\n\n" + "\n".join(loaded_cogs)+'```'
        await ctx.send(help_message)
    else:
        # Show commands in a specific cog
        cog_name = cog.lower()
        if cog_name in bot.cogs:
            cog = bot.cogs[cog_name]
            commands_list = [f"{command.name}: {command.help}" for command in cog.walk_commands()]
            help_message = f"``` commands in the {cog_name} cog:\n\n" + "\n".join(commands_list)+"```"
            await ctx.send(help_message)
        else:
            await ctx.send(f"no loaded")

@bot.command()
async def load(ctx, extension: str):
    try:
        bot.load_extension(f"cogs.{extension}")
        await ctx.message.add_reaction(y)
    except Exception as e:
        await ctx.message.add_reaction(x)

@bot.command()
async def unload(ctx, extension: str):
    try:
        await ctx.message.add_reaction(y)
    except Exception as e:
        await ctx.message.add_reaction(x)

@bot.command()
async def reload(ctx, extension: str):
    try:
        bot.unload_extension(f"cogs.{extension}")
        bot.load_extension(f"cogs.{extension}")
        await ctx.message.add_reaction(y)
    except Exception as e:
        await ctx.message.add_reaction(x)


USER_TOKEN = "MTAwMzM1NDEwNjU1MjkyNjI1OA.G_akcx.Uld5abawuFVQhbyocwwmfotKucoOamNvMBBRQ4"

bot.run(USER_TOKEN) 