# Member Join, Member Remove, Member Update, Member Ban, Member Unban

print('Loading Member Event Handler... ', end='')


async def join(member):
    await member.guild.default_channel.send(f'Welcome {member.mention} to the {member.guild.name}! '
                                            'Head to role-assignment to get Roles! <:bardlove:242942446072233984>')


async def leave(member):
    pass


print('done.')
