import discord
import os

from src.events import message, members

print('Loading Bot...')

# All Events go through here.
client = discord.Client()


@client.event
async def on_ready():
    print('Logged in.')


@client.event
async def on_resumed():
    pass


@client.event
async def on_message(msg):
    await message.handle_message(msg)


@client.event
async def on_message_delete(msg):
    pass


@client.event
async def on_message_edit(before, after):
    pass


@client.event
async def on_reaction_add(reaction, user):
    pass


@client.event
async def on_reaction_remove(reaction, user):
    pass


@client.event
async def on_reaction_clear(reaction, user):
    pass


@client.event
async def on_channel_create(channel):
    pass


@client.event
async def on_channel_delete(channel):
    pass


@client.event
async def on_channel_update(before, after):
    pass


@client.event
async def on_member_join(member):
    members.join(member)


@client.event
async def on_member_remove(member):
    pass


@client.event
async def on_member_update(before, after):
    pass


@client.event
async def on_server_join(server):
    pass


@client.event
async def on_server_remove(server):
    pass


@client.event
async def on_server_update(before, after):
    pass


@client.event
async def on_server_role_create(role):
    pass


@client.event
async def on_server_role_delete(role):
    pass


@client.event
async def on_server_role_update(before, after):
    pass


@client.event
async def on_server_emojis_update(before, after):
    pass


@client.event
async def on_server_available(server):
    pass


@client.event
async def on_server_unavailable(server):
    pass


@client.event
async def on_member_ban(member):
    pass


@client.event
async def on_member_unban(server, user):
    pass


def start():
    client.run(os.environ['DISCORD_TOKEN'])
    message.data.save_all()
