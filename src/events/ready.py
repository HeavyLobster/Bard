from src.util import data_cruncher

from src import twitch, bot
from src.messages.roles import fetch_role_assignment_messages


async def on_ready():
    print('Logged in.')
    await fetch_role_assignment_messages()
    print('Starting Twitch Event Listener...')
    bot.client.loop.create_task(twitch.update_streams(bot.client.get_channel(
        data_cruncher.data.get_stream_announcement_channel())))
