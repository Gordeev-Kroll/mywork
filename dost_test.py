# -*- coding: utf-8 -*-
# tonality.py
import nltk
from dostoevsky.tokenization import RegexTokenizer
from dostoevsky.models import FastTextSocialNetworkModel
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

import fasttext

fasttext.FastText.eprint = lambda x: None

# Инициализация модели один раз
tokenizer = RegexTokenizer()
tokens = tokenizer.split('всё очень плохо')
model = FastTextSocialNetworkModel(tokenizer=tokenizer)


def analyze_tonality(text):
    results = model.predict([text], k=4)[0]

    # Используйте метод get() для безопасного доступа к значениям словаря
    formatted_results = {
        'Нейтрально': results.get('neutral', 0.0),
        'Негативно': results.get('negative', 0.0),
        'Позитивно': results.get('positive', 0.0),
        'Пропущено': results.get('skip', 0.0)
    }
    return formatted_results
