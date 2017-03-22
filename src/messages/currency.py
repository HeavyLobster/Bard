import discord
import random
from src.util.data_cruncher import data
from src.util import embeds, permission_checks


@permission_checks.check_if_admin
async def toggle_cg(msg):
    """
    Toggle Currency Generation in the Channel in which this Command was invoked.
    
    :param msg: The Message invoking the Command
    :return: A Message indicating whether it was successful or not
    """
    if not isinstance(msg.channel, discord.abc.GuildChannel):
        return await embeds.desc_only(msg.channel, 'This Command must be used on a Guild.')

    if msg.channel.id in data.get_currency_channels(msg.guild.id):
        data.remove_currency_channel(msg.guild.id, msg.channel.id)
        return await embeds.desc_only(msg.channel, 'Currency Generation is now **disabled** in this Channel.')

    data.add_currency_channel(msg.guild.id, msg.channel.id)
    return await embeds.desc_only(msg.channel, 'Currency Generation is now **enabled** in this Channel.')


async def generator(msg):
    """
    Generate Currency based on different Parameters and a bit of Magic.
    
    :param msg: The original Message 
    :return: 
    """
    if not isinstance(msg.channel, discord.abc.GuildChannel):
        # Message not coming from within a Guild!
        return

    if msg.channel.id not in data.get_currency_channels(msg.guild.id):
        # Currency Generation not enabled!
        return

    if not random.uniform(0, 1) <= data.get_currency_chance(msg.guild.id) / 100:
        return

    # After some Checks, now finally - currency spawned!
    chime_image = random.choice([
         'http://2.bp.blogspot.com/-7s3q3BhdCBw/VPUPKAOTbUI/AAAAAAAAlCs/5vyP_lAN0S4/s1600/bardchime.jpg',
         'http://st.game.thanhnien.vn/image/9613/2015/11/24/trang-phuc-mua-dong/06.jpg',
         'http://pm1.narvii.com/5786/089f9a52941e8ded0f54df0978378db42680f6d8_hq.jpg',
         'https://cdn.discordapp.com/attachments/172251363110027264/283612882846089216/unknown.png'
    ])
    data.currency_increment_count(msg.guild.id)
    await embeds.desc_with_img(msg.channel, '**A Chime has appeared!** Type $pick to collect it!', chime_image,
                               f'This is Chime #{data.get_currency_total(msg.guild.id)} for this Guild.')

