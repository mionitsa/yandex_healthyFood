
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
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.

        res['response']['text'] = 'Здравствуйте! Вас приветствует гид в мир ' \
        'полезной еды. Для начала введите свой пол, возраст, рост и вес. Например: ' \
        '24 175 68.'
        return

    data = (req['request']['original_utterance']).split()

    kkal = int(10*int(data[3]) + 6.25*int(data[2]) - 5*int(data[1]))

    if data[0].lower() == 'мужчина':
        res['response']['text'] = 'Вам нужно потреблять %s килокалорий в день.' % (
            str(kkal + 5)
        )

    if data[0].lower() == 'женщина':
        res['response']['text'] = 'Вам нужно потреблять %s килокалорий в день.' % (
            str(kkal - 161)
        )

    if req['request']['original_utterance'] == '1':
        res['response']['text'] = 'Хорошо, учтём!'
