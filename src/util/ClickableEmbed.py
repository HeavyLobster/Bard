import random

import discord

from src.util import embeds


class ClickableEmbed:
    def __init__(self, title: str, contents: list, icon_link: str = ''):
        # Item: [desc_or_link, added_by, timestamp]
        print('Building Clickable Table... ', end='')
        self.embeds = list()
        for idx, item in enumerate(contents):
            self.embeds.append(discord.Embed())
            if icon_link != '':
                self.embeds[idx].set_thumbnail(url=icon_link)
            self.embeds[idx].title = title
            if item[0].startswith('http'):
                self.embeds[idx].set_image(url=item[0])
            else:
                self.embeds[idx].description = item[0]
            self.embeds[idx].set_footer(text=f'Added by {item[1]}')
            self.embeds[idx].timestamp = embeds.datetime_from_struct_time(item[2])
        random.shuffle(self.embeds)
        self.id = 0
        self.index = 0
        self.embedded_message = None
        print('done.')

    async def send(self, channel):
        self.embedded_message = await channel.send(embed=self.embeds[self.index])
        self.id = self.embedded_message.id
        await self.embedded_message.add_reaction('\N{BLACK LEFT-POINTING TRIANGLE}')
        await self.embedded_message.add_reaction('\N{BLACK RIGHT-POINTING TRIANGLE}')

    async def move(self, right: bool, member):  # Right or Left?
        await self.embedded_message.remove_reaction('\N{BLACK RIGHT-POINTING TRIANGLE}' if right
                                                    else '\N{BLACK LEFT-POINTING TRIANGLE}', member)
        try:
            self.index = self.index + 1 if right else self.index - 1
            next_contents = self.embeds[self.index]
        except IndexError:
            self.index = 0
        else:
            await self.embedded_message.edit(embed=next_contents)

    async def remove(self):
        print('Removing Clickable Table... ', end='')
        await self.embedded_message.delete()
        self.id = 0
        self.embeds = []
        print('done.')
