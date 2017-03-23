import cassiopeia
import discord
import json
import re
import requests
import urllib

from src.events.reactions import create_custom_reaction_embed
from src.util import embeds, lolapi
from src.util.data_cruncher import data
from src import bot


async def invoke_leaderboard_build(msg):
    """
    Invoke the asynchronously running process of building a Leaderboard of the top Mastery Points per Player that habe
    previously added themselves to a List.
    
    :param msg: The Message invoking the command
    :return The built Leaderboard. Takes some time.
    """
    return await bot.client.loop.create_task(_build_league_leaderboard(msg))


async def _build_league_leaderboard(msg):
    """
    Build a Leaderboard containing the top scores for the people who entered themselves into the List previously.
    
    :param msg: The Message invoking the Command 
    :return: The built Leaderboard. Takes some time.
    """
    user_list = data.get_league_guild_users(msg.guild.id)
    info = await embeds.desc_only(msg.channel, f'Building League of Legends Leaderboard for '
                                               f'**{len(user_list)} Users**...')
    users = []
    for user in data.get_league_guild_users(msg.guild.id):
        users.append([lolapi.get_mastery_points_by_id(user[0], user[1]),
                      lolapi.get_summoner_by_id(user[0], user[1]).name])
    users = sorted(users, key=lambda x: x[1], reverse=True)
    leader_board = discord.Embed()
    for idx, pair in enumerate(users):
        score = '{:,}'.format(pair[0])
        leader_board.add_field(name=f'#{idx} + 1: {pair[1]}', value=f'**{score}** points')
    await info.delete()
    return await msg.channel.send(embed=leader_board)


async def add_league_id(msg):
    """
    Add a Summoner ID to the League of Legends Users for the given Guild.
    
    :param msg: The Message invoking the Command 
    :return: The Response from the Bot
    """
    if len(msg.content.split()) < 3:
        return await embeds.desc_only(msg.channel, 'That\'s not the valid way to use this command.')
    region = msg.content.split()[1]
    summoner_name = ' '.join(msg.content.split()[2:])
    try:
        user_id = lolapi.get_id_by_name(summoner_name, region)
    except (cassiopeia.type.api.exception.APIError, ValueError):
        return await embeds.desc_only(msg.channel, 'The League of Legends API returned an Error trying to get your Sum'
                                                   'moner Account. This usually means that your Account was not found.')
    if user_id in sum(data.get_league_guild_users(msg.guild.id), []):
        return await embeds.desc_only(msg.channel, f'**{summoner_name}** is already on the List of Users for '
                                                   f'this Guild.')
    data.add_league_guild_user(msg.guild.id, user_id, region.upper())
    return await embeds.desc_only(msg.channel, f'Added **{summoner_name}** to the List of Users for League of Legends'
                                               f' for this Guild!')


async def remove_league_id(msg):
    """
    Remove a Summoner ID from the League of Legends Users for the given Guild.
    
    :param msg: The Message invoking the Command 
    :return: The Response from the Bot
    """
    if len(msg.content.split()) < 3:
        return await embeds.desc_only(msg.channel, 'That\'s not the valid way to use this command.')
    region = msg.content.split()[1]
    summoner_name = ' '.join(msg.content.split()[2:])
    try:
        user_id = lolapi.get_id_by_name(summoner_name, region)
    except (cassiopeia.type.api.exception.APIError, ValueError):
        return await embeds.desc_only(msg.channel, 'The League of Legends API returned an Error trying to get your Sum'
                                                   'moner Account. This usually means that your Account was not found.')
    if user_id not in sum(data.get_league_guild_users(msg.guild.id), []):  # flatten Array
        return await embeds.desc_only(msg.channel, f'**{summoner_name}** is not on the List of Users for this Guild.')
    data.remove_league_guild_user(msg.guild.id, user_id)
    return await embeds.desc_only(msg.channel, f'Removed **{summoner_name}** from the List of Users for League of '
                                               f'Legends for this Guild.')


async def add(msg):
    """
    Add a Custom Reaction for the Guild in which the Message was sent.
    
    :param msg: The message invoking the Command.
    :return: A discord.Message informing about the Success or Failure of adding it.
    """
    if len(msg.content.split()[2:]) < 1:
        return await embeds.desc_only(msg.channel, 'Too little content for a Custom Reaction!')
    elif msg.content.split()[1] == 'add':  # !add add, u memers
        return await embeds.desc_only(msg.channel, 'That\'s not a valid Custom Reaction name.')
    data.add_custom_reaction(msg.guild.id, msg.content.split()[1], ' '.join(msg.content.split()[2:]), msg.author.name)
    return await embeds.desc_only(msg.channel, f'Added new Custom Reaction called {msg.content.split()[1]}.')


async def meow(msg):
    """
    Sends a random Cat Image or GIF. Note that the request is blocking.
    
    :param msg: The Message invoking the Command
    :return: A discord.Message Object containing a Cat Image or GIF
    """
    link = json.load(urllib.request.urlopen('http://random.cat/meow'))['file']
    return await embeds.img_only(msg.channel, link)


async def woof(msg):
    """
    Sends a random Dog GIF. Note that the request is blocking.
    
    :param msg: The Message invoking the Command 
    :return: A discord.Message Object containing a Cat Image or GIF
    """
    url = requests.get('https://api.giphy.com/v1/gifs/random?'
                       'api_key=dc6zaTOxFJmzC&tag=dog').json()['data']['image_original_url']
    return await msg.channel.send(url)


async def get_one(msg):
    """
    Sends a Custom Reaction with the specified name.
    
    :param msg: The Message invoking the Command 
    :return: None if no Custom Reaction was found, otherwise a discord.Message Object containing the Custom Reaction.
    """
    try:
        name = msg.content[1:].split()[0]
        reaction = data.get_custom_reaction(msg.guild.id, name)
    except IndexError:
        return None
    else:
        if reaction is None:
            return None
        elif reaction[0].startswith('http'):  # Properly Embed Links to GIF, Images etc.
            return await embeds.img_with_footer(msg.channel, reaction[0],
                                                f'"{name}" | Added by {reaction[1]}', reaction[2])
        elif reaction[0] != '':
            return await embeds.desc_with_footer(msg.channel, reaction[0],
                                                 f'"{name}" | Added by {reaction[1]}', reaction[2])


async def build_list(msg):
    """
    Send a List of Custom Reactions found on the Guild in which the Command was invoked.
    
    :param msg: The Message invoking the Command 
    :return: A discord.Message Object with the Bot's Response.
    """
    custom_reactions = data.get_all_custom_reactions_on_guild(msg.guild.id)
    if custom_reactions is None:
        return await embeds.desc_only(msg.channel, 'Sorry, no Quotes were found for this Server.')
    else:
        return await create_custom_reaction_embed(f'- All Custom Reactions on {msg.guild.name} - ',
                                                  custom_reactions, msg.channel,
                                                  'https://lh3.googleusercontent.com/'
                                                  'BvIDv_HYH8HnHubWn_lle2eC5lm5lY3kAGI'
                                                  'kFniSk8x_SDpbUr0dlNTe6P6j_C8f4cSmH-d'
                                                  '0rtuSlUU=w1441-h740')


async def hugemoji(msg):
    """
    Sends a "hugified" version of the Emoji given in the Message. Only works for Custom Emojis.
    
    :param msg: The Message invoking the Command 
    :return: A discord.Message Object with a huge version of the Emoji.
    """
    emoji_id = re.search('[0-9]+', msg.content)
    # Make sure it also works when there's a number in the ID!
    try:
        if len(emoji_id.group(0)) == 1:
            emoji_id = re.search('[0-9]+', msg.content[msg.content.find(emoji_id.group(0)) + 1:])
    except AttributeError:
        return await embeds.desc_only(msg.channel, 'Sorry, something went wrong.')
    else:
        return await embeds.img_only(msg.channel, f'https://cdn.discordapp.com/emojis/{emoji_id.group(0)}.png')


async def help(msg):
    """
    Send a Message with a Link to Bard's Wiki.
    
    :param msg: The Message invoking the Command 
    :return: A discord.Message Object with the hopefully helpful Message.
    """
    return await embeds.desc_only(msg.channel, "**You can view Bard's Commands here:** "
                                               "https://github.com/Volcyy/Bard/wiki")

