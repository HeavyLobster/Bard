import datetime
import discord.embeds
from time import strptime, mktime


def datetime_from_struct_time(struct_time):
    try:
        return datetime.datetime.fromtimestamp(mktime(strptime(struct_time, '%Y-%m-%d %H:%M:%S')))
    except (ValueError, TypeError):  # throws errors but still works I guess
        pass


async def desc_only(channel, desc: str, color: discord.Colour=None):
    embed = discord.Embed()
    embed.description = desc
    if color is not None:
        embed.colour = color
    try:
        return await channel.send(embed=embed)
    except discord.errors.HTTPException:
        pass


async def title_and_desc(channel, title: str, desc: str, color: discord.Colour=None):
    embed = discord.Embed()
    embed.title = title
    embed.description = desc
    if color is not None:
        embed.colour = color
    try:
        return await channel.send(embed=embed)
    except discord.errors.HTTPException:
        pass

async def red_desc(channel, desc: str):
    embed = discord.Embed()
    embed.description = desc
    try:
        return await channel.send(embed=embed)
    except discord.errors.HTTPException:
        pass


async def img_only(channel, link: str):
    embed = discord.Embed()
    embed.set_image(url=link)
    try:
        return await channel.send(embed=embed)
    except discord.errors.HTTPException:
        pass

async def desc_with_img(channel, desc: str, link: str, footer: str=''):
    """
    Send an Embed with a Description and Image.
    
    :param channel: The Channel in which to send the Embed
    :param desc: The Description that the Embed should contain
    :param link: A Link to the Image that should be displayed
    :param footer: An optional Footer to be put at the Bottom of the Embed
    :return: A discord.Message Object containing the sent Embed, or None if sending it failed.
    """
    embed = discord.Embed()
    embed.description = desc
    embed.set_image(url=link)
    if footer != '':
        embed.set_footer(text=footer)
    try:
        return await channel.send(embed=embed)
    except discord.errors.HTTPException as e:
        print(e)
        return None

async def video_only(channel, link: str):
    embed = discord.Embed()
    embed.video.url = link
    try:
        return await channel.send(embed=embed)
    except discord.errors.HTTPException:
        print(f'Failed to send Video with link: {link}')


async def desc_with_footer(channel, desc: str, footer: str, timestamp: str):
    embed = discord.Embed()
    embed.description = desc
    embed.set_footer(text=footer)
    try:
        embed.timestamp = datetime_from_struct_time(timestamp)
    except TypeError:
        pass  # hurr durr type error
    return await channel.send(embed=embed)


async def img_with_footer(channel, link: str, footer: str, timestamp):
    embed = discord.Embed()
    embed.set_image(url=link)
    embed.set_footer(text=footer)
    embed.timestamp = datetime_from_struct_time(timestamp)
    return await channel.send(embed=embed)


async def url_with_desc(channel, title: str, url: str, desc: str):
    embed = discord.Embed()
    embed.url = url
    embed.description = desc
    try:
        return await channel.send(embed=embed)
    except discord.errors.HTTPException:
        print(f'Couldn\'t send Embed with Link {url}, description: {desc}')
