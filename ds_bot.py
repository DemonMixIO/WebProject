from logic import *
from tokens import DS_TOKEN

import asyncio

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix='!', intents=intents)


@bot.command(name='set_timer')
async def ds_set_timer(ctx, hours, minutes, seconds):
    time = int(hours) * 3600 + int(minutes) * 60 + int(seconds)
    await ctx.send(f"таймер запущен на {hours}:{minutes}:{seconds}!")
    await asyncio.sleep(time)
    await ctx.send("время Х наступило!")


@bot.command(name='wiki')
async def ds_get_wiki_summary(ctx, *, query=''):
    if not query:
        await ctx.send('Отправьте сообщение в формате: !wiki <запрос>')
        return
    result = get_wiki_summary(query)
    await ctx.send(result)


@bot.command(name='dice')
async def ds_handle_dice_roll(ctx, dice=''):
    if not dice:
        await ctx.send('Отправьте сообщение в формате: !dice <кол-во костей>x<кол-во граней>')
        return
    result = handle_dice_roll(dice)
    if result:
        await ctx.send(result)


@bot.command(name='cat')
async def ds_get_random_cat_pic(ctx):
    result = get_random_cat_pic()
    await ctx.send(result)


@bot.command(name='dog')
async def ds_get_random_dog_pic(ctx):
    result = get_random_dog_pic()
    await ctx.send(result)


@bot.command(name='horoscope')
async def ds_get_horoscope(ctx, sign=''):
    if not sign:
        await ctx.send('Отправьте сообщение в формате: !horoscope <знак зодиака>')
        return
    horoscope, image = astrology_get_horoscope(sign)
    if horoscope and image:
        await ctx.send(image)
        await ctx.send(horoscope)


@bot.command(name='time')
async def ds_time(ctx):
    result = time()
    await ctx.send(result)


@bot.command(name='date')
async def ds_date(ctx):
    result = date()
    await ctx.send(result)


@bot.command(name='commands')
async def ds_help(ctx):
    help_text = """
!date - получить текущую дату
!time - получить текущее время
!cat - получить случайное изображение кота
!dog - получить случайное изображение собаки
!horoscope <знак зодиака> - получить прогноз на день
!dice <кол-во костей>x<кол-во граней> - бросить кости
!wiki <запрос> - получить краткую информацию с Википедии
!set_timer <hours> <minutes> <seconds> - запустить таймер
    """
    await ctx.send(help_text)


if __name__ == '__main__':
    bot.run(DS_TOKEN)
    print('print')
