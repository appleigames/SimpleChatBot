import telebot
from telebot import types
from random import choice
import json

#JSON
with open('base.json', 'r', encoding='utf-8') as file:
    data = json.load(file)

def save_base():
    file = open('base.json', 'w', encoding='utf-8')
    json.dump(data, file, indent=4, ensure_ascii=False)
    file.close()


education_mode = False
math_mode = False
action: str
tag: str
ignore_symbols = ',."\'{}[]()!#$%^&*№;:?\\|/'


bot = telebot.TeleBot('7179420529:AAEOXaN8vYV5OVd4_OYDy7tK6hHGWxnTjL8')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, f'Дарова, {message.from_user.first_name}')


@bot.message_handler(commands=['developer', 'author'])
def developer(message):
    if message.from_user.id != 5105507379:
        bot.send_message(message.chat.id, 'Меня создал @AppleBox01')
    else:
        bot.send_message(message.chat.id, 'Ты мой создатель')


@bot.message_handler(commands=['stop'])
def developer(message):
    if message.from_user.id == 5105507379:
        bot.send_message(message.chat.id, 'Ты предал меня! Ублюдок!')
        bot.stop_bot()
    else:
        bot.send_message(message.chat.id, 'Ты меня не остановишь')


@bot.message_handler(commands=['help'])
def help(message):
    if message.from_user.id != 5105507379:
        bot.send_message(message.chat.id, 'Я короче бот.\nУмею разговаривать\nУ меня есть несколько <i>команд</i>:\n /start\n/help\n/developer\n/info\n/education\n/finish', 'html')
    else:
        bot.send_message(message.chat.id,'Я короче твой бот.\nУмею разговаривать\nУ меня есть несколько <i>команд</i>:\n /start\n/help\n/developer\n/info\n/education\n/finish', 'html')


@bot.message_handler(commands=['info'])
def info(message):
    bot.reply_to(message, f'Вот вся инфа о тебе:\nID: {message.from_user.id}\n'
                          f'Имя: {message.from_user.first_name}\n'
                          f'Фамилия: {message.from_user.last_name}\n'
                          f'Никнейм: {message.from_user.username}\n'
                          f'Являешься ты ботом: {message.from_user.is_bot}\n'
                          f'Премиум: {message.from_user.is_premium}\n'
                          f'Язык: {message.from_user.language_code}\n'
                          f'Бот может присоединяться к группам: {message.from_user.can_join_groups}\n'
                          f'Отключен режим конфиденциальности у бота: {message.from_user.can_read_all_group_messages}\n'
                          f'Бот поддерживает встроенные запросы: {message.from_user.supports_inline_queries}\n')


@bot.message_handler(commands=['math'])
def math(message):
    global math_mode
    if not education_mode:
        if not math_mode:
            math_mode = True
            bot.send_message(message.chat.id, 'Отправьте мне математическое выражение, я решу его... Наверное')
        else:
            bot.send_message(message.chat.id, 'Вы уже в режиме математики')
    else:
        bot.send_message(message.chat.id, 'Вы в режиме обучения')


@bot.message_handler(commands=['education'])
def education(message):
    global education_mode
    if not math_mode:
        if not education_mode:
            education_mode = True
            bot.send_message(message.chat.id, 'Обучение начато')
            bot.send_message(message.chat.id, 'Напишите "/choose"')
        else:
            bot.send_message(message.chat.id, 'Обучение уже начато')
    else:
        bot.send_message(message.chat.id, 'Вы в режиме математики')


@bot.message_handler(commands=['finish'])
def finish(message):
    global education_mode, action, math_mode
    if education_mode:
        education_mode = False
        action = ''
        bot.send_message(message.chat.id, 'Обучение завершено\nЕсли вы хотите продолжить обучение, напишите /education')

    elif math_mode:
        math_mode = False
        bot.send_message(message.chat.id, 'Вы вышли из режима математики')

    else:
        if message.from_user.id != 5105507379:
            bot.send_message(message.chat.id, 'Вы не вошли ни в один из режимов')
        else:
            bot.send_message(message.chat.id, 'Сначала войди в какой-нибудь режим, идиот!')


@bot.message_handler(commands=['choose'])
def choose(message):
    if education_mode:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton('Новый тег', callback_data='new_tag'))
        markup.add(types.InlineKeyboardButton('Редактировать тег', callback_data='edit_tag'))
        markup.add(types.InlineKeyboardButton('Закончить обучение', callback_data='finish'))
        bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=markup)
    else:
        bot.send_message(message.chat.id, 'Режим обучения не включен')


@bot.callback_query_handler(func=lambda callback: True)
def callback(callback):
    if callback.data == 'new_tag':
        new_tag(callback.message)

    elif callback.data == 'edit_tag':
        edit_tag(callback.message)

    elif callback.data == 'rename_tag':
        rename(callback.message)

    elif callback.data == 'edit_messages':
        add_message(callback.message)

    elif callback.data == 'edit_answers':
        add_answers(callback.message)

    elif callback.data == 'finish':
        finish(callback.message)

    else:
        bot.send_message(callback.message.chat.id, 'Произошла ошибка')


#Режим обучения
@bot.message_handler(commands=['new tag'])
def new_tag(message):
    global action
    if education_mode:
        action = 'new tag'
        bot.send_message(message.chat.id, 'Напишите мне новый тег')
    else:
        bot.send_message(message.chat.id, 'Режим обучения не включен')


@bot.message_handler(commands=['edit tag'])
def edit_tag(message):
    global action
    if education_mode:
        action = 'edit tag'
        bot.send_message(message.chat.id,'Напишите тег, который хотите редактировать')
    else:
        bot.send_message(message.chat.id, 'Режим обучения не включен')


def rename(message):
    global action
    action = 'rename tag'
    bot.send_message(message.chat.id, 'Напишите новое название тега')


def add_message(message):
    global action
    action = 'add messages'
    bot.send_message(message.chat.id, 'Напишите сообщение или сообщения(через точку с запятой), на которые я должен буду давать ответ')


def add_answers(message):
    global action
    action = 'add answers'
    bot.send_message(message.chat.id, 'Напишите сообщение или сообщения(через точку с запятой), которые я должен буду писать в ответ')


#Чат
@bot.message_handler()
def chat(message):
    global action
    if not education_mode and not math_mode:

        text = message.text.lower()
        text = text.translate(str.maketrans('', '', ignore_symbols))
        words = text.split()

        for i in data.keys():

            for word in words:

                if word in data[i]['messages']:
                    if i == 'hello' or i == 'bye':
                        bot.send_message(message.chat.id, choice(data[i]['answers']) + ', ' + message.from_user.first_name)
                    elif i == 'id':
                        bot.reply_to(message, f'Вот твой ID: {message.from_user.id}')
                    elif i == 'info':
                        info(message)
                    elif i == 'developer':
                        developer(message)
                    else:
                        bot.send_message(message.chat.id, choice(data[i]['answers']))

                    break


    elif education_mode:
        global tag
        if action == 'new tag' and message.text != '':
            tag = message.text
            data[tag] = {'messages': [], 'answers': []}
            add_message(message)

        elif action == 'edit tag' and message.text != '':
            tag = message.text.lower()
            if tag in data.keys():
                markup = types.InlineKeyboardMarkup()
                markup.add(types.InlineKeyboardButton('Изменить название', callback_data='rename_tag'))
                markup.add(types.InlineKeyboardButton('Изменить содержимое', callback_data='edit_messages'))
                markup.add(types.InlineKeyboardButton('Закончить обучение', callback_data='finish'))
                bot.send_message(message.chat.id, 'Что вы хотите сделать?', reply_markup=markup)

            else:
                bot.send_message(message.chat.id, 'Такого тега не существует')

        elif action == 'rename tag' and message.text != '':
            new_tag = message.text.lower()
            data[new_tag] = data.pop(tag)
            tag = ''
            save_base()
            finish(message)

        elif action == 'add messages' and message.text != '':
            messages = message.text.lower()
            messages = messages.split(';')
            for i in range(len(messages)):
                if messages[i][0] == ' ':
                    messages[i] = messages[i][1:]
            data[tag]['messages'] = messages
            add_answers(message)

        elif action == 'add answers' and message.text != '':
            answers = message.text
            answers = answers.split(';')
            for i in range(len(answers)):
                if answers[i][0] == ' ':
                    answers[i] = answers[i][1:]
            data[tag]['answers'] = answers
            tag = ''
            save_base()
            finish(message)

        else:
            if message.from_user.id != 5105507379:
                bot.send_message(message.chat.id, 'Ошибка')
            else:
                bot.send_message(message.chat.id, 'Ошибка. Чини меня, дебил')


    elif math_mode:
        if message.text != '/finish':
            math_exp = eval(message.text)
            bot.send_message(message.chat.id, math_exp)
            finish(message)


bot.polling(none_stop=True)
