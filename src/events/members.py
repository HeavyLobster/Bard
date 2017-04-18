import random

# Member Join, Member Remove, Member Update, Member Ban, Member Unban

print('Loading Member Event Handler... ', end='')


async def join(member):

    if random.randrange(6) != 0:
        await member.guild.default_channel.send(f'Welcome {member.mention} to the {member.guild.name}! '
                                            'Head to <#265551115901206528> to get Roles! <:bardlove:242942446072233984>')
    else:
        await member.guild.default_channel.send(f'Welcome {member.mention} ! <:bardhi2:269858268048916480> Have some <:cacao:269857893086527488> and <:porosnax:278951733609234433> <:bardhug:269858053820645389> \nHead to <#265551115901206528> to get Roles! <:bardlove:242942446072233984>')


async def leave(member):
    pass


print('done.')
