import urllib

import json
import re
import requests

from src.events import reactions
from src.messages import administration, custom_reactions, roles
from src.util import data_cruncher
from src.util import embeds

print('Loading Message Event Handler... ', end='')

replies = {
    data_cruncher.data.get_prefix('administration'): {
        'addmod': administration.add_mod,
        'rmmod': administration.remove_mod,
        'removemod': administration.remove_mod,
        'addadmin': administration.add_admin,
        'rmadmin': administration.remove_admin,
        'removeadmin': administration.remove_admin,
        'changeactivity': administration.change_activity,
        'kick': administration.kick,
        'ban': administration.ban
    },
    data_cruncher.data.get_prefix('roles'): {
        'assign': roles.assign,
        'iam': roles.assign,
        'remove': roles.remove,
        'rm': roles.remove,
        'roles': roles.list_self_assignable,
        'lsar': roles.list_self_assignable,
        'iamn': roles.remove,
        'addselfassignable': roles.add_self_assignable,
        'asar': roles.add_self_assignable,
        'removeselfassignable': roles.remove_self_assignable,
        'rsar': roles.remove_self_assignable
    },
    data_cruncher.data.get_prefix('custom_reactions'): {
        'add': custom_reactions.add
    }
    # data_cruncher.data.get_prefix('currency'): currency_cmd,
    # data_cruncher.data.get_prefix('custom_reactions'): custom_reaction_cmd,
    # data_cruncher.data.get_prefix('hugemoji'): hugemoji_cmd
}


async def handle_message(msg):
    try:
        reply_func = replies.get(msg.content[:1]).get(msg.content[1:].split()[0])  # Only pass the Command Part

    except AttributeError:  # NoneType object has no attribute get blah blah blah, means no command found
        return
    if msg.author.id == 226612862620008448:  # message by bot itself, for safety
        return
    elif reply_func:  # Check if Command exists
        try:
            reply = await reply_func(msg)
        except TypeError as e:
            print(e)

            # Delete Reply after time, if set


async def custom_reaction_cmd(msg):
    msg.content = msg.content[1:]
    if msg.content.startswith('add') and msg.content[4:7] != 'add':  # the famous !add add
        try:
            if len(msg.content.split()[2:]) <= 1:
                await embeds.desc_only(msg.channel, 'Too little content for a Custom Reaction!')
                return
            data_cruncher.data.add_custom_reaction(msg.guild.id, msg.content.split()[1],
                                                   ' '.join(msg.content.split()[2:]), msg.author.name)
        except IndexError:
            return
        await embeds.desc_only(msg.channel, f'Added new Reaction called {msg.content.split()[1]}.')
        await msg.delete()

    elif msg.content == 'meow':
        link = json.load(urllib.request.urlopen('http://random.cat/meow'))['file']
        await embeds.img_only(msg.channel, link)
        await msg.delete()

    elif msg.content == 'woof':
        url = requests.get('https://api.giphy.com/v1/gifs/random?'
                           'api_key=dc6zaTOxFJmzC&tag=dog').json()['data_cruncher.data']['image_original_url']
        await embeds.img_only(msg.channel, f'{url}')
        await msg.delete()

    elif msg.content.startswith('listall'):
        custom_reactions = data_cruncher.data.get_all_custom_reactions_on_guild(msg.guild.id)
        if custom_reactions is None:
            await embeds.desc_only(msg.channel, 'Sorry, no Quotes were found for this Server.')
        else:
            await reactions.create_custom_reaction_embed(f'- All Custom Reactions on {msg.guild.name} - ',
                                                         custom_reactions, msg.channel,
                                                         'https://lh3.googleusercontent.com/'
                                                         'BvIDv_HYH8HnHubWn_lle2eC5lm5lY3kAGI'
                                                         'kFniSk8x_SDpbUr0dlNTe6P6j_C8f4cSmH-d'
                                                         '0rtuSlUU=w1441-h740')
        await msg.delete()

    else:
        try:
            reaction = data_cruncher.data.get_custom_reaction(msg.guild.id, msg.content.split()[0])
        except IndexError:
            pass
        else:
            if reaction is None:
                pass
            elif reaction[0].startswith('http'):  # Properly Embed Links to GIF, Images etc.
                await embeds.img_with_footer(msg.channel, reaction[0], f'Added by {reaction[1]}', reaction[2])
                await msg.delete()
            elif reaction[0] != '':
                await embeds.desc_with_footer(msg.channel, reaction[0], f'Added by {reaction[1]}', reaction[2])
                await msg.delete()


async def hugemoji_cmd(msg):
    # Match Emoji ID with RegEx
    emoji_id = re.search('[0-9]+', msg.content)
    # Make sure it also works when there's a number in the ID!
    try:
        if len(emoji_id.group(0)) == 1:
            emoji_id = re.search('[0-9]+', msg.content[msg.content.find(emoji_id.group(0)) + 1:])
    except AttributeError:
        await embeds.desc_only(msg.channel, 'Sorry, something went wrong.')
    else:
        await embeds.img_only(msg.channel, f'https://cdn.discordapp.com/emojis/{emoji_id.group(0)}.png')
    await msg.delete()



print('done.')
