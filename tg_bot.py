import asyncio
import datetime
import random

import requests
from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters

from logic import *

TG_BOT_TOKEN = '7160249519:AAHlmU8Giwfpq9VJ9kpuliWtJeDzV6G3fII'


async def tg_start(update, context):
    keyboard = [['Игровой помощник', 'Информация ℹ', 'Астрология🔮']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)


async def tg_astrology_select_sign(update, context):
    keyboard = []
    signs = astrology_get_signs()
    keyboard.append(signs[:4])
    keyboard.append(signs[4:8])
    keyboard.append(signs[8:12])
    keyboard.append(['Назад'])
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите знак зодиака:', reply_markup=reply_markup)


async def tg_astrology_get_goroscope(update, context):
    url = "https://newastro.vercel.app/"
    payload = {
        "date": (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        "lang": "ru",
        "sign": update.message.text
    }
    response = requests.post(url, json=payload)
    caption = response.json()['horoscope'].split(' - ', 1)[1].replace('.', '. '.replace(' -', ' - '))
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=response.json()['icon'], caption=caption)


async def tg_info(update, context):
    keyboard = [['Узнать дату📅', 'Узнать время⌚'], ['Назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)


async def tg_date(update, context):
    """Отправляет дату, когда получена команда /date"""
    await update.message.reply_text(datetime.datetime.now().strftime('%d.%m.%Y'))


async def tg_time(update, context):
    """Отправляет текущее время, когда получена команда /time"""
    await update.message.reply_text(datetime.datetime.now().strftime('%H:%M:%S'))


async def tg_astrology(update, context):
    keyboard = [['Гороскоп⛎', 'Узнать дату📅'], ['Назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)


async def tg_player_start(update, context):
    keyboard = [['Бросить кубик🎲', 'Установить таймер⏲'], ['Назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)


async def tg_dice(update, context):
    keyboard = [['1x6', '2x6', '1x20'], ['Назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите кубик для броска:', reply_markup=reply_markup)


async def tg_timer(update, context):
    keyboard = [['30 секунд', '1 минута', '5 минут'], ['Назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите время:', reply_markup=reply_markup)


async def tg_handle_dice_roll(update, context):
    query = update.message.text
    if query == '1x6':
        result = random.randint(1, 6)
    elif query == '2x6':
        result = f"{random.randint(1, 6)}, {random.randint(1, 6)}"
    elif query == '1x20':
        result = random.randint(1, 20)
    else:
        return
    await update.message.reply_text(f"Результат: {result}")


async def tg_handle_timer(update, context):
    query = update.message.text
    if query == '30 секунд':
        seconds = 30
    elif query == '1 минута':
        seconds = 60
    elif query == '5 минут':
        seconds = 300
    else:
        return
    keyboard = [['Жду...']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text(f'Таймер запущен: {query}. Жди🙂', reply_markup=reply_markup)
    await asyncio.sleep(seconds)
    await update.message.reply_text(f"{query} истекло")
    await tg_timer(update, context)


async def tg_close_timer(update, context):
    await update.message.reply_text('Таймер сброшен.')
    await tg_timer(update, context)


async def tg_back_to_start(update, context):
    await tg_start(update, context)


def tg_launch():
    tg_application = Application.builder().token(TG_BOT_TOKEN).build()
    tg_application.add_handler(MessageHandler(filters.Regex('Старт'), tg_start))
    tg_application.add_handler(MessageHandler(filters.Regex('Игровой помощник'), tg_player_start))
    tg_application.add_handler(MessageHandler(filters.Regex('Информация ℹ'), tg_info))
    tg_application.add_handler(MessageHandler(filters.Regex('Астрология🔮'), tg_astrology))
    tg_application.add_handler(MessageHandler(filters.Regex('Узнать дату📅'), tg_date))
    tg_application.add_handler(MessageHandler(filters.Regex('Узнать время⌚'), tg_time))
    tg_application.add_handler(MessageHandler(filters.Regex('Бросить кубик🎲'), tg_dice))
    tg_application.add_handler(MessageHandler(filters.Regex('Установить таймер⏲'), tg_timer))
    tg_application.add_handler(MessageHandler(filters.Regex('Закрыть❌'), tg_close_timer))
    tg_application.add_handler(MessageHandler(filters.Regex('^(1x6|2x6|1x20)$'), tg_handle_dice_roll))
    tg_application.add_handler(MessageHandler(filters.Regex('^(30 секунд|1 минута|5 минут)$'), tg_handle_timer))
    tg_application.add_handler(MessageHandler(filters.Regex('Назад'), tg_back_to_start))
    tg_application.add_handler(MessageHandler(filters.Regex('Гороскоп⛎'), tg_astrology_select_sign))
    tg_application.add_handler(MessageHandler(filters.Regex(
        '^(Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|Sagittarius|Capricorn|Aquarius|Pisces)$'),
        tg_astrology_get_goroscope))
    tg_application.run_polling()


if __name__ == '__main__':
    tg_launch()
