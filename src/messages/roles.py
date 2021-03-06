import cassiopeia
import discord
from src.events import message
from src.util import embeds, checks, lolapi
from src.util.data_cruncher import data

from src import bot


async def _perform_checks(msg: discord.Message):
    status = data.get_role_self_assigning_state(msg.guild.id)
    if status is None:  # No Roles found
        return await embeds.desc_only(msg.channel, 'There are no self-assignable Roles set for this Server.')
    elif not status:  # Self-Assigning Disabled
        return await embeds.desc_only(msg.channel, 'Self-Assigning Roles is currently disabled for this Server.')
    elif len(msg.content.split()) < 2:  # No Role specified
        return await embeds.desc_only(msg.channel, 'No Role specified, can\'t modify.')
    role = _get_role_by_name(' '.join(msg.content.split()[1:]), msg.guild.roles)
    if role is None:
        return await embeds.desc_only(msg.channel, f'Couldn\'t find **\'{" ".join(msg.content.split()[1:])}\'** '
                                                   f'on this Server.')
    return role


async def log(guild_id: int, log_message: str):
    try:
        await embeds.desc_only(bot.client.get_channel(data.get_log_channel(guild_id)), log_message)
    except AttributeError:
        pass


def get_comma_separated_roles(msg):
    comma_separated_roles = list()
    msg.content = msg.content[5:]  # Ignore the command part
    for single_role in msg.content.split(', '):
        role_name = single_role.lstrip()
        single_role = _get_role_by_name(role_name, msg.guild.roles)
        comma_separated_roles.append([single_role, role_name])
    return comma_separated_roles


def _get_role_by_name(name, guild_roles):
    return discord.utils.find(lambda r: r.name == name, guild_roles)


async def in_role(msg):
    """
    Shows the count and a list of all members that are in the role that was looked up.
    
    :param msg: The Message invoking the Command 
    :return: A discord.Message instance representing the Bot's response
    """
    if len(msg.content.split()) < 2:
        return await embeds.desc_only(msg.channel, 'You need to name the Role for which you would like to lookup its '
                                                   'members to use this Command!', discord.Color.red())
    searched_role = ' '.join(msg.content.split()[1:])
    searched_role_lower = searched_role.lower()
    members_with_role = []
    if searched_role_lower not in (role.name.lower() for role in msg.guild.roles):
        return await embeds.desc_only(msg.channel, f'This Server does not have any Role named {searched_role}.',
                                      discord.Color.red())
    response = await embeds.desc_only(msg.channel, 'Finding Members...')
    for member in msg.guild.members:
        for role in member.roles:
            if role.name.lower() == searched_role_lower:
                members_with_role.append(member)
    await response.delete()
    members_with_role_as_string = ', '.join(x.name for x in members_with_role)
    if len(members_with_role_as_string) > 2000:
        members_with_role_as_string = 'There are too many players to list them here.'
    return await embeds.title_and_desc(msg.channel, f'- Members with Role "{searched_role}" -',
                                       f'{members_with_role_as_string}\n\n'
                                       f'**{len(members_with_role)} total**.')

async def assign(msg):
    role = await _perform_checks(msg)
    if not isinstance(role, discord.Role):  # checks didn't pass, it sent a warning instead of the Role
        return role

    if role in msg.author.roles[1:]:
        return await embeds.desc_only(msg.channel, 'You already have that Role assigned.')
    elif role.id not in data.get_self_assignable_roles(msg.guild.id):
        return await embeds.desc_only(msg.channel, 'That Role is not self-assignable.')
    else:
        try:
            await msg.author.add_roles(role)
        except discord.errors.Forbidden as err:
            return await embeds.desc_only(msg.channel, f'Can\'t assign: {err}.')
    await log(msg.guild.id, f'**{str(msg.author)}** self-assigned the `{role.name}` Role.')
    return await embeds.desc_only(msg.channel, f'Gave you the **{role.name}** Role!')


async def remove(msg):
    role = await _perform_checks(msg)
    if not isinstance(role, discord.Role):
        return role  # why am I returning this
    try:
        if role.id not in data.get_self_assignable_roles(msg.guild.id):
            return await embeds.desc_only(msg.channel, 'That Role is not self-assignable.')
        elif role in msg.author.roles[1:]:  # first element is always @everyone, so skip it
            await msg.author.remove_roles(role)
        else:
            return await embeds.desc_only(msg.channel, 'You don\'t have that Role assigned.')
    except discord.errors.Forbidden as err:
        return await embeds.desc_only(msg.channel, f'Can\'t remove: {err}.')
    await log(msg.guild.id, f'**{str(msg.author)}** self-removed the `{role.name}` Role.')
    return await embeds.desc_only(msg.channel, f'Removed **{role.name}** from you!')


async def list_self_assignable(msg):
    if not data.get_role_self_assigning_state(msg.guild.id):
        return await embeds.desc_only(msg.channel, 'Self-Assigning Roles is **disabled** for this Server.')
    roles = data.get_self_assignable_roles(msg.guild.id)
    if roles is None:
        return await embeds.desc_only(msg.channel, 'There are no self-assignable Roles for this Server.')
    elif len(roles) >= 1:
        role_names = [discord.utils.find(lambda r: r.id == role_id, msg.guild.roles) for role_id in roles]
        return await embeds.desc_only(msg.channel, f'**There\'s a total of {len(role_names)} self-assignable '
                                                   f'Roles:**\n {", ".join((x.name for x in role_names))}')


@checks.is_mod
async def add_self_assignable(msg):
    roles = get_comma_separated_roles(msg)
    updated_roles = []
    for role in roles:
        if role[0] is None:
            await embeds.desc_only(msg.channel, f'Couldn\t find `{role[1]}`.')
        elif role[0].position >= msg.guild.me.top_role.position:
            await embeds.desc_only(msg.channel, f'The Role `{role[1]}` stands higher or equal to mine, '
                                                f'can\'t make self-assignable.')
        elif data.get_self_assignable_roles(msg.guild.id) is not None \
                and role[0].id in data.get_self_assignable_roles(msg.guild.id):
            await embeds.desc_only(msg.channel, f'`{role[1]}` is already self-assignable.')
        else:
            data.add_self_assignable_role(msg.guild.id, role[0].id)
            updated_roles.append(role[0].name)
    if len(updated_roles) > 1:
        return await embeds.desc_only(msg.channel, '**The following Roles are now self-assignable:** \n'
                                                   f'{", ".join(updated_roles)}')
    elif len(updated_roles) == 1:
        return await embeds.desc_only(msg.channel, f'Role `{role[0].name}` is now self-assignable.')


@checks.is_mod
async def remove_self_assignable(msg):
    role = await _perform_checks(msg)
    if not isinstance(role, discord.Role):
        return role

    data.remove_self_assignable_role(msg.guild.id, role.id)
    return await embeds.desc_only(msg.channel, f'Removed **{role.name}** from self-assignable Roles!')


@checks.is_admin
async def switch_self_assignment(msg):
    new_state = data.switch_role_self_assigning_state(msg.guild.id)
    if new_state is None:
        await embeds.desc_only(msg.channel, 'No self-assignable Roles set for this Server.')
    else:
        await embeds.desc_only(msg.channel, f'Self-Assigning Roles is now '
                                            f'**{"enabled" if new_state else "disabled"}**.')


async def get_league_role(msg):
    server = msg.content.split()[1]
    name = ' '.join(msg.content.split()[2:])

    async def add_league_role_with_log(msg, role_name: str):
        role = _get_role_by_name(role_name, msg.guild.roles)
        if role in msg.author.roles[1:]:
            return await embeds.desc_only(msg.channel, 'You already have a matching Role.')
        else:
            await msg.author.add_roles(role)
            await log(msg.guild.id, f'Gave **{str(msg.author)}** the `{role.name}` Role for `{name}` on `{server}`.')
            return await embeds.desc_only(msg.channel, f'Gave you the **{role.name}** Role!')

    try:
        champion_points = lolapi.get_mastery_points(name, server)
    except ValueError:
        return await embeds.desc_only(msg.channel, 'Some error occured, keep in mind: it\'s .getmyrole <server> <name>')
    except cassiopeia.type.api.exception.APIError:
        return await embeds.desc_only(msg.channel, 'Riot Games API returned an API Error trying to fetch your score.')
    except IndexError:
        return await embeds.desc_only(msg.channel, 'Please use the command like this: .getmyrole <server> <name>')
    else:
        if champion_points < 50000:
            await embeds.desc_only(msg.channel, 'Sadly, you don\'t meet the requirements for any mastery-related role.'
                                                ' However, I have good news:')
            return await add_league_role_with_log(msg, 'Aspiring Bard')
        elif 50000 <= champion_points < 100000:
            return await add_league_role_with_log(msg, '50k')
        elif 100000 <= champion_points < 250000:
            return await add_league_role_with_log(msg, '100k')
        elif 250000 <= champion_points < 500000:
            return await add_league_role_with_log(msg, '250k')
        elif 500000 <= champion_points < 750000:
            return await add_league_role_with_log(msg, '500k')
        elif 750000 <= champion_points < 1000000:
            return await add_league_role_with_log(msg, '750k')
        elif 1000000 <= champion_points < 1500000:
            return await add_league_role_with_log(msg, '1M')
        elif champion_points >= 1500000:
            return await add_league_role_with_log(msg, '1.5M')

