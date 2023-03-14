import time
from config import name, bot_name
from tts import say
from stt import listen
import os
import openai
import datetime

openai.api_key = "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"


def get_time():
    now = datetime.datetime.now()
    hours = now.hour
    minutes = now.minute
    time_str = f"{num2word(hours)} часов {num2word(minutes)} минут"
    text(time_str)


def num2word(num):
    ones = ['ноль', 'один', 'два', 'три', 'четыре', 'пять', 'шесть', 'семь', 'восемь', 'девять']
    teens = ['десять', 'одиннадцать', 'двенадцать', 'тринадцать', 'четырнадцать', 'пятнадцать', 'шестнадцать',
             'семнадцать', 'восемнадцать', 'девятнадцать']
    tens = ['двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят', 'семьдесят', 'восемьдесят', 'девяносто']
    if num < 10:
        return ones[num]
    elif num < 20:
        return teens[num - 10]
    elif num < 100:
        tens_index = num // 10 - 2
        ones_index = num % 10
        if ones_index == 0:
            return tens[tens_index]
        else:
            return f"{tens[tens_index]} {ones[ones_index]}"
    else:
        return str(num)


def question(quest):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"I'm a very smart {bot_name} question answering bot. If you ask me a question based on truth, I will give you an answer in two sentences. If you ask me a question that is nonsense, cheating, or doesn't have a clear answer, I will answer 'Unknown'. I will also translate the answer into Russian.Q:{quest}\nA:\n",
        max_tokens=200,
        n=1,
        temperature=0,
    )
    message = response.choices[0].text.strip()
    return message


def text(msg):
    say(msg)
    print(msg)


def hello(name):
    text(f'Здравствуйте, {name}!')


def call_me(name):
    words = list(query.split(' '))
    for word in range(len(words)):
        if words[word - 2] == "меня":
            name = words[word - 1]
    text(f'Здравствуйте, {name}!')


def call_bot(bot_name):
    words = list(query.split(' '))
    for word in range(len(words)):
        if words[word - 2] == "тебя":
            bot_name = words[word - 1]
    text(f"Да, можете обращаться ко мне {bot_name}")


def goodbye(name):
    text(f"Всего доброго, {name}!")


while True:
    query = listen()
    print(query)
    if bot_name in query:
        if "привет" in query:
            hello(name)
        elif "пока" in query:
            goodbye(name)
            break
        elif "зови меня" in query:
            call_me(name)
        elif "могу я звать тебя" in query:
            call_bot(bot_name)
        elif "сколько время" in query or "который час" in query:
            get_time()
        else:
            ans = question(query)
            text(ans)
