from logic import *
from tokens import DS_TOKEN

import asyncio

import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True
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

if __name__ == '__main__':
    bot.run(DS_TOKEN)
