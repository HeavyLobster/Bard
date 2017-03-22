import asyncio

import aiohttp
import os
from src.util.data_cruncher import data

from src import bot
from src.util.embeds import url_with_desc

url = 'https://api.twitch.tv/kraken/streams/'


async def get_stream(stream_name: str):
    """
    Helper Function to get information about the state of a single Channel.
    
    An interesting Note is that sometimes the Twitch API will return some weird JSON thing I have not figured out yet.
    In that case, it the second Item in the List returned is None to indicate that the requested Stream is neither
    offline nor online, but rather that the Twitch API returned something weird.
    
    :param stream_name: The Streamer Name for which to obtain Information. 
    :return: 
    """
    with aiohttp.ClientSession() as session:
        try:
            async with session.get(f'{url}{stream_name}?client_id={os.environ["TWITCH_TOKEN"]}') as resp:
                try:
                    if (await resp.json())['stream'] is None:
                        stream = [stream_name, False]
                    else:
                        stream = [stream_name, True]
                except KeyError:
                    # Something is wrong here with the Twitch API.
                    return [stream_name, None]
        except aiohttp.errors.ClientOSError:
            print('Can\'t fetch Stream Data...')
        else:
            return stream


async def update_streams(channel):
    """
    Starts the Stream Update Listener towards the Twitch API. 
    
    If TWITCH_TOKEN is not found in the Environment Variables, it will not start.
    Otherwise, it will enter a loop running until the connected Discord Client logs off.
    
    :param channel: The Channel in which to send announcements about a stream going online / offline.
    """
    try:
        os.environ['TWITCH_TOKEN']
    except KeyError:
        print('No Twitch Token found in Environment Variables. Can\'t initialize Twitch Stream Update Listener...')
    else:
        await bot.client.wait_until_ready()
        last_streamers, curr_streamers = [], []
        while not bot.client.is_closed():
            for idx, streamer_name in enumerate(data.get_twitch_subscriptions()):
                curr_streamer = await get_stream(streamer_name)
                if curr_streamer[1] is None or (last_streamers != [] and last_streamers[idx][1]) is None:
                    continue
                elif last_streamers != [] and curr_streamer[1] != last_streamers[idx][1]:
                    await url_with_desc(channel,
                                        f'Twitch: {curr_streamer[0]}',
                                        f'http://twitch.tv/{curr_streamer[0]}',
                                        f'**{curr_streamer[0]}** is now {"online!" if curr_streamer[1] else "offline."}'
                                        f'\n {f"http://twitch.tv/{curr_streamer[0]}" if curr_streamer[1] else ""}')
                curr_streamers.append(curr_streamer)
                await asyncio.sleep(5)
            last_streamers = curr_streamers
            curr_streamers = []  # Reset List so it doesn't fill up infinitely
        print('Shut Down Twitch Stream Update Listener, Bot logged off.')
