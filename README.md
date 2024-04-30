# DS-Bot и TG-Bot Launcher

Этот скрипт запускает двух ботов: DS-Bot и TG-Bot. DS-Bot - это бот для Discord, а TG-Bot - бот для Telegram. Оба бота предназначены для взаимодействия с пользователями на соответствующих платформах.

## Необходимые условия
- Python 3.6 или более поздняя версия
- модуль `concurrent.futures`
- модули `ds_bot` и `tg_bot`
- файл `tokens.py`, содержащий токены бота

## Как запустить
1. Убедитесь, что в вашем проекте есть необходимые модули и файлы.
2. Запустите скрипт `main.py`.

## Структура кода
Скрипт `main.py` использует `ThreadPoolExecutor` для одновременного запуска DS-Bot и TG-Bot. Функция `ds_bot.run(DS_TOKEN)` запускает DS-Bot, а функция `tg_launch(TG_TOKEN)` запускает TG-Bot.

## Конфигурация
Токены ботов DS-Bot и TG-Bot хранятся в файле `tokens.py`. Вы можете найти токены для каждого бота в переменных `DS_TOKEN` и `TG_TOKEN`, соответственно.


## Команды
Список команд у обеих ботов похожий. Для получения более подробной информации о командах воспользуйтесь командой `/help` для TG-Bot и `!commands` для DS-Bot.