import random

import discord

from src.util import embeds


class ClickableCustomReactionEmbed:
    def __init__(self, title: str, contents: list, icon_link: str = ''):
        """
        Build a ClickableCustomReactionEmbed, which is an Embedded message that contains multiple different Messages.
        Users can navigate through it by clicking on the Reactions that the Bot added on Creation.
        
        :param title: The Title for the ClickableCustomReactionEmbed which will stay throughout all Navigation. 
        :param contents: A List Containing Custom Reactions in the following format:
                         [ [ contents: str, author: str, creation date: struct_time, name: str ] ... ] 
        :param icon_link: An URL specifying the Icon to use for the Embed.
        """
        # Item: [desc_or_link, added_by, timestamp, name]
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
            self.embeds[idx].set_footer(text=f'"{item[3]}" | Added by {item[1]}')
            self.embeds[idx].timestamp = embeds.datetime_from_struct_time(item[2])
        random.shuffle(self.embeds)
        self.id = 0
        self.index = 0
        self.embedded_message = None

    async def send(self, channel):
        """
        Sends self as an Embed to the specified channel.
        
        :param channel: A discord.Channel object to be used as destination.
        """
        self.embedded_message = await channel.send(embed=self.embeds[self.index])
        self.id = self.embedded_message.id
        await self.embedded_message.add_reaction('\N{BLACK LEFT-POINTING TRIANGLE}')
        await self.embedded_message.add_reaction('\N{BLACK RIGHT-POINTING TRIANGLE}')

    async def move(self, right: bool, member):
        """
        Move the Embed Message either one further in the list of Custom Reactions, or in the opposite direction.
         
        :param right: A boolean specifying whether to move Right or Left. 
        :param member: The discord.Member that added the Reaction to the Message. 
                       This is necessary to only remove the Reaction of the Member, not others. 
        """
        await self.embedded_message.remove_reaction('\N{BLACK RIGHT-POINTING TRIANGLE}' if right
                                                    else '\N{BLACK LEFT-POINTING TRIANGLE}', member)
        try:
            self.index = self.index + 1 if right else self.index - 1
        except IndexError:
            self.index = 0
        finally:
            next_contents = self.embeds[self.index]
            await self.embedded_message.edit(embed=next_contents)

    async def remove(self):
        """
        Delete the Embed containing the ClickableCustomReactionEmbed.
        """
        await self.embedded_message.delete()
        self.id = 0
        self.embeds = []
