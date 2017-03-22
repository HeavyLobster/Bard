import discord
from src.util.data_cruncher import data


def is_owner(func):
    def func_wrapper(msg):
        if msg.author.id in data.get_owner():
            return func(msg)

    return func_wrapper


def is_admin(func):
    def func_wrapper(msg):
        if msg.author.id in data.get_admins_and_above(msg.guild.id):
            return func(msg)

    return func_wrapper


def is_mod(func):
    def func_wrapper(msg):
        if msg.author.id in data.get_moderators_and_above(msg.guild.id):
            return func(msg)

    return func_wrapper


def is_in_guild(func):
    def func_wrapper(msg):
        if isinstance(msg.channel, discord.abc.GuildChannel):
            return func(msg)

    return func_wrapper
