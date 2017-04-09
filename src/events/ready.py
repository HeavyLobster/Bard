from src.util import data_cruncher

from src import twitch, bot


async def on_ready():
    """
    Handles the on_ready Event emitted when the Bot has finished logging in.
    Currently, this fetches messages in #role-assignment on the Bardians Discord Server, and
    afterwards starts a task to get the Streams in the specified Stream Announcement Channel.
    """
    print('Logged in.')
    print('Starting Twitch Event Listener...')
    await bot.client.loop.create_task(twitch.update_streams(bot.client.get_channel(
                                      data_cruncher.data.get_stream_announcement_channel())))
