import discord

from src import bot
from src.util import embeds, permission_checks
from src.util.data_cruncher import data


@permission_checks.check_if_mod
async def kick(msg):
    if not len(msg.mentions):
        return await embeds.desc_only(msg.channel, 'No User specified. Kick not possible.')
    else:
        try:
            await msg.guild.kick(msg.mentions[0])
            if len(msg.content.split()) >= 3:  # if a kick message is specified
                await msg.mentions[0].send(f'**You have been kicked from {msg.guild.name}, reason:** \n'
                                           f'{" ".join(msg.content.split()[2:])}')
        except (discord.errors.Forbidden, discord.errors.HTTPException) as err:
            return await embeds.desc_only(msg.channel, f'**Can\'t kick**: {err}.')
        return await embeds.desc_only(msg.channel, 'Gone!')


@permission_checks.check_if_mod
async def ban(msg):
    if not len(msg.mentions):
        return await embeds.desc_only(msg.channel, 'No User specified. Ban not possible.')
    else:
        try:
            await msg.guild.ban(msg.mentions[0])
            if len(msg.content.split()) >= 3:  # if a ban message is specified
                await msg.mentions[0].send(f'**You have been kicked from {msg.guild.name}, reason:** \n'
                                           f'{" ".join(msg.content.split()[2:])}')
        except (discord.errors.Forbidden, discord.errors.HTTPException) as err:
            return await embeds.desc_only(msg.channel, f'**Can\’t ban:** {err}.')
        return await embeds.desc_only(msg.channel, 'Gone!')


@permission_checks.check_if_admin
async def change_activity(msg):
    # TODO: add new config file for global settings like the last activity etc
    try:
        new_activity = msg.content.split()[1:]
    except IndexError:
        return await embeds.desc_only(msg.channel, 'No new Activity specified.')
    else:
        new_game = discord.Game()
        new_game.name = ' '.join(new_activity)
        await bot.client.change_presence(game=new_game)
        return await embeds.desc_only(msg.channel, 'Changed Activity.')


@permission_checks.check_if_admin
async def set_log_channel(msg):
    if data.set_log_channel(msg.guild.id, msg.channel.id):
        return await embeds.desc_only(msg.channel, 'Log Channel set to **this channel**.')
    else:
        return await embeds.desc_only(msg.channel, 'Failed to set Log channel.')


@permission_checks.check_if_admin
async def add_mod(msg):
    # issue: if multiple roles in the owner - admin - mod hierarchy are assigned, the topmost must be removed first
    if not len(msg.mentions):  # No User Mentioned
        return await embeds.desc_only(msg.channel, f'No User specified, cannot add Moderator.')
    elif msg.mentions[0].id in data.get_moderators_and_above(msg.guild.id):
        return await embeds.desc_only(msg.channel, f'**{msg.mentions[0].name}** is already a Moderator.')
    else:
        data.add_moderator(msg.guild.id, msg.mentions[0].id)
        print(f'Added {msg.mentions[0].name} (ID: {msg.mentions[0].id}) to Moderators for Guild {msg.guild.name}.')
        return await embeds.desc_only(msg.channel, f'Added **{msg.mentions[0].name}** to Moderators.')


@permission_checks.check_if_admin
async def remove_mod(msg):
    if not len(msg.mentions):
        return await embeds.desc_only(msg.channel, 'No User specified, cannot remove Moderator.')
    elif msg.mentions[0].id not in data.get_moderators_and_above(msg.guild.id):
        return await embeds.desc_only(msg.channel, f'**{msg.mentions[0].name}** is not a Moderator.')
    else:
        data.remove_moderator(msg.guild.id, msg.mentions[0].id)
        print(f'Removed {msg.mentions[0].name} (ID: {msg.mentions[0].id}) from Moderators for Guild {msg.guild.name}.')
        return await embeds.desc_only(msg.channel, f'Removed **{msg.mentions[0].name}** from Moderators.')


@permission_checks.check_if_admin
async def shutdown():
    await bot.client.close()


@permission_checks.check_if_owner
async def add_admin(msg):
    if not len(msg.mentions):
        return await embeds.desc_only(msg.channel, 'No User specified, cannot add Administrator.')
    elif msg.mentions[0].id in data.get_admins_and_above(msg.guild.id):
        return await embeds.desc_only(msg.channel, f'**{msg.mentions[0].name}** is already an Administrator.')
    else:
        data.add_administrator(msg.guild.id, msg.mentions[0].id)
        print(f'Added {msg.mentions[0].name} (ID: {msg.mentions[0].id} to Administrators for Guild {msg.guild.name}.')
        return await embeds.desc_only(msg.channel, f'Added **{msg.mentions[0].name}** to Administrators.')


@permission_checks.check_if_owner
async def remove_admin(msg):
    if not len(msg.mentions):
        return await embeds.desc_only(msg.channel, 'No User specified, cannot remove Administrator.')
    elif msg.mentions[0].id not in data.get_admins_and_above(msg.guild.id):
        return await embeds.desc_only(msg.channel, f'**{msg.mentions[0].name}** is not an Administrator.')
    else:
        data.remove_administrator(msg.guild.id, msg.mentions[0].id)
        print(f'Removed {msg.mentions[0].name} (ID: {msg.mentions[0].id}) from Administrators '
              f'for Guild {msg.guild.name}.')
        return await embeds.desc_only(msg.channel, f'Removed **{msg.mentions[0].name}** from Administrators.')
