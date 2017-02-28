from src.util import embeds
from src.util.data_cruncher import data


async def add(msg):
    if len(msg.content.split()[2:]) <= 1:
        return await embeds.desc_only(msg.channel, 'Too little content for a Custom Reaction!')
    elif msg.content.split()[1] == 'add':  # !add add
        return await embeds.desc_only(msg.channel, 'That\'s not a valid Custom Reaction name.')
    data.add_custom_reaction(msg.guild.id, msg.content.split()[1], ' '.join(msg.content.split()[2:]), msg.author.name)
    return await embeds.desc_only(msg.channel, f'Added new Reaction called {msg.content.split()[1]}.')
