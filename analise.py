# -*- coding: utf-8 -*-
import pickle
import re
import string

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.tag import pos_tag

def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens, lang='rus'):
        # Удаление ссылок (URLs) из текста
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        # Удаление упоминаний пользователей (Twitter-логинов)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        # Определение части речи и лемматизация
        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        # Добавление очищенного токена в список
        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

def analise(newsInput):
    # Открытие файла с предварительно обученным классификатором
    f = open('C:/Users/artem/PycharmProjects/telegramBot/TonalityFromNLTK/my_classifier.pickle', 'rb')
    # Загрузка классификатора из файла
    classifier = pickle.load(f)
    f.close()

    # Подготовка входных данных: токенизация и удаление шума
    custom_news = remove_noise(word_tokenize(newsInput))

    # Применение классификатора для оценки вероятности классов
    prob_dist = classifier.prob_classify(dict([news, True] for news in custom_news))

    print("Probability of Positive:", prob_dist.prob("Позитивная"))
    print("Probability of Negative:", prob_dist.prob("Негативная"))

    # Возвращение класса с максимальной вероятностью
    return prob_dist.max()

if __name__ == "__main__":
    text = 'Сегодня удивительный день! Солнце светит ярко, небо ясное, и в воздухе витает аромат свежесваренного кофе. Улыбнитесь, ведь вокруг так много прекрасного: замечательные моменты, улыбки прохожих и вдохновляющие виды природы. Жизнь полна ярких впечатлений и радостных событий!'
    #text = 'Сегодня ужасный день. Серый и дождливый, словно отражение моего настроения. Всё идет не так, как хотелось бы, и кажется, что проблемы накапливаются, словно снежный ком. Почему все вокруг такие неприятные? И почему всегда происходят только плохие вещи?'
    some = analise(text)
    print(some)