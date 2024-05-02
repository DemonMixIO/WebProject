from concurrent.futures import ThreadPoolExecutor
from ds_bot import bot as ds_bot
from tg_bot import tg_launch
from tokens import *


def main():
    with ThreadPoolExecutor(max_workers=1) as exe:
        exe.submit(ds_bot.run, DS_TOKEN)
        tg_launch(TG_TOKEN)


if __name__ == "__main__":
    main()
