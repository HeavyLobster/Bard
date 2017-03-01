import json
import re
import requests
import urllib

from src.events.reactions import create_custom_reaction_embed
from src.util import embeds
from src.util.data_cruncher import data


async def add(msg):
    if len(msg.content.split()[2:]) < 1:
        return await embeds.desc_only(msg.channel, 'Too little content for a Custom Reaction!')
    elif msg.content.split()[1] == 'add':  # !add add
        return await embeds.desc_only(msg.channel, 'That\'s not a valid Custom Reaction name.')
    data.add_custom_reaction(msg.guild.id, msg.content.split()[1], ' '.join(msg.content.split()[2:]), msg.author.name)
    return await embeds.desc_only(msg.channel, f'Added new Custom Reaction called {msg.content.split()[1]}.')


async def meow(msg):
    link = json.load(urllib.request.urlopen('http://random.cat/meow'))['file']
    return await embeds.img_only(msg.channel, link)


async def woof(msg):
    url = requests.get('https://api.giphy.com/v1/gifs/random?'
                       'api_key=dc6zaTOxFJmzC&tag=dog').json()['data_cruncher.data']['image_original_url']
    return await embeds.img_only(msg.channel, f'{url}')


async def get_one(msg):
    try:
        reaction = data.get_custom_reaction(msg.guild.id, msg.content[1:].split()[0])
    except IndexError:
        pass
    else:
        if reaction is None:
            return None
        elif reaction[0].startswith('http'):  # Properly Embed Links to GIF, Images etc.
            return await embeds.img_with_footer(msg.channel, reaction[0], f'Added by {reaction[1]}', reaction[2])
        elif reaction[0] != '':
            return await embeds.desc_with_footer(msg.channel, reaction[0], f'Added by {reaction[1]}', reaction[2])


async def build_list(msg):
    custom_reactions = data.get_all_custom_reactions_on_guild(msg.guild.id)
    if custom_reactions is None:
        return await embeds.desc_only(msg.channel, 'Sorry, no Quotes were found for this Server.')
    else:
        await create_custom_reaction_embed(f'- All Custom Reactions on {msg.guild.name} - ',
                                           custom_reactions, msg.channel,
                                           'https://lh3.googleusercontent.com/'
                                           'BvIDv_HYH8HnHubWn_lle2eC5lm5lY3kAGI'
                                           'kFniSk8x_SDpbUr0dlNTe6P6j_C8f4cSmH-d'
                                           '0rtuSlUU=w1441-h740')


async def hugemoji(msg):
    emoji_id = re.search('[0-9]+', msg.content)
    # Make sure it also works when there's a number in the ID!
    try:
        if len(emoji_id.group(0)) == 1:
            emoji_id = re.search('[0-9]+', msg.content[msg.content.find(emoji_id.group(0)) + 1:])
    except AttributeError:
        return await embeds.desc_only(msg.channel, 'Sorry, something went wrong.')
    else:
        return await embeds.img_only(msg.channel, f'https://cdn.discordapp.com/emojis/{emoji_id.group(0)}.png')
