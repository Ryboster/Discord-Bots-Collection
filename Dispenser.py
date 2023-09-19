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
        #message ID's
        self.target_ids = [1020307735801253898, 1153666715503312966]
        self.authors = [434807903623577620, 572358282895818753, 378985376435404800]
        
        #Emojis and their corresponding roles
        self.emoji_roles = {
            # Emoji: Role
            '♂️': '♂MALE',
            '♀️': '♀FEMALE',
            '🔼': "⬆️18",
            '🔽': '⬇️18'
            # Add more emoji-role mappings as needed
        }


#Startup part:
    async def on_ready(self):
        print(f'logged in as {discord.Client}')

#Assigning roles part:
    async def on_raw_reaction_add(self, payload): #Triggered when reaction is added:
        if payload.message_id in self.target_ids: #If reaction is added in targetted messages:
            try:
                self.decoded_emoji = emojis.decode(payload.emoji.name) #Get emoji and decode it
                guild = client.get_guild(payload.guild_id) #Get guild where that happened
                role = discord.utils.get(guild.roles, name=self.emoji_roles[self.decoded_emoji]) #Get corresponding role from server's roles
                await payload.member.add_roles(role) # Assign role to user     
            except KeyError: #If error occurs:
                guild = client.get_guild(payload.guild_id)
                role = discord.utils.get(guild.roles, name=self.emoji_roles[payload.emoji.name])
                await payload.member.add_roles(role)
                
#Removing roles part:                
    async def on_raw_reaction_remove(self, payload): #Triggered when reaction is removed
        if payload.message_id in self.target_ids: #If reaction is removed in targetted messages:
            try:
                self.decoded_emoji = emojis.decode(payload.emoji.name) #Get emoji and decode it
                guild = client.get_guild(payload.guild_id) #Get guild where that happened
                role = discord.utils.get(guild.roles, name=self.emoji_roles[self.decoded_emoji]) #Get corresponding role from server's roles
                member = guild.get_member(payload.user_id) #Get member who removed the reaction
                await member.remove_roles(role) #Remove the role from the user
            except KeyError:
                guild = client.get_guild(payload.guild_id)
                member = guild.get_member(payload.user_id)
                role = discord.utils.get(guild.roles, name=self.emoji_roles[payload.emoji.name])
                await member.remove_roles(role)

    async def on_message(self, message):
        print('meesage:', message.content, message.author.id)
        if message.content == "!!exit" and message.author.id in self.authors:
            print('Shutting down ...')
            await self.close()
            quit()

client = MyClient(intents=discord.Intents.all())
client.run(token)
