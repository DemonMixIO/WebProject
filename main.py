from concurrent.futures import ThreadPoolExecutor
from ds_bot import bot as ds_bot
from tg_bot import tg_launch
from tokens import *


# для vk: если бот не будет запускаться, попробовать вызывать его...

def main():
    with ThreadPoolExecutor(max_workers=1) as exe:
        exe.submit(ds_bot.run, DS_TOKEN)  # как этот,
        tg_launch(TG_TOKEN)  # этот,


if __name__ == "__main__":
    main()
    # tg_launch(TG_TOKEN)  # или этот
