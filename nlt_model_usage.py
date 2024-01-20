# -*- coding: utf-8 -*-
import pickle
import re
import string

from nltk.stem.wordnet import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk import FreqDist, classify, NaiveBayesClassifier
from nltk.tag import pos_tag


def remove_noise(tweet_tokens, stop_words=()):
    cleaned_tokens = []

    for token, tag in pos_tag(tweet_tokens, lang='rus'):
        token = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|' \
                       '(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', token)
        token = re.sub("(@[A-Za-z0-9_]+)", "", token)

        if tag.startswith("NN"):
            pos = 'n'
        elif tag.startswith('VB'):
            pos = 'v'
        else:
            pos = 'a'

        lemmatizer = WordNetLemmatizer()
        token = lemmatizer.lemmatize(token, pos)

        if len(token) > 0 and token not in string.punctuation and token.lower() not in stop_words:
            cleaned_tokens.append(token.lower())
    return cleaned_tokens

if __name__ == "__main__":
    classifier = NaiveBayesClassifier


    f = open('my_classifier.pickle', 'rb')
    classifier = pickle.load(f)
    f.close()

    custom_tweets = [
        "Как прекрасен этот день! Солнце светит ярко, птицы поют, и воздух наполнен ароматами цветов. Я полон энергии и готов сделать этот день незабываемым!",
        "Этот день просто ужасен. Солнце печет, птицы кричат, и воздух наполнен запахом выхлопных газов. Я устал и раздражен, и ничего не хочется делать.",
        "Счастье в моих руках – я только что стал обладателем нового телефона! Это невероятное чувство, когда ты держишь в руках технологическое чудо. Стильный дизайн, мгновенные реакции, кристально четкий экран – мой новый компаньон в повседневных приключениях.",
        "Спасибо большое за эти деньги",
        'Межгосударственный авиационный комитет опубликовал окончательный отчет по факту крушения вертолета санавиации «Ансат» в Городищенском районе Волгоградской области, произошедшего вечером 24 апреля 2023 года, сообщает V102.RU. В результате расследования были рассмотрены три версии авиационной аварии. Аналитиками изучались возможные причины, которые могли привести к падению вертолета и гибели пилота. По одной из версий, к катастрофе мог привести отказ системы управления воздушным судном.',
        '      В центре Волгограда 59-летняя женщина попала под колеса автомобиля. Как сообщили V102.RU в ГУ МВД по Волгоградской области, происшествие случилось накануне недалеко от остановки ЦПКиО.  59-летняя женщина перебегала дорогу по пешеходному переходу на запрещающий сигнал светофора. Спешка до добра не довела. Волгоградку сбила Лада Гранта под управлением 52-летнего водителя, который начал движение на разрешающий сигнал светофора.   Пешеход получила травмы и попала в больницу.  Видео ГУ МВД по Волгоградской области '
        ]
    sentiments = [
        "pos",  # "Just had an amazing experience with AwesomeServices, their customer support is top-notch!"
        "pos",  # "I can't believe the quality of the product I received from FantasticGoods, exceeded my expectations!"
        "pos",  # "Ordered from SuperQuickDelivery and got my package within hours. Impressed!"
        "neg",  # "Had a terrible experience with SlowServiceInc, will never use their services again."
        "neg",  # "In love with the new features of the latest app update. Great job, TechInnovators!"
        "neg",  # "Huge shoutout to DeliciousEats for the tasty food. Will definitely order again!"
    ]

    for i, tweet in enumerate(custom_tweets):
        custom_tokens = remove_noise(word_tokenize(tweet))
        print(f"{i + 1})\n\t{tweet}")
        print("\tPredict: ", classifier.classify(dict([token, True] for token in custom_tokens)))
        print(f"\tReal: {sentiments[i]}\n")
