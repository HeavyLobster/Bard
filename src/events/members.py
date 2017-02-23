# Member Join, Member Remove, Member Update, Member Ban, Member Unban

print('Loading Member Event Handler...')


async def join(member):
    await member.server.default_channel.send(f'Welcome **{member.name}** to the {member.server.name}!')  #


async def leave(member):
    pass
