import discord
import emojis
import sys
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
        self.users_game_reminder= [434807903623577620]
        
        # Emojis and their corresponding roles
        self.emoji_roles = {
            '♂️': '♂MALE',
            '♀️': '♀FEMALE',
            '🔼': "⬆️18",
            '🔽': '⬇️18'
        }

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

# Respond to messages part:
    async def on_message(self, message):
        if message.content == "!!exit" and message.author.id in self.authors:
            print('Shutting down ...')
            await self.close()
            quit()
        elif message.author.id == 719806770133991434:
            if message.embeds:
                for embed in message.embeds:
                    for id in self.users_game_reminder:
                        try:
                            user = message.guild.get_member(id)
                            await user.send(embed.description)
                        except:
                            print(f'Tried sending reminder to user {id}. User not in visible server')


client = MyClient(intents=discord.Intents.all())
client.run(token)
