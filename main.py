
# main.py
import telebot
from telebot import types
import random
import dost_test
import nltk_analysis
import rewriter
import summarizer
import tonality
from TonalityFromNLTK import analise
from auth_data import token
from models import News, PersonsToNews, PlacesToNews, session
import asyncio

import fasttext
from tonality_nltk import analyze_tonality_nltk

fasttext.FastText.eprint = lambda x: None

# Словарь для хранения идентификаторов новостей пользователя
user_news_dict = {}

# Создаем пустой список для хранения пользователей
users_list = set()

def process_news(news):
    news_text = f"{news.title}\nДата: {news.date}\nСсылка: {news.link}\n\n{news.description}"
    return news_text

def get_help_message():
    help_message = "Список доступных команд:\n"
    help_message += "/start - Начать взаимодействие с ботом\n"
    help_message += "/get_random - Получить случайную новость\n"
    help_message += "/get_news - Получить новость\n"
    help_message += "/show_five - Получить пять новостей\n"
    help_message += "/get_lastnews - Получить последнюю новость\n"
    help_message += "/get_firstnews - Получить первую новость\n"
    help_message += "/help - Показать список доступных команд\n"
    return help_message

def create_custom_keyboard():
    keyboard = types.ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
    btn_next_news = types.KeyboardButton("Очередная новость")
    btn_five_news = types.KeyboardButton("Пять новостей")
    keyboard.add(btn_next_news, btn_five_news)
    return keyboard

def create_inline_keyboard(news_id):
    keyboard = types.InlineKeyboardMarkup(row_width=1)  # Устанавливаем row_width=2
    btn_tonality = types.InlineKeyboardButton("Анализ тональности", callback_data=f'tonality_{news_id}')
    btn_summarizer = types.InlineKeyboardButton("Аннотация", callback_data=f'summarizer_{news_id}')
    btn_rewriter = types.InlineKeyboardButton("Переписанная новость", callback_data=f'rewriter_{news_id}')
    keyboard.add(btn_tonality)
    keyboard.add(btn_summarizer, btn_rewriter)  # Добавляем две кнопки в одну строку
    return keyboard

def telegram_bot(token):
    bot = telebot.TeleBot(token)

    @bot.message_handler(commands=["start"])
    def start_message(message):
        user_id = message.chat.id
        users_list.add(user_id)
        bot.send_message(message.chat.id, "Добро пожаловать в телеграм-бот новостного портала V102.RU", reply_markup=create_custom_keyboard())
        bot.send_message(message.chat.id, get_help_message())

    @bot.message_handler(commands=["help"])
    def help_command(message):
        bot.send_message(message.chat.id, get_help_message())

    @bot.message_handler(commands=["get_random"])
    def get_random(message):
        all_news = session.query(News).all()

        if all_news:
            random_news = random.choice(all_news)
            news_text = process_news(random_news)
            keyboard = create_inline_keyboard(random_news.id)
            bot.send_message(message.chat.id, news_text, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Новостей не найдено.")

    @bot.message_handler(commands=["get_news"])
    def get_news_command(message):
        user_id = message.chat.id

        if user_id not in user_news_dict:
            # If the user is using the command for the first time in this session
            first_news = session.query(News).order_by(News.id).first()

            if first_news:
                news_text = process_news(first_news)
                keyboard = create_inline_keyboard(first_news.id)
                bot.send_message(message.chat.id, news_text, reply_markup=keyboard)

                # Store the last displayed news ID for the user
                user_news_dict[user_id] = first_news.id

            else:
                bot.send_message(message.chat.id, "Новостей не найдено.")
        else:
            # If the user has used the command before, increase the news ID
            user_last_news_id = user_news_dict[user_id]
            next_news = session.query(News).filter(News.id > user_last_news_id).order_by(News.id).first()

            if next_news:
                news_text = process_news(next_news)
                keyboard = create_inline_keyboard(next_news.id)
                bot.send_message(message.chat.id, news_text, reply_markup=keyboard)

                # Update the last displayed news ID for the user
                user_news_dict[user_id] = next_news.id
            else:
                bot.send_message(message.chat.id, "Новостей не найдено.")

    @bot.message_handler(commands=["show_five"])
    def show_five_command(message):
        user_id = message.chat.id

        if user_id not in user_news_dict:
            # If the user is using the command for the first time in this session
            first_news = session.query(News).order_by(News.id).first()

            if first_news:
                news_text = process_news(first_news)
                keyboard = create_inline_keyboard(first_news.id)
                bot.send_message(message.chat.id, news_text, reply_markup=keyboard)

                # Store the last displayed news ID for the user
                user_news_dict[user_id] = first_news.id

            else:
                bot.send_message(message.chat.id, "Новостей не найдено.")
        else:
            # If the user has used the command before, fetch the next five news items
            user_last_news_id = user_news_dict[user_id]
            next_news_list = session.query(News).filter(News.id > user_last_news_id).order_by(News.id).limit(5).all()

            if next_news_list:
                for next_news in next_news_list:
                    news_text = process_news(next_news)
                    keyboard = create_inline_keyboard(next_news.id)
                    bot.send_message(message.chat.id, news_text, reply_markup=keyboard)

                    # Update the last displayed news ID for the user
                    user_news_dict[user_id] = next_news.id
            else:
                bot.send_message(message.chat.id, "Новостей не найдено.")

    @bot.message_handler(func=lambda message: message.text == "Очередная новость")
    def get_news_next(message):
        user_id = message.chat.id

        if user_id not in user_news_dict:
            # If the user is using the command for the first time in this session
            first_news = session.query(News).order_by(News.id).first()

            if first_news:
                news_text = process_news(first_news)
                keyboard = create_inline_keyboard(first_news.id)
                bot.send_message(message.chat.id, news_text, reply_markup=keyboard)

                # Store the last displayed news ID for the user
                user_news_dict[user_id] = first_news.id

            else:
                bot.send_message(message.chat.id, "Новостей не найдено.")
        else:
            # If the user has used the command before, increase the news ID
            user_last_news_id = user_news_dict[user_id]
            next_news = session.query(News).filter(News.id > user_last_news_id).order_by(News.id).first()

            if next_news:
                news_text = process_news(next_news)
                keyboard = create_inline_keyboard(next_news.id)
                bot.send_message(message.chat.id, news_text, reply_markup=keyboard)

                # Update the last displayed news ID for the user
                user_news_dict[user_id] = next_news.id
            else:
                bot.send_message(message.chat.id, "Новостей не найдено.")

    @bot.message_handler(func=lambda message: message.text == "Пять новостей")
    def get_five_command(message):
        user_id = message.chat.id

        if user_id not in user_news_dict:
            # If the user is using the command for the first time in this session
            first_news = session.query(News).order_by(News.id).first()

            if first_news:
                news_text = process_news(first_news)
                keyboard = create_inline_keyboard(first_news.id)
                bot.send_message(message.chat.id, news_text, reply_markup=keyboard)

                # Store the last displayed news ID for the user
                user_news_dict[user_id] = first_news.id

            else:
                bot.send_message(message.chat.id, "Новостей не найдено.")
        else:
            # If the user has used the command before, fetch the next five news items
            user_last_news_id = user_news_dict[user_id]
            next_news_list = session.query(News).filter(News.id > user_last_news_id).order_by(News.id).limit(5).all()

            if next_news_list:
                for next_news in next_news_list:
                    news_text = process_news(next_news)
                    keyboard = create_inline_keyboard(next_news.id)
                    bot.send_message(message.chat.id, news_text, reply_markup=keyboard)

                    # Update the last displayed news ID for the user
                    user_news_dict[user_id] = next_news.id
            else:
                bot.send_message(message.chat.id, "Новостей не найдено.")

    @bot.message_handler(commands=["remove_keyboard"])
    def remove_keyboard(message):
        bot.send_message(message.chat.id, "Кастомная клавиатура удалена.", reply_markup=types.ReplyKeyboardRemove())

    @bot.message_handler(commands=["get_lastnews"])
    def get_last_news_command(message):
        last_news = session.query(News).order_by(News.id).first()
        if last_news:
            news_text = process_news(last_news)
            keyboard = create_inline_keyboard(last_news.id)
            bot.send_message(message.chat.id, news_text, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Новостей не найдено.")

    @bot.message_handler(commands=["get_news_by_id"])
    def get_news_by_id_command(message):
        news_id = 7434  # Заменить на нужный айди
        news = session.query(News).filter_by(id=news_id).first()

        if news:
            news_text = process_news(news)
            keyboard = create_inline_keyboard(news.id)
            bot.send_message(message.chat.id, news_text, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, f"Новость с ID {news_id} не найдена.")

    @bot.message_handler(commands=["get_firstnews"])
    def get_first_news_command(message):
        first_news = session.query(News).order_by(News.id.desc()).first()
        if first_news:
            news_text = process_news(first_news)
            keyboard = create_inline_keyboard(first_news.id)
            bot.send_message(message.chat.id, news_text, reply_markup=keyboard)
        else:
            bot.send_message(message.chat.id, "Новостей не найдено.")


    @bot.callback_query_handler(func=lambda call: call.data.startswith(('tonality_', 'summarizer_', 'rewriter_')))
    def callback_handler(call):
        operation, news_id = call.data.split('_')

        last_news = session.query(News).filter_by(id=news_id).first()

        if last_news:
            chat_id = call.message.chat.id

            persons_record_exists = session.query(PersonsToNews).filter_by(id_news=last_news.id).first()
            places_record_exists = session.query(PlacesToNews).filter_by(id_news=last_news.id).first()

            if operation == 'tonality':
                if persons_record_exists or places_record_exists:
                    person_name = persons_record_exists.person if persons_record_exists else ""
                    place_name = places_record_exists.places if places_record_exists else ""

                    tonality_result = dost_test.analyze_tonality(last_news.text)
                    tonality_result3 = analise.analise(last_news.text)


                    # Форматирование строки для вывода в желаемом формате
                    result_message = f"Найдено: {person_name} {place_name}\n" \
                                     f"Оценка тональности новости (Dostoevsky):\n" \
                                     f"Нейтрально {tonality_result['Нейтрально']:.4f}\n" \
                                     f"Негативно {tonality_result['Негативно']:.4f}\n" \
                                     f"Позитивно {tonality_result['Позитивно']:.4f}\n\n" \
                                     f"Оценка тональности новости (nltk): {tonality_result3}"


                    bot.send_message(chat_id, result_message, reply_to_message_id=call.message.message_id)

                else:
                    bot.reply_to(call.message, "Эта новость не содержит информацию о влиятельных персонах или достопримечательностях Волгоградской области")
            elif operation == 'summarizer':
                summarized_text = asyncio.run(summarizer.summarize(last_news.text))
                bot.send_message(chat_id, f"Аннотация: {summarized_text}",
                                 reply_to_message_id=call.message.message_id)
            elif operation == 'rewriter':
                rewrited_text = asyncio.run(rewriter.rewrite(last_news.text))
                bot.send_message(chat_id, f"Переписанная новость: {rewrited_text}", reply_to_message_id=call.message.message_id)
        else:
            bot.send_message(call.message.chat.id, "Новости не найдено.")

    bot.polling()

if __name__ == '__main__':
    telegram_bot(token)