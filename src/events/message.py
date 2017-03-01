from src.messages import administration, custom_reactions, roles
from src.util import data_cruncher

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
        'rsar': roles.remove_self_assignable
    },
    data_cruncher.data.get_prefix('custom_reactions'): {
        'add': custom_reactions.add,
        'meow': custom_reactions.meow,
        'woof': custom_reactions.woof,
        'viewall': custom_reactions.build_list,
        'showall': custom_reactions.build_list,
        'hm': custom_reactions.hugemoji
    }
    # data_cruncher.data.get_prefix('currency'): currency_cmd
}


async def handle_message(msg):
    try:
        reply_func = replies.get(msg.content[:1]).get(msg.content[1:].split()[0])  # Only pass the Command Part
    except (AttributeError, IndexError):  # NoneType object has no attribute get blah blah blah, means no command found
        return

    if not reply_func and msg.content[:1] == data_cruncher.data.get_prefix('custom_reactions'):
        try:

            if await custom_reactions.get_one(msg):
                await msg.delete()
            return
        except TypeError:  # auto-delete successfully grabbed custom reactions
            return

    if msg.author.id == 226612862620008448:  # message by bot itself, for safety
        return
    try:
        reply = await reply_func(msg)
    except TypeError:
        pass
        # Delete reply after time, if set


print('done.')
