from src.util import config_holder
from src.util import embeds

print('Loading Message Event Handler...')

data = config_holder.ConfigHolder()


async def handle_message(msg):
    if not msg.content.startswith(tuple(data.get_config('messages', 'prefixes').values())):
        return

    elif msg.content.startswith(data.get_config('messages', 'prefixes')['currency']):
        await currency_cmd(msg)

    elif msg.content.startswith(data.get_config('messages', 'prefixes')['custom_reactions']):
        await custom_reaction_cmd(msg)

    return msg.content


async def currency_cmd(msg):
    pass


async def custom_reaction_cmd(msg):
    msg.content = msg.content[1:]
    if msg.content.startswith('add'):
        data.add_custom_reaction(str(msg.guild.id), msg.content.split()[1], ' '.join(msg.content.split()[2:]))
    else:
        reaction = data.get_custom_reaction(str(msg.guild.id), msg.content.split()[0])
        if reaction.startswith('http'):  # Properly Embed Links to GIF, Images etc.
            await msg.channel.send(embed=embeds.image(reaction))
        else:
            await msg.channel.send(embed=embeds.simple(reaction))
