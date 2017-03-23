import discord
import os

from src.events import message, members, reactions, ready

print('Loading Bot... ', end='')

# All Events go through here.
client = discord.Client()


# Declear boolean to keep track of whether Volcyy's bot is online
volcyyBotOnline = False


# To avoid conflicts with another Bard bot, ignore commands and
# change status to make it clearer what's going on.

def becomeInactive():

    global volcyyBotOnline
    volcyyBotOnline = True


# Same as above, but becoming active instead of inactive

def becomeActive():

    global volcyyBotOnline
    volcyyBotOnline = False


@client.event
async def on_ready():

    # Detect Volcyy's bot when starting
    volcyyBot = client.get_guild(172226206375084032).get_member(226612862620008448)

    if volcyyBot.status != discord.Status.offline:
        becomeInactive()
        await client.change_presence(status=discord.Status.dnd)

    await ready.on_ready()


@client.event
async def on_resumed():
    pass


@client.event
async def on_message(msg):

    # Check if Volcyy's bot is online:
    if not volcyyBotOnline:

        try:
            await message.handle_message(msg)
        except TypeError:
            # Message wasn't sent in a Guild
            pass


@client.event
async def on_message_delete(msg):
    pass


@client.event
async def on_message_edit(before, after):
    await message.handle_message(after)


@client.event
async def on_reaction_add(reaction, user):

# Check if Volcyy's bot is online

    global volcyyBotOnline
    if not volcyyBotOnline:

        # Actual function
        if user.id != client.user.id:
            try:
                if reaction.message.id == reactions.get_custom_reaction_embed().id:
                    if reaction.emoji == '\N{BLACK RIGHT-POINTING TRIANGLE}':
                        await reactions.move_custom_reaction_embed(True, user)
                    elif reaction.emoji == '\N{BLACK LEFT-POINTING TRIANGLE}':
                        await reactions.move_custom_reaction_embed(False, user)
            except AttributeError:
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

    # Check if Volcyy's bot is online
    if not volcyyBotOnline:
        await members.join(member)


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


# Defining the event handler for on_member_update locally
#
# As of 2017-03-14 it's being used to detect if Volcyy's
# bot is online and affecting the behavior of other handlers

@client.event
async def on_member_update(before, after):

    global volcyyBotOnline

    # Detect Volcyy's bot's id and watch it for status changes

    if before.id == 226612862620008448:

        # If offline and coming online
        if before.status == discord.Status.offline and after.status != discord.Status.offline:
            becomeInactive()
            await client.change_presence(status=discord.Status.dnd)

        # If online and going offline
        if before.status != discord.Status.offline and after.status == discord.Status.offline:
            becomeActive()
            await client.change_presence(status=discord.Status.online)


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
    message.data_cruncher.data.save_all()


print('done.')
print('All Modules Loaded. Establishing Connection to Discord...')
