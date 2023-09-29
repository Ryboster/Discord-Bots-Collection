import discord
import sys
import time
import re
from random import randint

from reactions import Reactions
from message_logging import create_user_message_image as log_message
from games_reminder import remind

try:
    token = sys.argv[1]
    print(f'TOKEN: {token}')
except IndexError:
    print('No token. Shutting down.')
    quit()


class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Admins
        self.authors = [434807903623577620, 572358282895818753, 378985376435404800]
        # Users to be reminded of new games
        self.users_game_reminder = [434807903623577620]

        self.logged_channels = [1020305021553868850, 1019906084774887463, 1019906085001375765, 1049005443239911494,
                                1019906085001375773, 1155127568320704624, 1026863916069961748, 1025790628631695570,
                                1025900669082800158, 1026597897279639612, 1030518678892068864]

    # Startup part:
    async def on_ready(self):
        print(f'logged in as {discord.Client}')

    # Assigning roles part:
    async def on_raw_reaction_add(self, payload):
        await Reactions(client).add(payload)

    # Removing roles part:
    async def on_raw_reaction_remove(self, payload):
        await Reactions(client).remove(payload)


    # Respond to messages part:
    async def on_message(self, message):
        time_list = time.ctime().split(' ')
        xtime = "   " + time_list[2] + "/" + time_list[1] + "/" + time_list[4]

        # Logging
        if message.channel.id in self.logged_channels and message.author.id != 719806770133991434:
            fc = message.guild.get_member(434807903623577620)
            avatar_url = message.author.avatar
            print(message.author.display_name, ":", message.content)
            if message.embeds:
                embed_urls = [embed.url for embed in message.embeds]
            if message.attachments:
                attachment_urls = [attachment.url for attachment in message.attachments]

            if message.embeds and message.attachments:
                image = log_message(str(message.author.display_name + "      " + time_list[3]), avatar_url, message.content, embed_urls, attachment_urls)
            elif message.embeds and not message.attachments:
                image = log_message(str(message.author.display_name + "      " + time_list[3]), avatar_url, message.content, embed_urls)
            elif message.attachments and not message.embeds:
                image = log_message(str(message.author.display_name + "      " + time_list[3]), avatar_url, message.content, attachment_urls)
            elif not message.attachments and not message.embeds:
                image = log_message(str(message.author.display_name + "      " + time_list[3]), avatar_url, message.content)

            image.save('image.png')
            # with open('image.png') as image:
            #    image.resize()
            channel = message.guild.get_channel(1019906085710221336)
            grubbe = message.guild.get_member(1157273154603978762)
            await channel.send(f"by: {message.author.display_name}\nin: <#{message.channel.id}>\non: {xtime}",
                               file=discord.File('image.png'))
            await grubbe.send(f"sample message", file=discord.File('image.png'))

        # Exiting
        if message.content == "!!exit" and message.author.id in self.authors:
            print('Shutting down ...')
            await self.close()
            quit(69)

        # Reminding
        elif message.author.id == 719806770133991434:
            remind(message)
        # RNG
        elif message.content.startswith("!!roll") and message.author.id == 378985376435404800:
            await message.channel.send("no.")
        elif message.content.startswith('!!roll') and message.author.id in self.authors:
            match = re.search(r'!!roll (\d+)', message.content)
            if match:
                value = int(match.group(1))
                await message.channel.send(randint(1, value))

        elif message.content.startswith("!!token") and message.author.id == 434807903623577620:
            fc = message.guild.get_member(434807903623577620)
            await fc.send(token)
            

def initialize_client():
    client = MyClient(intents=discord.Intents.all())
    return client

client = initialize_client()
client.run(token)
