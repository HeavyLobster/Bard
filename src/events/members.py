# Member Join, Member Remove, Member Update, Member Ban, Member Unban

print('Loading Member Event Handler...')


async def join(member):
    await member.guild.default_channel.send(f'Welcome **{member.name}** to the {member.guild.name}'
                                            f'! <:bardlove:242942446072233984>')


async def leave(member):
    pass
