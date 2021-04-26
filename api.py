
# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging
from random import randint

# Импортируем подмодули Flask для запуска веб-сервиса.
from flask import Flask, request

app = Flask(__name__)

logging.basicConfig(level=logging.DEBUG)

# Хранилище данных о сессиях.
sessionStorage = {}


# Задаем параметры приложения Flask.
@app.route("/", methods=['POST'])
def main():
    # Функция получает тело запроса и возвращает ответ.
    logging.info('Request: %r', request.json)

    response = {
        "version": request.json['version'],
        "session": request.json['session'],
        "response": {
            "end_session": False
        }
    }

    handle_dialog(request.json, response)

    logging.info('Response: %r', response)

    return json.dumps(
        response,
        ensure_ascii=False,
        indent=2
    )


# Функция для непосредственной обработки диалога.
def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Меня зовут ЗдравоБот. Я помогу Вам ' \
        'вести здоровый образ жизни, а также дам несколько советов о правильном питании. ' \
        'Для начала давайте рассчитаем количество калорий, ' \
        'которые Вам стоит потреблять ежедневно. Скажите "Рассчитать".'
        return

    if 'рассчитать' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Введите свой пол, возраст, рост, вес, а также укажи степень ' \
        'Вашей физической активности через пробел, всё просто, ничего лишнего.\n1. Полное отсутствие ' \
        'физической активности.\n2. Небольшие пробежки или легкая ' \
        'гимнастика 1-3 раза в неделю.\n3. Средние нагрузки 3-5 раз в неделю.\n4. ' \
        'Полноценные тренировки 6-7 раз в неделю. Вот так: Мужчина 24 186 72 2'
        return

    if 'мужчина' in req['request']['original_utterance'].lower():
        data = (req['request']['original_utterance']).split()
        kkal = int(10*int(data[3]) + 6.25*int(data[2]) - 5*int(data[1]) + 5)
        if int(data[4]) == 1:
            kkal *= 1.2
        if int(data[4]) == 2:
            kkal *= 1.375
        if int(data[4]) == 3:
            kkal *= 1.55
        if int(data[4]) == 4:
            kkal *= 1.725
        res['response']['text'] = 'Вам нужно потреблять %s килокалорий в день.' % (
            str(int(kkal)))
        return

    if 'женщина' in req['request']['original_utterance'].lower():
        data = (req['request']['original_utterance']).split()
        kkal = int(10*int(data[3]) + 6.25*int(data[2]) - 5*int(data[1]) - 161)
        if int(data[4]) == 1:
            kkal *= 1.2
        if int(data[4]) == 2:
            kkal *= 1.375
        if int(data[4]) == 3:
            kkal *= 1.55
        if int(data[4]) == 4:
            kkal *= 1.725
        res['response']['text'] = 'Вам нужно потреблять %s килокалорий в день.' % (
            str(int(kkal)))
        return
    else:
        res['response']['text'] = 'Не совсем Вас понял, попробуйте вновь.'
        return

    if 'факт' in req['request']['original_utterance'].lower():
        bank = ['бла бла бла', 'ла ла лей', 'вот это да', 'ахаххахах']
        random_number = randint(0, len(bank)-1)
        res['response']['text'] = bank[random_number]
        return
