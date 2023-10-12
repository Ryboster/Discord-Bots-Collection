import discord
import requests
import time
import os

import discord

intents = discord.Intents.default()
intents.messages = True  # Enable the message intent

# Replace 'YOUR_BOT_TOKEN' with your bot's token
bot_token = 'MTE1NzI3MzE1NDYwMzk3ODc2Mg.GFmQu1.7Yzu8GTt07TK2jlq5U999Jq553gsn8vmLxFsmk'
client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user.name}')

@client.event
async def on_message(message):
    #print('MESSAGE:',message)
    print('MESSAGE_CONTENT:', message.content)
    if message.content.startswith('!!scrape'):
        # Replace 'YOUR_GUILD_ID' and 'YOUR_CHANNEL_ID' with the desired guild and channel IDs
        channel_id = '1019906085710221336'
        channel = message.guild.get_channel(channel_id)
        print('received scrape')
        #channel = guild.get_channel(channel_id)

        async for message in channel.history(limit=None):
            # Process each message here
            print(f'{message.author}: {message.content}')
            if message.attachments:
                attachment_urls = [attachment.url for attachment in message.attachments]

        scrape_images(attachment_urls)

    elif message.content == "!!ping":
        print('pong')


def scrape_images(attachments):
    for attachment_url in attachments:
        response = requests.get(attachment_url, stream=True)

        if not os.path.exists('chat_history'):
            os.makedirs('chat_history')

        if response.status_code == 200:
            filename = os.path.join("image", os.path.basename(attachment_url))

            # Open a file in binary write mode and save the image data
            with open(filename, "wb") as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)

            print(f"Saved image: {filename}")


# Run the bot
client.run(bot_token)
