from src.messages import administration, custom_reactions, currency, roles
from src.util import checks, data_cruncher

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
        'setlog': administration.set_log_channel,
        'initlog': administration.set_log_channel,
        'shutdown': administration.shutdown,
        'kill': administration.shutdown,
        'kick': administration.kick,
        'purge': administration.purge,
        'prune': administration.purge,
        'clear': administration.purge,
        'ban': administration.ban
    },
    data_cruncher.data.get_prefix('roles'): {
        'assign': roles.assign,
        'iam': roles.assign,
        'remove': roles.remove,
        'rm': roles.remove,
        'iamn': roles.remove,
        'getmyrole': roles.get_league_role,
        'leaguerole': roles.get_league_role,
        'roles': roles.list_self_assignable,
        'lsar': roles.list_self_assignable,
        'addselfassignable': roles.add_self_assignable,
        'asar': roles.add_self_assignable,
        'removeselfassignable': roles.remove_self_assignable,
        'rsar': roles.remove_self_assignable,
        'switch': roles.switch_self_assignment
    },
    data_cruncher.data.get_prefix('custom_reactions'): {
        'add': custom_reactions.add,
        'meow': custom_reactions.meow,
        'woof': custom_reactions.woof,
        'viewall': custom_reactions.build_list,
        'showall': custom_reactions.build_list,
        'hm': custom_reactions.hugemoji,
        'help': custom_reactions.help
    },
    data_cruncher.data.get_prefix('currency'): {
        'c': currency.get_money,
        'chime': currency.get_money,
        'chimes': currency.get_money,
        'chance': currency.get_chance,
        'give': currency.give_money,
        'switch': currency.toggle_cg,
        'toggle': currency.toggle_cg,
        'cg': currency.toggle_cg,
        'grant': currency.add_money,
        'take': currency.remove_money
    }
}


@checks.is_in_guild
async def handle_message(msg):
    """
    Handles a Message passed through various Checks. The Bot only responds on Guilds.
    
    Tries to get a function to reply with as saved in the dictionary shown above.
    If this fails, it will return. Otherwise, it continues to check whether it started with a known prefix
    - in this case, this is the prefix for Custom Reactions. It then tries to obtain a Custom Reaction.
    If it found one, it deletes the Message invoking the Command. Otherwise, nothing happens.
    After this process, the message is passed to the Currency Module which uses non-Commands as triggers for 
    potential Currency spawning. The Commands exposed by the Module are specified in the Dictionary above.
    
    :param msg: A discord.Message Object with which this Function should actuate. 
    """
    if msg.author.id == 226612862620008448:  # message by bot itself, for safety
        return

    valid_prefix_commands = replies.get(msg.content[:1], None)
    if valid_prefix_commands is not None:  # No message of interest
        try:
            valid_response = valid_prefix_commands.get(msg.content[1:].split()[0])
        except IndexError:  # somebody sent a single character for some reason
            pass
        else:
            if valid_response is None and msg.content[:1] == data_cruncher.data.get_prefix('custom_reactions'):
                if await custom_reactions.get_one(msg):
                    await msg.delete()
            elif valid_response is not None:
                reply = await valid_response(msg)
                # Delete reply after a set time
    else:
        await currency.generator(msg)


print('done.')
