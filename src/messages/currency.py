import discord
from src.util.data_cruncher import data


async def generator(msg):
    """
    Generate Currency based on different Parameters and a flavour of Magic.
    
    :param msg: The original Message 
    :return: 
    """
    if msg.channel.id in