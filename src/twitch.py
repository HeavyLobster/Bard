import asyncio

from src import bot
from src.util.data_cruncher import data
from src.util.embeds import url_with_desc


async def update_streams():
    stream_channel = bot.client.get_channel(data.get_stream_announcement_channel())
    while not bot.client.is_closed():
        for idx, stream in enumerate(data.get_streams_status()):
            if data.get_streams()[idx][1] != stream[1]:
                await url_with_desc(stream_channel,
                                    f'**{stream[0]}** is now {"online" if stream[1] else "offline"}!',
                                    f'http://twitch.tv/{stream[0]}')
        await asyncio.sleep(len(data.get_twitch_subscriptions()))  # Rate limit is around 1 request per second
