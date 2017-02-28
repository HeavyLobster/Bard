from src.util.data_cruncher import data


def check_if_owner(func):
    def func_wrapper(msg):
        if msg.author.id in data.get_owner():
            return func(msg)

    return func_wrapper


def check_if_admin(func):
    def func_wrapper(msg):
        if msg.author.id in data.get_admins_and_above(msg.guild.id):
            return func(msg)

    return func_wrapper


def check_if_mod(func):
    def func_wrapper(msg):
        if msg.author.id in data.get_moderators_and_above(msg.guild.id):
            return func(msg)

    return func_wrapper
