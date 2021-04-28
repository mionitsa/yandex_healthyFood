
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

def handle_dialog(req, res):
    user_id = req['session']['user_id']

    if req['session']['new']:
        res['response']['text'] = 'Привет! Меня зовут ЗдравоБот. Я помогу Вам ' \
        'вести здоровый образ жизни, а также дам несколько советов о правильном питании. ' \
        'Для начала давайте рассчитаем количество калорий, ' \
        'которое Вам стоит потреблять ежедневно. Для этого скажите "Рассчитать".'
        return
    #Рассчитать
    if 'счит' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'Введите свой пол, возраст, рост, вес, а также укажите степень ' \
        'Вашей физической активности через пробел, всё просто, ничего лишнего.\n1. Полное отсутствие ' \
        'физической активности.\n2. Небольшие пробежки или легкая ' \
        'гимнастика 1-3 раза в неделю.\n3. Средние нагрузки 3-5 раз в неделю.\n4. ' \
        'Полноценные тренировки 6-7 раз в неделю. \nВот так: Мужчина 24 186 72 2'
        return
    #Совет
    if 'совет' in req['request']['original_utterance'].lower():
        res['response']['text'] = '1. Следите за своим рационом, а также регялярностью питания.\n' \
        '2. Пейте достаточное количество воды.\n3. Перекусывайте правильно.\n4. ' \
        'Ешьте меньше сахара!\n 5. Питайтесь продуктыми, содержащие пищевые волокна.\n 6. Начинайте день с обильного завтрака.' \
        '\nДля дополнительной информации напишите номер совета.'
        return

    if  req['request']['original_utterance'] == '1':
        res['response']['text'] = 'Питание должно быть сбалансированным и включать ' \
        'белки, жиры, углеводы, витамины, макро- и микроэлементы. Оптимальный ежедневный рацион (по БМЖ) на 50% состоит ' \
        'из углеводов, на 25% — из белков и на 25% — из жиров. '
        res['response']['buttons'] = [
            {'title': "Что такое БМЖ?",  'hide': True}
        ]
        return

    if req['request']['original_utterance'] == '2':
        res['response']['text'] = 'Организм примерно на 60% состоит из воды. Она очень важна для нашего здоровья, '\
        'потому что вымывает токсины из органов, переносит питательные вещества в клетки, помогает переваривать пищу. Можно легко отслеживать уровень воды в организме через приложение.'
        res['response']['buttons'] = [
            {'title': "Чистая вода - лучший напиток!", "url": "https://apps.apple.com/ru/app/waterbalance/id517657679", 'hide': True}
        ]
        return

    if req['request']['original_utterance'] == '3':
        res['response']['text'] = 'Перекусывать надо только тогда, когда Вы действительно голодны. ' \
        'Исследование показало, что 55% испытуемых перекусывали из-за чувства искушения, а не потому что хотели есть. Для отличного перкуса подойдут: \n' \
        '• Белковые продукты — греческий йогурт, творог, сваренные вкрутую яйца, ломтик сыра. \n' \
        '• Орехи — отлично насыщают миндаль и арахис. \n' \
        '• Свежие овощи и фрукты, овощные салаты.\n• Тёмный шоколад с содержанием какао не менее 70%.'
        return

    if req['request']['original_utterance'] == '4':
        res['response']['text'] = 'Врачи-диетологи рекомендуют здоровым людям ограничивать употребление сахара: не больше 20-25 грамм в сутки. ' \
        'Но, по статистике, средняя норма его потребления в России – 107 грамм, в США – 160 грамм. Излишнее потребление сахара снижает иммунитет, а также повреждает прочность костных тканей.'
        return

    if req['request']['original_utterance'] == '5':
        res['response']['text'] = 'Чтобы в вашем меню было достаточно клетчатки, необходимой для нормального пищеварения, ' \
        'нужно есть как зерновые продукты, так и фрукты, овощи и ягоды. Сократите потребление продуктов из белой муки и ешьте больше ' \
        'цельнозерновых продуктов, богатых пищевыми волокнами и более полноценных.'
        return

    if req['request']['original_utterance'] == '6':
        res['response']['text'] = 'Ночью организм потребляет запасы углеводов, которые накопились в печени, ' \
        'и утром их следует восстановить. Если не есть завтрак, организм начнет разлагать собственные запасы, ' \
        'что может привести к снижению эффективности функционирования организма, например, снижению работоспособности, ' \
        'способности к обучению и концентрации внимания.'
        return
    #БМЖ
    if 'бмж' in req['request']['original_utterance'].lower():
        res['response']['text'] = 'БЖУ - это сокращнное название Белков, Жиров и ' \
        'Углеводов. Если хотите узнать о какой-то составляющей пищи поподробнее, то просто напишите её. '
        return

    if 'бел' in req['request']['original_utterance'].lower():
        res['response']['text'] = '• Белки - cтроительный материал организма, причём не только для клеток, но и для ферментов и гормонов. Белки бывают животными (постное мясо, рыба, ' \
            'яйца, молочные продукты) и растительными (фасоль, орехи, семена, брокколи, зелёный горошек, кукуруза). ' \
            'Желательно включать в рацион оба вида, потому что каждый содержит различные полезные вещества.'
        return

    if 'жир' in req['request']['original_utterance'].lower():
        res['response']['text'] = '• Жиры помогают усваивать витамины А, D и Е. Насыщенные жиры не навредят вам, если не превышать свою норму калорий. А вот трансжиров стоит избегать они увеличивают ' \
        'риск сердечно-сосудистых заболеваний. Этих веществ много в тортах, печенье и хлебе.'
        return

    if 'углевод' in req['request']['original_utterance'].lower():
        res['response']['text'] = '• Углеводы - главный поставщик энерги, сюда входят также клетчатка, витамины и минералы. Они часто сконцентрированы в богатых углеводами продуктах. ' \
        'Углеводы делятся на простые и сложные. Последние долго расщепляются и дают продолжительный заряд энергии. Простые углеводы быстро усваиваются и дают мгновенный приток энергии.'
        return
    #Факт
    if 'факт' in req['request']['original_utterance'].lower():
        bank = ['Острая пища продлевает жизнь.',
        'В лимонах больше сахара, чем в клубнике.',
        'В яичных желтках больше питательных веществ и минералов, чем в белках.',
        'В сладком перце больше витамина С, чем в цитрусовых.',
        'Морская соль ничем не отличается от обычной пищевой соли',
        'Помидоры теряют свой вкус при хранении в холодильнике.',]
        random_number = randint(0, len(bank)-1)
        res['response']['text'] = bank[random_number]
        return
    #Помощь
    if req['request']['original_utterance'].lower() in [
        'помощь',
        'что ты умеешь',
        'что ты умеешь?',
        'помоги',
    ]:
        res['response']['text'] = 'Дополнительную информацию о возможностях и реализации навыка можно найти по ссылке внизу.'
        res['response']['buttons'] = [
            {'title': "О навыке", "url": "https://github.com/mionitsa/yandex_healthyFood", 'hide': True}
        ]
        return

    if 'клик' in str(req['request']['original_utterance']).lower():
        res['response']['text'] = 'Вы можете спросить меня интересный факт о еде. Я знаю куча таких!'
        return

    if 'вода' in str(req['request']['original_utterance']).lower():
        res['response']['text'] = 'Эх... как жаль, что я не могу выпить воды, ведь я бот.'
        return

    if 'мужчина' in str(req['request']['original_utterance']).lower():
        req['request']['original_utterance'] = req['request']['original_utterance'].replace('.', ' ')
        req['request']['original_utterance'] = req['request']['original_utterance'].replace('-', ' ')
        req['request']['original_utterance'] = req['request']['original_utterance'].replace(',', ' ')

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
        res['response']['text'] = 'Вам нужно потреблять %s килокалорий в день. Для подсчёта калорий ' \
        'можно использовать удобное приложение.' % (
            str(int(kkal)))
        res['response']['buttons'] = [
            {'title': "Кликай!", "url": "https://apps.apple.com/ru/app/yazio-%D1%81%D1%87%D0%B5%D1%82%D1%87%D0%B8%D0%BA-%D0%BA%D0%B0%D0%BB%D0%BE%D1%80%D0%B8%D0%B9-%D0%B8-%D0%B4%D0%B8%D0%B5%D1%82%D0%B0/id946099227", 'hide': True}
        ]
        return

    if 'женщина' in str(req['request']['original_utterance']).lower():
        req['request']['original_utterance'] = req['request']['original_utterance'].replace('.', ' ')
        req['request']['original_utterance'] = req['request']['original_utterance'].replace('-', ' ')
        req['request']['original_utterance'] = req['request']['original_utterance'].replace(',', ' ')

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
        res['response']['text'] = 'Вам нужно потреблять %s килокалорий в день. Для подсчёта калорий ' \
        'можно использовать удобное приложение.' % (
            str(int(kkal)))
        res['response']['buttons'] = [
            {'title': "Кликай!", "url": "https://apps.apple.com/ru/app/yazio-%D1%81%D1%87%D0%B5%D1%82%D1%87%D0%B8%D0%BA-%D0%BA%D0%B0%D0%BB%D0%BE%D1%80%D0%B8%D0%B9-%D0%B8-%D0%B4%D0%B8%D0%B5%D1%82%D0%B0/id946099227", 'hide': True}
        ]
        return
    else:
        res['response']['text'] = 'Не совсем Вас понял, попробуйте вновь.'
        return
