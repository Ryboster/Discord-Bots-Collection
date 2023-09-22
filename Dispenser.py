import discord
import emojis
import sys
from PIL import Image, ImageDraw, ImageFont
import requests
import time
import re
from random import randint

try:
    token = sys.argv[1]
    print(f'TOKEN: {token}')
except IndexError:
    print('No token. Shutting down.')
    quit()


class MyClient(discord.Client):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Message ID's
        self.target_ids = [1020307735801253898, 1153666715503312966]
        # Admins
        self.authors = [434807903623577620, 572358282895818753, 378985376435404800]
        # Users to be reminded of new games
        self.users_game_reminder = [434807903623577620]

        # Emojis and their corresponding roles
        self.emoji_roles = {
            '♂️': '♂MALE',
            '♀️': '♀FEMALE',
            '🔼': "⬆️18",
            '🔽': '⬇️18'
        }

        self.logged_channels = [1020305021553868850, 1019906084774887463, 1019906085001375765, 1049005443239911494,
                                1019906085001375773,
                                1026863916069961748, 1025790628631695570, 1025900669082800158, 1026597897279639612,
                                1030518678892068864]

    # Startup part:
    async def on_ready(self):
        print(f'logged in as {discord.Client}')

    # Assigning roles part:
    async def on_raw_reaction_add(self, payload):
        if payload.message_id in self.target_ids:
            try:
                self.decoded_emoji = emojis.decode(payload.emoji.name)
                guild = client.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=self.emoji_roles[self.decoded_emoji])
                await payload.member.add_roles(role)
            except KeyError:
                guild = client.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=self.emoji_roles[payload.emoji.name])
                await payload.member.add_roles(role)

    # Removing roles part:
    async def on_raw_reaction_remove(self, payload):
        if payload.message_id in self.target_ids:
            try:
                self.decoded_emoji = emojis.decode(payload.emoji.name)
                guild = client.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=self.emoji_roles[self.decoded_emoji])
                member = guild.get_member(payload.user_id)
                await member.remove_roles(role)
            except KeyError:
                guild = client.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                role = discord.utils.get(guild.roles, name=self.emoji_roles[payload.emoji.name])
                await member.remove_roles(role)

    def create_user_message_image(self, username, avatar_url, message_content, *args):
        attachment_urls = False
        attachments_list = False

        if args:
            print(f'{len(args)} arguments received')
            if 'attachments' in str(args[0]).split('/'):
                attachment_urls = args[0]
                print(args)
        # Calculate image height
        lines = []
        current_line = ""
        draw = ImageDraw.Draw(Image.new('RGB', (400, 400), color='#36393e'))
        font = ImageFont.truetype("arial.ttf", 16)
        for word in message_content.split():
            text_size = draw.textsize(current_line + word, font=font)
            if text_size[0] <= 300:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        size_of_lines = 0
        for line in lines:
            size_of_lines += 16

        frame_height = 100 + size_of_lines

        if attachment_urls:
            collective_width = 0
            collective_height = 0
            attachment_position = (10, 100)
            x_position, y_position = attachment_position
            attachments_list = []
            y = 0
            for url in attachment_urls:
                attachment = Image.open(requests.get(url, stream=True).raw)
                attachment_width, attachment_height = attachment.size
                new_attachment_width = 150
                new_attachment_height = int(attachment_height * (new_attachment_width / attachment_width))

                collective_width += new_attachment_width
                resized_image = attachment.resize((new_attachment_width, new_attachment_height), Image.LANCZOS)
                print(f'collective width: {collective_width}')
                print(f"x position: {x_position}")

                if y != 0:
                    x_position += collective_width
                else:
                    collective_height += new_attachment_height
                    collective_width = 0

                if collective_width >= 400 or x_position >= 400:
                    print(f'collective width or x position is higher than 400, {y}')
                    y_position += new_attachment_height
                    collective_height += new_attachment_height
                    x_position = 10
                    resized_image = attachment.resize((new_attachment_width, new_attachment_height), Image.LANCZOS)
                    attachments_list.append((resized_image, (x_position, y_position)))
                    #x_position += collective_width
                    collective_width = 0
                    continue

                attachments_list.append((resized_image, (x_position, y_position)))
                y += 1


            frame_height += collective_height


        frame_width = 400
        print(f'image width: {frame_width}\nimage height: {frame_height}')
        # Create an image
        image = Image.new('RGB', (frame_width, frame_height), color='#36393e')
        # Create a drawing context
        draw = ImageDraw.Draw(image)
        # Choose a font and size
        font = ImageFont.load_default()
        font_size = 16
        font = ImageFont.truetype("arial.ttf", font_size)

        # Set text position
        username_position = (100, 10)
        avatar_position = (10, 10)
        message_position = (100, 40)
        # Load the user's avatar
        avatar = Image.open(requests.get(avatar_url, stream=True).raw)
        avatar = avatar.resize((80, 80))

        # Paste the avatar onto the image
        image.paste(avatar, avatar_position)
        if attachments_list:
            print(attachments_list)
            for picture, position in attachments_list:
                image.paste(picture, position)


        # Write the username to the image
        draw.text(username_position, username, fill='white', font=font)

        message_height = 0
        for line in lines:
            print(line)
            draw.text(message_position, line, fill='white', font=font)
            message_height += font_size
            message_position = (message_position[0], message_position[1] + font_size)
        return image

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
                image = self.create_user_message_image(str(message.author.display_name + "      " + time_list[3]), avatar_url, message.content, embed_urls, attachment_urls)
            elif message.embeds and not message.attachments:
                image = self.create_user_message_image(str(message.author.display_name + "      " + time_list[3]), avatar_url, message.content, embed_urls)
            elif message.attachments and not message.embeds:
                image = self.create_user_message_image(str(message.author.display_name + "      " + time_list[3]), avatar_url, message.content, attachment_urls)
            elif not message.attachments and not message.embeds:
                image = self.create_user_message_image(str(message.author.display_name + "      " + time_list[3]), avatar_url, message.content)
            image.save('image.png')
            # with open('image.png') as image:
            #    image.resize()
            channel = message.guild.get_channel(1019906085710221336)
            await channel.send(f"by: {message.author.display_name}\nin: <#{message.channel.id}>\non: {xtime}",
                               file=discord.File('image.png'))

        # Exiting
        if message.content == "!!exit" and message.author.id in self.authors:
            print('Shutting down ...')
            await self.close()
            quit()

        # Reminding
        elif message.author.id == 719806770133991434:
            if message.embeds:
                for embed in message.embeds:
                    for id in self.users_game_reminder:
                        try:
                            user = message.guild.get_member(id)
                            await user.send(embed.title + "\n" + embed.description)
                            await user.send(embed.url)
                        except:
                            print(f'Tried sending reminder to user {message.author.display_name}. User not in visible server')
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


client = MyClient(intents=discord.Intents.all())
client.run(token)
