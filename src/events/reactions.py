from src.util import ClickableCustomReactionEmbed

# Clickable Embed Storage to keep maximum one of each embed type in memory
clickable_embed_storage = {
    'custom-reaction': None,
    'quotes': None
}


def get_custom_reaction_embed():
    return clickable_embed_storage['custom-reaction']


def get_quotes_embed():
    return clickable_embed_storage['quotes']


async def create_custom_reaction_embed(title: str, contents: list, channel, icon_link: str = ''):
    embed = clickable_embed_storage['custom-reaction']
    if isinstance(embed, ClickableCustomReactionEmbed.ClickableCustomReactionEmbed):
        await embed.remove()
        print('Deleted Old Custom Reaction Embed.')
    clickable_embed_storage['custom-reaction'] = ClickableCustomReactionEmbed.ClickableCustomReactionEmbed(title, contents, icon_link)
    await get_custom_reaction_embed().send(channel)


def remove_custom_reaction_embed():
    clickable_embed_storage['custom-reaction'] = None


async def move_custom_reaction_embed(right: bool, user):
    await get_custom_reaction_embed().move(right, user)
