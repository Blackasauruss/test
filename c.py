import discord
import asyncio

# Replace 'YOUR_TOKEN' with your actual self-bot token
TOKEN = "MTIwNzc3OTE0NTIxNjQzNDI3Nw.GuEtPu.5oi6ISq5d2ENYbY2USMWGzhRrgD2d0POPudNp4"
CHANNEL_ID = 921951061332336640  # Replace with your target channel ID

client = discord.Client()

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    
    channel = client.get_channel(CHANNEL_ID)
    if channel:
        print(f"Found channel: {channel.name}")

        # Deleting all messages in the channel
        async for message in channel.history(limit=None):
            try:
                await message.delete()
                print(f'Deleted message from {message.author}: {message.content}')
            except discord.errors.NotFound:
                # If the message is already deleted or inaccessible
                print(f'Failed to delete message from {message.author}')
    
    else:
        print("Channel not found!")
    
    await client.close()

client.run(TOKEN)