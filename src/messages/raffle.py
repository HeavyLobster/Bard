import random
import discord
from src.util import embeds

# Return's a random user's nickname and 4 digit identifier
async def raffle(msg):

    onlineMembers = []

    for member in msg.guild.members:
        if member.status == discord.Status.online:
            onlineMembers.append(member)

    winnerIndex = random.randrange(len(onlineMembers))

    formattedString = onlineMembers[winnerIndex].name
    formattedString += "#"
    formattedString += onlineMembers[winnerIndex].discriminator

    return await embeds.desc_only(msg.channel, formattedString)
