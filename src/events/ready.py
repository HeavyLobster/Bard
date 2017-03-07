from src import twitch
from src.bot import client
from src.messages.roles import fetch_role_assignment_messages
from src.util import data_cruncher


async def on_ready():
    print('Logged in.')
    await fetch_role_assignment_messages()
    print('Starting Twitch Event Listener...')
    client.loop.create_task(twitch.update_streams(client.get_channel(
        data_cruncher.data.get_stream_announcement_channel())))
