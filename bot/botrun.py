import json
import os
import random
import sqlite3
import string

import discord
from discord.ext import commands

from TimeConversion import DataOut as DataOut
from TimeConversion import SecondsConvert as SecondsConvert
from WorkBase import Base as Base
from embedbot import EmbedBot as Embed

bot = commands.Bot(command_prefix='!', intents=discord.Intents.all(), )
base1 = Base('BOT.db')

@bot.event
async def on_ready():
    print('connect')
    sc = SecondsConvert()

    tables = base1.fetchall
    for table in tables:
        for guild in bot.guilds:
            if table[1] in guild.name.replace(" ", "") + 'Game':
                if sc.day == 1:
                    top_game = base1.execute_top_3('game', table[1], sc.months_minus, sc.data)
                    eb = Embed(bot)
                    url = 'https://discordhub.com/static/icons/25827c76015aa84041ac8fb6ed14bd56.jpg?q=1599333568'
                    description = f'Топ игр c'
                    footer_text = f'Ты втираешь мне какуе-то дич'
                    await eb.embed_top(top_game, guild, url, description, footer_text, sc.months_minus)

                    top_game = base1.execute_top_3('userid', table[1], sc.months_minus, sc.data)
                    description = f'Топ игроков c'
                    url = 'https://images.fineartamerica.com/images/artistlogos/2-kate-green-1479756827-square.jpg'
                    await eb.embed_top(top_game, guild,  url, description, footer_text, sc.months_minus, bot)


# команда инфо с подкомандами
@bot.command(name='инфо')
async def инфо(ctx, arg=None):
    author = ctx.message.author
    if arg is None:
        await ctx.send(f'{author.mention} \n Введите: \n !инфо общая \n !инфо команды')
    elif arg == 'общая':
        await ctx.send(f'{author.mention} \n Я Наблюдатель версии 1.0.0. Я умею собирать статистику по '
                       f'играм и матюкам. В дальнейшем я буду улучшаться и модифицироваться. Работаю я, '
                       f'когда у @Gemad работает комп. Если меня нет значит и @Gemad не дома')
    elif arg == 'команды':
        await ctx.send(f'{author.mention} \n !test - Бот онлайн? \n !статус - мои матюки \n !статистика '
                       f'пользователь @имя период(в днях,НЕ ОБЯЗАТЕЛЬНО) - вывод информации по играм пользователя \n '
                       f'!статистика пользователи - вывод информации времени в играх всех пользователей \n '
                       f'!статистика я период(в днях,НЕ ОБЯЗАТЕЛЬНО) - вывод информации себя \n !топ - вывод топ по '
                       f'времени в игре')



# Команда статус пользователя
@bot.command(name='статус')
async def status(ctx):
    base1.execute_check(ctx.message.guild.name.replace(" ", ""))
    warning = base1.check(ctx.message.guild.name.replace(" ", ""), ctx.message.author.id)

    if warning is None:
        await ctx.send(f'{ctx.message.author.mention}, чист как слеза')
    else:
        await ctx.send(f'{ctx.message.author.mention} сказал {warning[1]} матюков')


@bot.command(name='топ')
async def top(ctx):
    time_game = base1.execute_users(ctx.guild.name.replace(" ", "") + 'Game')
    description = 'Время в игре'
    url = 'https://discordhub.com/static/icons/25827c76015aa84041ac8fb6ed14bd56.jpg?q=1599333568'
    eb = Embed(bot)
    await eb.embed_user(time_game, ctx, url, description, None, None, bot)

@bot.group(name='статистика')
async def statistics(ctx):
    if ctx.invoked_subcommand is None:
        time_game = base1.execute_statistics(ctx.guild.name.replace(" ", "") + 'Game')
        description: string = 'За все время'
        url = 'https://discordhub.com/static/icons/25827c76015aa84041ac8fb6ed14bd56.jpg?q=1599333568'
        eb = Embed(bot)
        await eb.embed_user(time_game, ctx, url, description, None, None, None)


@statistics.command(name='пользователь')
async def statistics_user(ctx, member: discord.Member, arg=None):
    description = f'Пользователь **{member.name}** '
    if arg is None:
        arg = '90'
        description += f'\n'
    else:
        description += f'за период {arg} дней'
    period = SecondsConvert(arg)
    time_game = base1.execute_user(ctx.guild.name.replace(" ", "") + 'Game', member.id, period.data)
    url = member.display_avatar
    eb = Embed(bot)
    await eb.embed_user(time_game, ctx, url, description, None, None, None)

@statistics.command(name='пользователи')
async def top(ctx):
    time_game = base1.execute_users(ctx.guild.name.replace(" ", "") + 'Game')
    description = 'Статистика проведенного времени пользователей'
    url = 'https://sun9-79.userapi.com/s/v1/ig2/kc45bCIF2MN_w0fUsgJrtVF-NuFFI9aCQ26K06Bh_lZIEzu0VqrLkItepEF-vQ0HigF2s2Xu16Df7DeenWIMP_oq.jpg?size=604x604&quality=96&type=album'
    eb = Embed(bot)
    await eb.embed_user(time_game, ctx, url, description, None, None, bot)

@statistics.command(name='я')
async def statistics_me(ctx, arg=None):
    description: string = f'Пользователь **{ctx.author.name}**'
    if arg is None:
        arg = '90'
        description += f'\n'
    else:
        description += f'за период {arg} дней\n'
    period = SecondsConvert(arg)
    description += f'за период {arg} дней\n'
    time_game = base1.execute_user(ctx.guild.name.replace(" ", "") + 'Game', ctx.author.id, period.data)
    url = ctx.author.display_avatar
    eb = Embed(bot)
    await eb.embed_user(time_game, ctx, url, description, None, None, None)

# анализатор мата и баны
@bot.event
async def on_message(message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in
        message.content.split(' ')}.intersection(json.load(open('words.json'))) != set():
        name = message.guild.name.replace(" ", "")
        base1.execute_check(name)
        base1.base_update(name, message.author.id)


    await bot.process_commands(message)
    if message.author.id == 219779423904202752:  # Димин id
        if 'https://' in message.content or message.content == '':
            description = "«Oh My God! Who the hell cares?!»\n© (Peter Griffin)"
            url = 'https://s00.yaplakal.com/pics/pics_original/7/4/0/15640047.jpg'
            embed = discord.Embed(description=description, color=0xFF0000)
            embed.set_thumbnail(url=url)
            await bot.get_channel(message.channel.id).send(embed=embed)


# Приветствие Юзиров
@bot.event
async def on_member_join(member):
    await member.send('Я за тобой слежу и кстати информация по командам череp !инфо')

    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, смотрите кто теперь в нашей гачи тусовке')


# Прощание Юзиров
@bot.event
async def on_member_remove(member):
    for ch in bot.get_guild(member.guild.id).channels:
        if ch.name == 'основной':
            await bot.get_channel(ch.id).send(f'{member}, теперь будет гачиться в другом месте')


@bot.event
async def on_presence_update(before, after):
    if before.activity is not None:
        activity_type = str(before.activity.type)
        if activity_type == 'ActivityType.playing':
            name = before.guild.name.replace(" ", "") + 'Game'
            base1.create_table(name)
            game = before.activity.name
            time_start = before.activity.start.replace(tzinfo=None)
            user_id = before.id
            time_end = SecondsConvert()
            game_time = time_end.time_to_second(time_start)

            base1.base_insert(name, user_id, game, time_start, game_time)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        title_error_two = 'Введенная вами команда не существует'
        desc_error_two = 'Используйте **!help**, чтобы просмотреть список всех доступных команд'
        embed_var_two = discord.Embed(title=title_error_two,
                                      description=desc_error_two,
                                      color=0xFF0000)
        await ctx.reply(embed=embed_var_two)

bot.run(os.getenv('TOKEN'))
