import discord
import requests
import asyncio

DISCORD_TOKEN = "REDACTED_DISCORD_BOT_TOKEN"
DISCORD_CHANNEL_ID = 1041982465079783474
DISCORD_GUILD_ID = 1040671795994443777
BLOCKED_SERVERS_URL = 'https://raw.githubusercontent.com/games647/Minecraft-Blocked-Servers/main/blockedservers.txt'
HASHES_FILE = 'sent_hashes.txt'

intents = discord.Intents(message_content=True, guilds=True)
client = discord.Client(intents=intents)

def read_sent_hashes():
    try:
        with open(HASHES_FILE, 'r') as file:
            return dict(line.strip().split(':') for line in file.readlines())
    except FileNotFoundError:
        return {}

def write_sent_hashes(sent_hashes):
    with open(HASHES_FILE, 'w') as file:
        for server_hash, message_id in sent_hashes.items():
            file.write(f"{server_hash}:{message_id}\n")

async def fetch_and_send_blocked_servers():
    try:
        response = requests.get(BLOCKED_SERVERS_URL)
        response.raise_for_status()
        lines = response.text.strip().split('\n')
        new_hashes = set()

        for line in lines:
            parts = line.split(' : ')

            if len(parts) == 2:
                ip_address, server_name = parts
                server_name = server_name.strip()
                server_hash = ip_address.strip()
                message = f"Server **{server_name}** has been blocked for breaking EULA!"
            else:
                server_hash = line.strip()
                message = f"Server with hash **{server_hash}** has been blocked for breaking EULA!"

            new_hashes.add(server_hash)

            if server_hash not in sent_hashes_messages:
                guild = client.get_guild(DISCORD_GUILD_ID)
                channel = guild.get_channel(DISCORD_CHANNEL_ID)
                sent_message = await channel.send(message)
                sent_hashes_messages[server_hash] = sent_message.id

        removed_hashes = set(sent_hashes_messages.keys()) - new_hashes

        for removed_hash in removed_hashes:
            message_id = sent_hashes_messages.pop(removed_hash)
            guild = client.get_guild(DISCORD_GUILD_ID)
            channel = guild.get_channel(DISCORD_CHANNEL_ID)
            message = await channel.fetch_message(message_id)
            await message.delete()

        write_sent_hashes(sent_hashes_messages)

    except Exception as e:
        print(f"Error fetching or sending blocked servers: {e}")

async def update_blocked_servers():
    while True:
        await fetch_and_send_blocked_servers()
        await asyncio.sleep(15)

@client.event
async def on_ready():
    print(f'Logged in as {client.user}')
    global sent_hashes_messages
    sent_hashes_messages = read_sent_hashes()
    await update_blocked_servers()

if __name__ == '__main__':
    try:
        asyncio.run(client.start(DISCORD_TOKEN))
    except KeyboardInterrupt:
        asyncio.run(client.close())
        print("Bot stopped.")
