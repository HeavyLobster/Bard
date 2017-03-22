import discord
from src.util import embeds, permission_checks
from src.util.data_cruncher import data

from src import bot


@permission_checks.check_if_mod
async def kick(msg):
    """
    Kick a mentioned User from the Guild.
    
    The User must be mentioned via @name#1337 so the Bot can obtain the Member object.
    It's also possible to specify an optional Kick Message that will be sent by the Bot via DM to the kicked User.
     
    :param msg: The Message invoking the Command
    :return: A discord.Message Object containing the resulting Feedback from the Bot.
    """
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
    """
    Ban a mentioned User from the Guild.

    The User must be mentioned via @name#1337 so the Bot can obtain the Member object.
    It's also possible to specify an optional Ban Message that will be sent by the Bot via DM to the banned User.

    :param msg: The Message invoking the Command
    :return: A discord.Message Object containing the resulting Feedback from the Bot.
    """
    if not len(msg.mentions):
        return await embeds.desc_only(msg.channel, 'No User specified. Ban not possible.')
    else:
        try:
            await msg.guild.ban(msg.mentions[0])
            if len(msg.content.split()) >= 3:  # if a ban message is specified
                await msg.mentions[0].send(f'**You have been banned from {msg.guild.name}, reason:** \n'
                                           f'{" ".join(msg.content.split()[2:])}')
        except (discord.errors.Forbidden, discord.errors.HTTPException) as err:
            return await embeds.desc_only(msg.channel, f'**Can\’t ban:** {err}.')
        return await embeds.desc_only(msg.channel, 'Gone!')


@permission_checks.check_if_mod
async def purge(msg):
    """
    Purge a specified amount of Messages.
    
    It's possible to either purge a given amount of Messages, or by also mentioning a User searching for Messages
    of the User in the specified amount of Messages.
    
    :param msg: The Message invoking the Command
    :return: A discord.Message Object containing the response from the Bot. Most likely the amount of purged Messages.
    """
    try:
        amount = int(msg.content.split()[1])
    except (ValueError, IndexError):
        amount = 20
    if len(msg.mentions) == 1:
        purge_this_user = msg.mentions[0]
    try:
        def check_if_wanted_user(m):
            return m.author == purge_this_user

        if 'purge_this_user' in locals():
            deleted = await msg.channel.purge(limit=amount, check=check_if_wanted_user)
        else:
            deleted = await msg.channel.purge(limit=amount)
        resp = f'Purged a total of **{len(deleted)} Messages**' \
               f'{"." if "purge_this_user" not in locals() else f" from **{purge_this_user.name}**."}'
        return await embeds.desc_only(msg.channel, resp)
    except discord.Forbidden:
        return await embeds.desc_only(msg.channel, f'I don\'t have the required Permissions to purge Messages.')
    except discord.HTTPException:
        return await embeds.desc_only(msg.channel, 'Got HTTP Exception trying to delete Messages.')


@permission_checks.check_if_admin
async def change_activity(msg):
    """
    Change the Activity, or also named "playing state", of the Bot.

    :param msg: The Message invoking the Command 
    :return: A discord.Message Object containing the response of the Bot.
    """
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
    """
    Set a Log Channel which is used to inform about various Events. 
    
    :param msg: The Message invoking the Command
    :return: A discord.Message Object containing the Response from the Bot indicating Success or Failure.
    """
    if data.get_log_channel(msg.guild.id) == msg.channel:
        return await embeds.desc_only(msg.channel, 'This already is the Log Channel for this Guild.')
    elif data.set_log_channel(msg.guild.id, msg.channel.id):
        return await embeds.desc_only(msg.channel, 'Log Channel set to **this channel**.')
    else:
        return await embeds.desc_only(msg.channel, 'Failed to set Log channel.')


@permission_checks.check_if_admin
async def add_mod(msg):
    """
    Add a Moderator for the Guild in which the Message was sent.
    
    Since Bard uses his own Permission Management System, this is necessary to authorize Users to use various Commands.
    Check the usage of the @permission_checks Decorator for knowing which Group can invoke which Command.
    
    :param msg: The Message invoking the Command 
    :return: A discord.Message Object containing the Response from the Bot indicating Success or Failure.
    """
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
    """
    Remove a Moderator for the Guild in which the Message was sent.
    
    :param msg: The Message invoking the Command 
    :return: A discord.Message Object containing the Response from the Bot indicating Success or Failure.
    """
    if not len(msg.mentions):
        return await embeds.desc_only(msg.channel, 'No User specified, cannot remove Moderator.')
    elif msg.mentions[0].id not in data.get_moderators_and_above(msg.guild.id):
        return await embeds.desc_only(msg.channel, f'**{msg.mentions[0].name}** is not a Moderator.')
    else:
        data.remove_moderator(msg.guild.id, msg.mentions[0].id)
        print(f'Removed {msg.mentions[0].name} (ID: {msg.mentions[0].id}) from Moderators for Guild {msg.guild.name}.')
        return await embeds.desc_only(msg.channel, f'Removed **{msg.mentions[0].name}** from Moderators.')


@permission_checks.check_if_admin
async def shutdown(msg):
    """
    Shutdown the Bot.
    
    :param msg: The Message invoking the Command. 
    :return: A discord.Message Object informing about the Bot shutting itself down.
    """
    await embeds.desc_only(msg.channel, '*emulates windows xp shutdown sound*')
    await bot.client.close()


@permission_checks.check_if_owner
async def add_admin(msg):
    """
    Add an Administrator for the Guild in which the Message was sent.

    Since Bard uses his own Permission Management System, this is necessary to authorize Users to use various Commands.
    Check the usage of the @permission_checks Decorator for knowing which Group can invoke which Command.

    :param msg: The Message invoking the Command 
    :return: A discord.Message Object containing the Response from the Bot indicating Success or Failure.
    """
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
    """
    Remove an Administrator for the Guild in which the Message was sent.

    :param msg: The Message invoking the Command 
    :return: A discord.Message Object containing the Response from the Bot indicating Success or Failure.
    """
    if not len(msg.mentions):
        return await embeds.desc_only(msg.channel, 'No User specified, cannot remove Administrator.')
    elif msg.mentions[0].id not in data.get_admins_and_above(msg.guild.id):
        return await embeds.desc_only(msg.channel, f'**{msg.mentions[0].name}** is not an Administrator.')
    else:
        data.remove_administrator(msg.guild.id, msg.mentions[0].id)
        print(f'Removed {msg.mentions[0].name} (ID: {msg.mentions[0].id}) from Administrators '
              f'for Guild {msg.guild.name}.')
        return await embeds.desc_only(msg.channel, f'Removed **{msg.mentions[0].name}** from Administrators.')
