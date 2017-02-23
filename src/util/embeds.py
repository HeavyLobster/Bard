import datetime
import discord.embeds
from time import strptime, mktime


def datetime_from_struct_time(struct_time):
    try:
        return datetime.datetime.fromtimestamp(mktime(strptime(struct_time, '%Y-%m-%d %H:%M:%S')))
    except (ValueError, TypeError):  # throws errors but still works I guess
        pass


async def desc_only(channel, desc: str):
    embed = discord.Embed()
    embed.description = desc
    await channel.send(embed=embed)


async def img_only(channel, link: str):
    embed = discord.Embed()
    embed.set_image(url=link)
    await channel.send(embed=embed)


async def desc_with_footer(channel, desc: str, footer: str, timestamp: str):
    embed = discord.Embed()
    embed.description = desc
    embed.set_footer(text=footer)
    try:
        embed.timestamp = datetime_from_struct_time(timestamp)
    except TypeError:
        pass  # hurr durr type error
    await channel.send(embed=embed)


async def img_with_footer(channel, link: str, footer: str, timestamp: str):
    embed = discord.Embed()
    embed.set_image(url=link)
    embed.set_footer(text=footer)
    embed.timestamp = datetime_from_struct_time(timestamp)
    await channel.send(embed=embed)
