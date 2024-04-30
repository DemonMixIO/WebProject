import datetime
import json
import random

import requests
import wikipedia

wikipedia.set_lang("ru")


def get_wiki_summary(query):
    try:
        summary = wikipedia.summary(query, sentences=2)
        return summary
    except wikipedia.exceptions.PageError:
        return "К сожалению, я не смог найти информацию по вашему запросу."
    except wikipedia.exceptions.DisambiguationError as e:
        return (f"Ваш запрос может относиться к разным темам: {', '.join(e.options[:3])}... "
                f"Пожалуйста, уточните ваш запрос.")


def astrology_get_signs():
    with open('data/signs.json', 'r', encoding='utf-8') as file:
        json_file = json.load(file)
    signs = []
    for dct in json_file:
        signs.append(dct['name'])
    return signs


def astrology_get_horoscope(sign):
    url = "https://newastro.vercel.app/"
    payload = {
        "date": (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%Y-%m-%d"),
        "lang": "ru",
        "sign": sign
    }
    response = requests.post(url, json=payload)
    caption = response.json()['horoscope'].split(' - ', 1)[1].replace('.', '. '.replace(' -', ' - '))
    image = response.json()['icon']
    return caption, image


def handle_dice_roll(query):
    result = []
    if query == '1x6':
        result = random.randint(1, 6)
    elif query == '2x6':
        result = f"{random.randint(1, 6)}, {random.randint(1, 6)}"
    elif query == '1x20':
        result = random.randint(1, 20)
    else:
        if 'x' in query:
            splq = query.split('x')
            if len(splq) == 2:
                if splq[0].isdigit() and splq[1].isdigit():
                    for i in range(int(splq[0])):
                        result.append(random.randint(1, int(splq[1])))
    return ', '.join(result)
