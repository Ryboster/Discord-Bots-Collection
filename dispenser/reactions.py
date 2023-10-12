import emojis
import discord

class Reactions():

    def __init__(self, client):
        # Message ID's
        self.client = client
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
                                1019906085001375773, 1155127568320704624, 1026863916069961748, 1025790628631695570,
                                1025900669082800158, 1026597897279639612, 1030518678892068864]

    # Assigning roles part:
    async def add(self, payload):
        if payload.message_id in self.target_ids:
            try:
                self.decoded_emoji = emojis.decode(payload.emoji.name)
                guild = self.client.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=self.emoji_roles[self.decoded_emoji])
                await payload.member.add_roles(role)
            except KeyError:
                guild = self.client.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=self.emoji_roles[payload.emoji.name])
                await payload.member.add_roles(role)
    async def remove(self, payload):
        if payload.message_id in self.target_ids:
            try:
                self.decoded_emoji = emojis.decode(payload.emoji.name)
                guild = self.client.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=self.emoji_roles[self.decoded_emoji])
                member = guild.get_member(payload.user_id)
                await member.remove_roles(role)
            except KeyError:
                guild = self.client.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                role = discord.utils.get(guild.roles, name=self.emoji_roles[payload.emoji.name])
                await member.remove_roles(role)

#client = Reactions(intents=discord.Intents.all())