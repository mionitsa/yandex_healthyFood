
# coding: utf-8
# Импортирует поддержку UTF-8.
from __future__ import unicode_literals

# Импортируем модули для работы с JSON и логами.
import json
import logging

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

        sessionStorage[user_id] = {
            'suggests': [
                "Мужчина",
                "Женщина",
            ]
        }

        res['response']['text'] = 'Здравствуйте! Вас приветствует гид в мир ' \
        'полезной еды. Для начала введите свой пол, возраст, рост и вес. Например: ' \
        'Мужчина 24 175 68.'
        #res['response']['buttons'] = get_suggests(user_id)

    if 'мужчина' in req['request']['original_utterance'].lower():
        data = (req['request']['original_utterance']).split()
        kkal = int(10*int(data[3]) + 6.25*int(data[2]) - 5*int(data[1]))
        res['response']['text'] = 'Вам нужно потреблять %s килокалорий в день.' % (
            str(kkal + 5))
        return

    if 'женщина' in req['request']['original_utterance'].lower():
        data = (req['request']['original_utterance']).split()
        kkal = int(10*int(data[3]) + 6.25*int(data[2]) - 5*int(data[1]))
        res['response']['text'] = 'Вам нужно потреблять %s килокалорий в день.' % (
            str(kkal - 161))
        return

    if req['session']['new']:
        res['response']['text'] = 'Также, укажите степень Вашей физической активности:\n'\
        '1. Полное отсутствие физической активности.\n2. Небольшие пробежки или легкая ' \
        'гимнастика 1-3 раза в неделю.\n3. Средние нагрузки 3-5 раз в неделю.\n4. ' \
        'Полноценные тренировки 6-7 раз в неделю.\n5. Интенсивные силовые упражнения ' \
        '2 раза в день.'

    if req['request']['original_utterance'].lower() == 'привет':
        res['response']['text'] = 'Привет, друг!'
        return

def get_suggests(user_id):
    session = sessionStorage[user_id]

    suggests = [
        {'title': suggest, 'hide': False}
        for suggest in session['suggests']
    ]


    return suggests
