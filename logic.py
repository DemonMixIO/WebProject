import json

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