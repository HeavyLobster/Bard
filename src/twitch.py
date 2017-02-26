import aiohttp
import asyncio
import os

from src import bot
from src.util.data_cruncher import data
from src.util.embeds import url_with_desc

url = 'https://api.twitch.tv/kraken/streams/'


async def get_stream(stream_name: str):
    with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'{url}{stream_name}?client_id={os.environ["TWITCH_TOKEN"]}') as resp:
                try:
                    if (await resp.json())['stream'] is None:
                        stream = [stream_name, False]
                    else:
                        stream = [stream_name, True]
                except KeyError:
                    print(f'Failed to access Stream data for {stream_name}.')
                    return [stream_name, None]
        except aiohttp.errors.ClientOSError:
            print('Can\'t fetch Stream Data...')
        else:
            return stream


async def update_streams(channel):
    try:
        os.environ['TWITCH_TOKEN']
    except KeyError:
        print('No Twitch Token found in Environment Variables. Not Starting...')
    else:
        await bot.client.wait_until_ready()
        last_streamers, curr_streamers = [], []
        while not bot.client.is_closed():
            for idx, streamer_name in enumerate(data.get_twitch_subscriptions()):
                curr_streamer = await get_stream(streamer_name)
                if curr_streamer[1] is None:
                    print(f'Couldn\'t update Stream State of {curr_streamer[0]}')
                elif last_streamers != [] and curr_streamer[1] != last_streamers[idx][1]:
                    await url_with_desc(channel,
                                        f'Twitch: {curr_streamer[0]}',
                                        f'http://twitch.tv/{curr_streamer[0]}',
                                        f'**{curr_streamer[0]}** is now {"online" if curr_streamer[1] else "offline"}!')
                curr_streamers.append(curr_streamer)
                await asyncio.sleep(1)  # Rate limit is around 1 request per second
            last_streamers = curr_streamers
            curr_streamers = []  # Reset List so it doesn't fill up infinitely
