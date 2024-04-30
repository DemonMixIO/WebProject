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
    if 'x' in query:
        splq = query.split('x')
        if len(splq) == 2:
            if splq[0].isdigit() and splq[1].isdigit():
                for i in range(int(splq[0])):
                    result.append(str(random.randint(1, int(splq[1]))))
    return ', '.join(result)


def handle_timer(query):
    if query == '30 секунд':
        seconds = 30
    elif query == '1 минута':
        seconds = 60
    elif query == '5 минут':
        seconds = 300
    else:
        return
    return seconds


def get_random_dog_pic():
    try:
        response = requests.get('https://dog.ceo/api/breeds/image/random')
        if response.status_code == 200:
            json_response = response.json()
            dog_pic_url = json_response['message']
            return dog_pic_url
    except Exception as e:
        print(f"Ошибка при получении картинки с собакой: {e}")
    return None


def get_random_cat_pic():
    try:
        response = requests.get('https://api.thecatapi.com/v1/images/search')
        if response.status_code == 200:
            json_response = response.json()
            cat_pic_url = json_response[0]['url']
            return cat_pic_url
    except Exception as e:
        print(f"Ошибка при получении картинки с котиком: {e}")
    return None
