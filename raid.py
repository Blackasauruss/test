import discum
import threading
import time

# Load tokens from file
with open("tokens.txt", "r") as file:
    tokens = [line.strip() for line in file if line.strip()]

# User ID to react to
TARGET_USER_ID = "703318911999017151"  # Replace with actual user ID
EMOJI = "🔥"  # Replace with desired emoji (Unicode emoji or :custom_emoji_name:)

# Function to handle bot reactions globally
def bot_reactor(token):
    bot = discum.Client(token=token, log=False)

    @bot.gateway.command
    def on_message(resp):
        if resp.event.message:
            message = resp.parsed.auto()
            author_id = message["author"]["id"]
            message_id = message["id"]
            channel_id = message["channel_id"]

            if author_id == TARGET_USER_ID:
                print(f"[{token[:5]}...] Reacting to message {message_id} in channel {channel_id}")
                
                # Send reaction using bot._http.postReaction()
                bot._http.postReaction(channel_id, message_id, EMOJI)

    bot.gateway.run(auto_reconnect=True)

# Start a thread for each bot
threads = []
for token in tokens:
    thread = threading.Thread(target=bot_reactor, args=(token,))
    thread.start()
    threads.append(thread)
    time.sleep(1)  # Prevent rate-limiting issues

# Keep script running
for thread in threads:
    thread.join()