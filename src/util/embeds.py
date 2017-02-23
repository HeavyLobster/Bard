import discord.embeds


def simple(text: str):
    embed = discord.Embed()
    embed.description = text
    return embed


def image(link: str):
    embed = discord.Embed()
    embed.set_image(url=link)
    return embed
