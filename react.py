import discum

# Load tokens from tokens.txt
def load_tokens(file_path):
    with open(file_path, 'r') as f:
        return [line.strip() for line in f.readlines()]

tokens = load_tokens('tokens.txt')

# User ID to react to
target_user_id = "1130370024981405747"  # Replace with the actual user ID

# Emoji to react with (e.g., 💀 for a skull)
reaction_emoji = "💀"

# Channel ID where the bot should monitor messages
channel_id = "1316314947701178390"  # Replace with the target channel ID


def create_client(token):
    bot = discum.Client(token=token, log=False)

    @bot.gateway.command
    def on_message(resp):
        if resp.event.ready:  # Ready event
            user_info = bot.gateway.session.user
            if user_info:
                print(f"Logged in as {user_info['username']}")
        if resp.event.message:  # Message received
            message = resp.parsed.auto()
            if message['author']['id'] == target_user_id:
                # React to the message
                response = bot.gateway.request.call(
                    "PUT",
                    f"/channels/{message['channel_id']}/messages/{message['id']}/reactions/{reaction_emoji}/@me"
                )
                if response.status_code == 204:  # HTTP 204 No Content indicates success
                    print(f"Reacted to message: {message['content']}")
                else:
                    print(f"Failed to react. Status code: {response.status_code}")

    return bot

# Start bots for each token
for token in tokens:
    client = create_client(token)
    client.gateway.run(auto_reconnect=True)
    time.sleep(1)  # Prevent rate limiting between token logins
