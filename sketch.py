import discord
import emojis
import sys
import pyautogui
from PIL import Image, ImageDraw, ImageFont
import requests

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
                                1030518678892068864,
                                1116089292524097647]

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

    def create_user_message_image(self, username, avatar_url, message_content):
        # Create an image with a white background
        image = Image.new('RGB', (400, 200), color='white')
        # Create a drawing context
        draw = ImageDraw.Draw(image)
        # Choose a font and size
        font = ImageFont.load_default()
        font_size = 20
        font = ImageFont.truetype("/home/pc/Desktop/arial.ttf", font_size)
        # Calculate text position
        username_position = (100, 10)
        avatar_position = (10, 10)
        message_position = (10, 60)
        # Load the user's avatar
        avatar = Image.open(requests.get(avatar_url, stream=True).raw)
        avatar = avatar.resize((80, 80))

        # Paste the avatar onto the image
        image.paste(avatar, avatar_position)

        # Write the username to the image
        draw.text(username_position, username, fill='black', font=font)

        # Wrap and write the message content to the image
        max_width = 380
        lines = []
        current_line = ""
        for word in message_content.split():
            text_size = draw.textsize(current_line + word, font=font)
            if text_size[0] <= max_width:
                current_line += word + " "
            else:
                lines.append(current_line)
                current_line = word + " "
        lines.append(current_line)

        message_height = 0
        for line in lines:
            draw.text(message_position, line, fill='black', font=font)
            message_height += font_size
            message_position = (message_position[0], message_position[1] + font_size)

        return image

    # Respond to messages part:
    async def on_message(self, message):
        # Logging
        if message.channel.id in self.logged_channels:
            #fc = message.guild.get_member(434807903623577620)
            avatar_url = message.author.avatar
            print(message.author.display_name,":", message.content)
            image = self.create_user_message_image(message.author.display_name, avatar_url, message.content)
            image.save('image.png')
            await fc.send(file=discord.File('image.png'))

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
                        except:
                            print(f'Tried sending reminder to user {id}. User not in visible server')
        # RNG
        elif message.content.startswith('!!roll') and message.author.id in self.authors:
            match = re.search(r'!!roll (\d+)', message.content)
            if match:
                value = int(match.group(1))
                await message.channel.send(randint(1, value))


client = MyClient(intents=discord.Intents.all())
client.run(token)
