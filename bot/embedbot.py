import string

import discord
from discord.ext import commands
from TimeConversion import DataOut as DataOut


class EmbedBot:

    def __init__(self, bot: commands.Bot):
        self.bot = bot

    async def bot_embed(self, channel, description, url, icon_url, footer_text):
        embed = discord.Embed(description=description, color=0x00ffffff)
        embed.set_thumbnail(url=url)
        embed.set_footer(text=footer_text, icon_url=icon_url)
        await channel.send(embed=embed)

    async def embed_top(self, top_game, guild, url, description, footer_text, date=None, bot=None):

        icon_url = 'https://cdn.onlinewebfonts.com/svg/download_378989.png'
        description = self.description(description, date)
        description = self.description_time(top_game, description, bot)
        category = guild.categories[0]
        channel = category.channels[0]
        await self.bot_embed(channel, description, url, icon_url, footer_text)

    async def embed_user(self, top_game, ctx, url, description, footer_text, date=None, bot=None):
        icon_url = 'https://cdn.onlinewebfonts.com/svg/download_378989.png'
        description = self.description(description, date)
        description += self.description_time(top_game, bot)
        footer_text = self.footer_text(top_game, footer_text)
        await self.bot_embed(ctx, description, url, icon_url, footer_text)

    def description(self, description, date):
        if date is not None:
            description += f' {date} \n'
        elif date is None:
            description += f'\n'
        return description

    def description_time(self, top_game, bot):
        tg = DataOut()
        description: string = ''
        for i in top_game:
            tg.time_update(i[1])
            if bot:
                description += f'\t{bot.get_user(i[0]).display_name} - '
            elif bot is None:
                description += f'\t{i[0]} - '
            description += f'{tg.output_days(True)}, '
            description += f'{tg.output_hours(True)}, '
            description += f'{tg.output_minutes(True)}\n'
        return description

    def footer_text(self, top_game, footer_text):
        tg = DataOut()
        if footer_text is None:
            all_tg = 0
            for i in top_game:
                all_tg += i[1]
            tg.time_update(all_tg)
            footer_text = f'{tg.output_days(True)}, '
            footer_text += f'{tg.output_hours(True)}, '
            footer_text += f'{tg.output_minutes(True)}\n'
        return footer_text
