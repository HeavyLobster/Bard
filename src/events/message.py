import asyncio
import json
import re
import urllib

import discord
import requests

from src.events import reactions
from src.util import data_cruncher
from src.util import embeds

print('Loading Message Event Handler... ', end='')

data = data_cruncher.data


async def handle_message(msg):
    if msg.author.id == 226612862620008448:  # message by bot itself
        return

    elif msg.author.id == data.get_owner()[0] and msg.content.startswith('!ttwitch'):
        # evaluation command for me
        try:
            await embeds.desc_only(msg.channel, eval(msg.content[5:]))
        except (TypeError, NameError, AttributeError) as e:
            response = await embeds.desc_only(msg.channel, str(e))
            await asyncio.sleep(2)
            await response.delete()
        await msg.delete()

    elif msg.content.startswith(data.get_prefix('administration')):
        await administration_cmd(msg)

    elif msg.content.startswith(data.get_prefix('roles')):
        await role_cmd(msg)

    elif msg.content.startswith(data.get_prefix('currency')):
        await currency_cmd(msg)

    elif msg.content.startswith(data.get_prefix('custom_reactions')):
        await custom_reaction_cmd(msg)

    elif msg.content.startswith(data.get_prefix('hugemoji')):
        await hugemoji_cmd(msg)

    return msg.content


async def administration_cmd(msg):
    msg.content = msg.content[1:]
    if msg.guild.id in data.get_role_servers() \
            and msg.author.id not in data.get_moderators_and_above(msg.guild.id):  # Moderator and above Commands
        return

    if msg.guild.id in data.get_role_servers() \
            and msg.author.id not in data.get_admins_and_above(msg.guild.id):  # Admin and above Commands
        return

    if msg.content.startswith('addmod'):
        try:
            data.add_moderator(msg.guild.id, msg.mentions[0].id)
        except IndexError:
            await embeds.desc_only(msg.channel, 'Couldn\'t add Moderator, no Member specified.')
        else:
            await embeds.desc_only(msg.channel, f'Added {str(msg.mentions[0])} as Moderator for this Server.')

    elif msg.content.startswith('removemod') or msg.content.startswith('rmmod'):
        try:
            success = data.remove_moderator(msg.guild.id, msg.mentions[0].id)
        except IndexError:
            await embeds.desc_only(msg.channel, 'Couldn\'t remove Moderator, no Member specified.')
        else:
            if success is None:
                await embeds.desc_only(msg.channel, 'No User Configuration for this Server present, can\'t remove.')
            elif not success:
                await embeds.desc_only(msg.channel, f'Couldn\'t find {str(msg.mentions[0].id)} in Moderators.')
            else:
                data.remove_moderator(msg.guild.id, msg.mentions[0].id)
                await embeds.desc_only(msg.channel, f'Removed {str(msg.mentions[0])} from Moderators '
                                                    f'for this Server.')

    if msg.author.id != data.get_owner()[0]:  # Owner-Only Commands
        return

    if msg.content.startswith('addadmin'):
        try:
            data.add_administrator(msg.guild.id, msg.mentions[0].id)
        except IndexError:
            await embeds.desc_only(msg.channel, 'Couldn\'t add Administrator, no Member specified.')
        else:
            await embeds.desc_only(msg.channel, f'Added {str(msg.mentions[0])} as Administrator for this Server.')

    elif msg.content.startswith('removeadmin') or msg.content.startswith('rmadmin'):
        try:
            success = data.remove_administrator(msg.guild.id, msg.mentions[0].id)
        except IndexError:
            await embeds.desc_only(msg.channel, 'Couldn\'t remove Administrator, no Member specified.')
        else:
            if success is None:
                await embeds.desc_only(msg.channel, 'No User Configuration for this Server present, can\'t remove.')
            elif not success:
                await embeds.desc_only(msg.channel, f'Couldn\'t find {str(msg.mentions[0].id)} in Administrators.')
            else:
                data.remove_administrator(msg.guild.id, msg.mentions[0].id)
                await embeds.desc_only(msg.channel, f'Removed {str(msg.mentions[0])} from Administrators '
                                                    f'for this Server.')


async def role_cmd(msg):
    # i wrote this at 2 AM in the morning, don't judge
    msg.content = msg.content[1:]

    async def self_assigning_enabled():
        self_assigning_roles_enabled = data.get_role_self_assigning_state(msg.guild.id)
        if self_assigning_roles_enabled is None:
            await embeds.desc_only(msg.channel, 'There are no self-assignable Roles for this Server.')
            return False
        elif not self_assigning_roles_enabled:
            await embeds.desc_only(msg.channel, 'Self-Assigning and Removing Roles is '
                                                'currently disabled on this Server.')
            return False
        return True

    async def get_role_by_name(name):
        return discord.utils.find(lambda r: r.name == (' '.join(name) if type(name) is list else name), msg.guild.roles)

    async def get_comma_separated_roles():
        comma_separated_roles = list()
        msg.content = msg.content[5:]  # Ignore the command part
        for single_role in msg.content.split(', '):
            role_name = single_role
            single_role = await get_role_by_name(single_role)
            comma_separated_roles.append([single_role, role_name])
        return comma_separated_roles
    role = await get_role_by_name(msg.content.split()[1:])
    if msg.content.startswith('assign'):
        if not await self_assigning_enabled():
            return
        elif data.get_self_assignable_roles(msg.guild.id) is None:
            await embeds.desc_only(msg.channel, 'There are no self-assignable Roles for this Server.')
        elif role is None:
            await embeds.desc_only(msg.channel, 'That Role was not found.')
        elif role.id not in data.get_self_assignable_roles(msg.guild.id):
            await embeds.desc_only(msg.channel, 'That Role is not self-assignable.')
        else:
            await msg.author.add_roles(role)
            await embeds.desc_only(msg.channel, f'Gave you the `{role.name}` Role!')

    elif msg.content.startswith('remove') or msg.content.startswith('unassign'):
        if not await self_assigning_enabled():
            return
        elif not data.get_role_self_assigning_state(msg.guild.id):
            await embeds.desc_only(msg.channel, 'You can\'t remove not self-assignable Roles.')
        else:
            await msg.author.remove_roles(role)
            await embeds.desc_only(msg.channel, f'Removed your `{role.name}` Role!')

    elif msg.content.startswith('roles') or msg.content.startswith('lsar'):  # list self-assignable roles
        if await self_assigning_enabled():
            roles = data.get_self_assignable_roles(msg.guild.id)
            if roles is None:
                await embeds.desc_only(msg.channel, 'There are no self-assignable Roles for this Server.')
            elif len(roles) >= 1:
                role_names = [discord.utils.find(lambda r: r.id == role_id, msg.guild.roles) for role_id in roles]
                await embeds.desc_only(msg.channel, f'**There\'s a total of {len(role_names)} self-assignable '
                                                    f'Roles:**\n {", ".join((x.name for x in role_names))}')

    elif str(msg.guild.id) in data.get_role_servers() \
            and msg.author.id not in data.get_moderators_and_above(msg.guild.id):  # Moderator and above Commands
        return

    elif msg.content.startswith('asar'):  # Add self-assignable Role(s)
        updated_roles = []
        for local_single_role in await get_comma_separated_roles():
            if local_single_role[0] is None:
                await embeds.desc_only(msg.channel, f'Couldn\t find Role `{local_single_role[1]}` on this Server.')
            elif str(msg.guild.id) not in data.get_role_servers():
                await embeds.desc_only(msg.channel, 'There are no self-assignable Roles set on this Server.')
            elif local_single_role[0].id in data.get_self_assignable_roles(msg.guild.id):
                await embeds.desc_only(msg.channel, f'`{local_single_role[1]}` is already self-assignable.')
            else:
                data.add_self_assignable_role(msg.guild.id, local_single_role[0].id)
                updated_roles.append(local_single_role[0].name)
        if len(updated_roles) > 1:
            await embeds.desc_only(msg.channel, '**The following Roles are now self-assignable:** \n'
                                                f'{", ".join(updated_roles)}')
        elif len(updated_roles) == 1:
            await embeds.desc_only(msg.channel, f'Role `{local_single_role[0].name}` is now self-assignable.')

    elif msg.content.startswith('rsar'):  # Remove self-assignable Role
        success = data.remove_self_assignable_role(msg.guild.id, role.id)
        if success is None:
            await embeds.desc_only(msg.channel, 'There are no self-assignable Roles for this Server.')
        elif not success:
            await embeds.desc_only(msg.channel, 'Role is not self-assignable, can\'t remove.')
        elif success:
            await embeds.desc_only(msg.channel, f'Role `{role.name} is no longer self-assignable.')

    if str(msg.guild.id) in data.get_role_servers() \
            and msg.author.id not in data.get_admins_and_above(msg.guild.id):  # Admin and Above commands
        return

    if msg.content == 'switch':
        new_state = data.switch_role_self_assigning_state(msg.guild.id)
        if new_state is None:
            await embeds.desc_only(msg.channel, 'No self-assignable Roles set for this Server.')
        else:
            await embeds.desc_only(msg.channel, f'Self-Assigning Roles is now '
                                                f'**{"enabled" if new_state else "disabled"}**.')
            # await msg.delete()


async def currency_cmd(msg):
    pass


async def custom_reaction_cmd(msg):
    msg.content = msg.content[1:]
    if msg.content.startswith('add') and msg.content[4:7] != 'add':  # the famous !add add
        try:
            if len(msg.content.split()[2:]) <= 1:
                await embeds.desc_only(msg.channel, 'Too little content for a Custom Reaction!')
                return
            data.add_custom_reaction(msg.guild.id, msg.content.split()[1],
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
                           'api_key=dc6zaTOxFJmzC&tag=dog').json()['data']['image_original_url']
        await embeds.img_only(msg.channel, f'{url}')
        await msg.delete()

    elif msg.content.startswith('listall'):
        custom_reactions = data.get_all_custom_reactions_on_guild(msg.guild.id)
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
            reaction = data.get_custom_reaction(msg.guild.id, msg.content.split()[0])
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
