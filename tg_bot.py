import asyncio

from telegram import ReplyKeyboardMarkup
from telegram.ext import Application, MessageHandler, filters, CommandHandler

from logic import *
from tokens import TG_TOKEN


async def tg_get_wiki_summary(update, context):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text('Отправьте сообщение в формате: /wiki <запрос>')
        return
    await update.message.reply_text(get_wiki_summary(query))


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


async def tg_astrology_get_horoscope(update, context):
    caption, image = astrology_get_horoscope(update.message.text)
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=image, caption=caption)


async def tg_info(update, context):
    keyboard = [['Узнать дату📅', 'Узнать время⌚', '/wiki'], ['/cat', '/dog', 'Назад']]
    reply_markup = ReplyKeyboardMarkup(keyboard)
    await update.message.reply_text('Выберите действие:', reply_markup=reply_markup)


async def tg_date(update, context):
    await update.message.reply_text(date)


async def tg_time(update, context):
    await update.message.reply_text(time)


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
    result = handle_dice_roll(update.message.text)
    await update.message.reply_text(f"Результат: {result}")


async def tg_handle_timer(update, context):
    query = update.message.text
    seconds = handle_timer(update.message.text)
    if seconds:
        keyboard = [['Жду...']]
        reply_markup = ReplyKeyboardMarkup(keyboard)
        await update.message.reply_text(f'Таймер запущен: {query}. Жди🙂', reply_markup=reply_markup)
        await asyncio.sleep(seconds)
        await update.message.reply_text(f"{query} истекло")
        await tg_timer(update, context)
    else:
        await update.message.reply_text(f"Неверное время: {query}")
        await tg_timer(update, context)


async def tg_back_to_start(update, context):
    await tg_start(update, context)


async def tg_get_random_cat_pic(update, context):
    img = get_random_cat_pic()
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=img)


async def tg_get_random_dog_pic(update, context):
    img = get_random_dog_pic()
    await context.bot.send_photo(chat_id=update.message.chat_id, photo=img)

async def tg_command_dice(update, context):
    query = " ".join(context.args)
    if not query:
        await update.message.reply_text('Отправьте сообщение в формате: /dice <кол-во костей>x<кол-во граней>')
        return
    await update.message.reply_text(handle_dice_roll(query))


async def tg_help(update, context):
    text = '''
/cat - получить случайное изображение кота
/dog - получить случайное изображение собаки
/time - получить текущее время
/date - получить текущую дату
/wiki <запрос> - получить краткую информацию с Википедии
/dice <кол-во костей>x<кол-во граней> - бросить кости
    '''
    await update.message.reply_text(text)


def tg_launch(token):
    print('telegram bot started')
    tg_application = Application.builder().token(token).build()
    tg_application.add_handler(CommandHandler("wiki", tg_get_wiki_summary))
    tg_application.add_handler(CommandHandler("cat", tg_get_random_cat_pic))
    tg_application.add_handler(CommandHandler("dog", tg_get_random_dog_pic))
    tg_application.add_handler(CommandHandler("date", tg_date))
    tg_application.add_handler(CommandHandler("time", tg_time))
    tg_application.add_handler(CommandHandler("dice", tg_command_dice))
    tg_application.add_handler(CommandHandler("help", tg_help))
    tg_application.add_handler(MessageHandler(filters.Regex('Старт'), tg_start))
    tg_application.add_handler(MessageHandler(filters.Regex('Назад'), tg_back_to_start))
    tg_application.add_handler(MessageHandler(filters.Regex('Гороскоп⛎'), tg_astrology_select_sign))
    tg_application.add_handler(MessageHandler(filters.Regex('Астрология🔮'), tg_astrology))
    tg_application.add_handler(MessageHandler(filters.Regex('Информация ℹ'), tg_info))
    tg_application.add_handler(MessageHandler(filters.Regex('Узнать дату📅'), tg_date))
    tg_application.add_handler(MessageHandler(filters.Regex('Узнать время⌚'), tg_time))
    tg_application.add_handler(MessageHandler(filters.Regex('Бросить кубик🎲'), tg_dice))
    tg_application.add_handler(MessageHandler(filters.Regex('^(1x6|2x6|1x20)$'), tg_handle_dice_roll))
    tg_application.add_handler(MessageHandler(filters.Regex('Игровой помощник'), tg_player_start))
    tg_application.add_handler(MessageHandler(filters.Regex('Установить таймер⏲'), tg_timer))
    tg_application.add_handler(MessageHandler(filters.Regex('^(30 секунд|1 минута|5 минут)$'), tg_handle_timer))
    tg_application.add_handler(MessageHandler(filters.Regex(
        '^(Aries|Taurus|Gemini|Cancer|Leo|Virgo|Libra|Scorpio|Sagittarius|Capricorn|Aquarius|Pisces)$'),
        tg_astrology_get_horoscope))
    tg_application.run_polling()


if __name__ == '__main__':
    tg_launch(TG_TOKEN)
