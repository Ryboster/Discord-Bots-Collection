import discord

async def remind(message):
    if message.embeds:
        for embed in message.embeds:
            for id in self.users_game_reminder:
                try:
                    user = message.guild.get_member(id)
                    await user.send(embed.title + "\n" + embed.description)
                    await user.send(embed.url)
                except:
                    print(f'Tried sending reminder to user {message.author.display_name}. User not in visible server')