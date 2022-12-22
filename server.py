import logging
import datetime

from data.group_data import type_films
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN
from fw.actions_with_message import get_film_with_filter
from fw.db.tables.table_text_message_from_user import write_message_from_user_in_table_with_type_films, write_message_from_user_in_table, get_messages_from_user, delete_all_messages_from_user, delete_last_messages_from_user
from fw.db.tables.table_films import get_random_film, add_info_about_film_in_table_films, check_type_films_in_db_films
from fw.db.db_base import get_users_who_recommended_with_correct_type_film
from fw.db.tables.table_users import add_info_about_user_in_table_users

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


# Функция, обрабатывающая команду /start
@dp.message_handler(commands=["start"])
async def start(message):
    # Записываем пользователя в базу данных users если он пишет впервые
    add_info_about_user_in_table_users(message.chat.id, message.chat['first_name'], message.chat['last_name'])
    # Формируем кнопки для выдачи пользователю
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Очень хочу посмотреть фильм!")
    item2 = types.KeyboardButton("Готов пополнить список фильмов =)")
    markup.add(item1)
    markup.add(item2)
    # Записываем сообщение от пользователя в базу данных
    write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
    # Отвечаем пользователю с новыми кнопками
    await message.reply('Привет, ' + message.chat['first_name'] + '! \n'
                                'Ты уже выбрал, хочешь быть полезен друзьям или они тебе ? =) ', reply_markup=markup)

@dp.message_handler(commands=["end"])
async def end(message):
    # Записываем пользователя в базу данных users если он пишет впервые
    add_info_about_user_in_table_users(message.chat.id, message.chat['first_name'], message.chat['last_name'])
    # Получаю время сервера
    time = datetime.datetime.now().strftime("%H")
    # Формирую ответ исходя из времени
    if 6 <= int(time) <= 10:
        answer = 'Хорошего дня, '
    elif 11 <= int(time) <= 15:
        answer = 'Хорошего вечера, '
    elif 16 <= int(time) <= 21:
        answer = 'Доброй ночи, '
    elif 22 <= int(time) or int(time) <= 5:
        answer = 'Пока! И ложись уже спать, '
    # Удаляю все сообщения от пользователя из базы данных
    delete_all_messages_from_user(message.chat.id)
    # Формируем кнопки для выдачи пользователю
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(types.KeyboardButton("/start"))
    # Отвечаем пользователю
    await message.reply(answer + message.chat['first_name'] +'.\n'
                        'В дальнейшем для старта просто нажми /start\n'
                        'Жду тебя снова!', reply_markup=markup)



@dp.message_handler(content_types=["text"])
async def first_step_want_watch_film(message):
    # Получаем последнее сообщение от пользователя
    all_messages_from_user = get_messages_from_user(message.chat.id)
    # Формируем последнее сообщение от пользователя
    text_last_message = all_messages_from_user[0][0]
    # Формируем предпоследнее сообщение от пользователя, если оно есть
    if len(all_messages_from_user) > 1:
        text_before_last_message = all_messages_from_user[1][0]
    # Получаем жанры фильмов, которые рекомендовали
    type_films_which_recommended = check_type_films_in_db_films()
    # Записываем пользователя в базу данных users если он пишет впервые
    add_info_about_user_in_table_users(message.chat.id, message.chat['first_name'], message.chat['last_name'])

    # Сценарий 1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, новое сообщение соответствует ли кнопке в предыдущем шаге и было ли последнее сообщение от пользователя /start
    if message.text == 'Очень хочу посмотреть фильм!' and text_last_message == '/start':
        # Формируем кнопки для выдачи пользователю
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Готов отдаться богу рандома! НЕ ВАЖНО, КАКОЙ ФИЛЬМ, ВАЖНО, КТО ЕГО ПОСОВЕТОВАЛ...")
        item2 = types.KeyboardButton("Рандом не мой вариант, давай выберем фильм под мои пожелания...")
        markup.add(item1)
        markup.add(item2)
        # Записываем сообщение от пользователя в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Отвечаем пользователю с новыми кнопками
        await message.reply('Используем рандом? \n'
                            'Или ты готов ответить на пару/тройку вопросов?', reply_markup=markup)


    # Сценарий 1.2 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, новое сообщение соответствует ли кнопке в предыдущем шаге и было ли последнее сообщение от пользователя /start
    elif message.text == "Готов пополнить список фильмов =)" and text_last_message == '/start':
        # Формируем кнопки для выдачи пользователю из списка жанров
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(0, len(type_films)):
            markup.add(types.KeyboardButton(type_films[i]))
        # Записываем сообщение от пользователя в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Отвечаем пользователю с будущими кнопками
        await message.reply('Фильм какого жанра ты хочешь посоветовать друзьям? \n'
                            , reply_markup=markup)


    # Сценарий 1.1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, новое сообщение соответствует ли кнопке в предыдущем шаге и было ли последнее сообщение от пользователя 'Очень хочу посмотреть фильм!'
    elif message.text == 'Готов отдаться богу рандома! НЕ ВАЖНО, КАКОЙ ФИЛЬМ, ВАЖНО, КТО ЕГО ПОСОВЕТОВАЛ...' and text_last_message == 'Очень хочу посмотреть фильм!':
        # Берем рандомный фильм из списка фильмов в базе данных
        name_film = get_random_film()
        # Записываем сообщение от пользователя в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Добавляем кнопку /end
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/end"))
        # Отвечаем пользователю с возможностью окончания диалога
        await message.reply('Рандом так рандом, вот тебе название фильма: \n\n'
                            f'<b>{name_film}</b>\n\n'
                            'И наконец, чтобы закончить этот приятный диалог нажми /end ,пожалуйста! Удачи! =)'
                            , reply_markup=markup, parse_mode="html")

    # Сценарий 1.1.2 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, новое сообщение соответствует ли кнопке в предыдущем шаге и было ли последнее сообщение от пользователя 'Очень хочу посмотреть фильм!'
    elif message.text == "Рандом не мой вариант, давай выберем фильм под мои пожелания..." and text_last_message == 'Очень хочу посмотреть фильм!':
        # Формируем кнопки для выдачи пользователю из списка жанров
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(0, len(type_films_which_recommended)):
            markup.add(types.KeyboardButton(type_films_which_recommended[i]))
        # Записываем сообщение от пользователя в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        await message.reply('Фильм какого жанра ты хочешь посмотреть сегодня?', reply_markup=markup)


    # Сценарий 1.2.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, новое сообщение соответствует ли кнопке в предыдущем шаге и было ли последнее сообщение от пользователя "Готов пополнить список фильмов =)"
    elif message.text in type_films and text_last_message == "Готов пополнить список фильмов =)":
        # Записываем сообщение от пользователя с учетом жанра
        write_message_from_user_in_table_with_type_films(message.chat.id, message.message_id, message.text, message.text)
        # Удаляем все предыдущие кнопки
        a = types.ReplyKeyboardRemove()
        await message.reply('С жанром определились. \n'
                            'Теперь укажи название фильма...', reply_markup=a)



    # Сценарий 1.1.2.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, новое сообщение соответствует ли кнопке в предыдущем шаге и было ли последнее сообщение от пользователя "Рандом не мой вариант, давай выберем фильм под мои пожелания..."
    elif message.text in type_films_which_recommended and text_last_message == "Рандом не мой вариант, давай выберем фильм под мои пожелания...":
        # Формируем кнопки для выдачи пользователю
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Хочу рекомендацию от конкретного пользователя!")
        item2 = types.KeyboardButton("Уверен в каждом из рекомендателей =)")
        markup.add(item1)
        markup.add(item2)
        # Записываем сообщение от пользователя с учетом жанра
        write_message_from_user_in_table_with_type_films(message.chat.id, message.message_id, message.text, message.text)
        # Отвечаем пользователю
        await message.reply('С жанром определились. \n'
                            'Давай теперь определимся, хочешь ли выбрать фильм от какого-то конкретного человек?', reply_markup=markup)

    # Сценарий 1.2.1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, было ли предпоследнее сообщение от пользователя "Готов пополнить список фильмов =)" и было ли последнее сообщение от пользователя, с жанром фильма
    elif text_before_last_message == "Готов пополнить список фильмов =)" and text_last_message in type_films:
        # Записываем информацию о фильме в базу films
        add_info_about_film_in_table_films(message.text, text_last_message, message.chat.id)
        # Формируем кнопки для выдачи пользователю
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/end"))
        # Отвечаем пользователю
        await message.reply('Спасибо за рекомендацию фильма! \n'
                            'Благодаря тебе наш список пополняется =) \n'
                            'Чтобы закончить этот приятный диалог нажми /end ,пожалуйста! Удачи! =)', reply_markup=markup
                            )

    # Сценарий 1.1.2.1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, новое сообщение соответствует ли кнопке в предыдущем шаге и было ли последнее сообщение из списка жанров фильмов
    elif message.text == "Хочу рекомендацию от конкретного пользователя!" and text_last_message in type_films_which_recommended:
        # Формируем кнопки для выдачи пользователю из списка жанров
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # Получаем список пользователей, которые рекомендавали выбранный жанр
        list_user = get_users_who_recommended_with_correct_type_film(text_last_message)
        for i in range(0, len(list_user)):
            markup.add(types.KeyboardButton(list_user[i]))
        # Добавляем кнопку, если вдруг не нашелся нужный рекомендатель
        markup.add(types.KeyboardButton("Подходящего рекомендателя, к сожалению, нет =("))
        # Записываем сообщение в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Отвечаем пользователю
        await message.reply('Давай выберем рекомендателя из списка =) \n'
                            'НО, если подходящего рекомендателя нет, нажми кнопку:\n'
                            'Подходящего рекомендателя, к сожалению, нет =(', reply_markup=markup)

    # Сценарий 1.1.2.1.1.2 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, новое сообщение соответствует ли кнопке в предыдущем шаге и было ли последнее сообщение от пользователя 'Очень хочу посмотреть фильм!'
    elif message.text == "Уверен в каждом из рекомендателей =)" and text_last_message in type_films_which_recommended:
        # Получаем фильм для рекомендации с учетом жанра и реомендующего
        name_film = get_film_with_filter(message.chat.id)
        # Записываем сообщение в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Формируем кнопки для выдачи пользователю
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/end"))
        await message.reply('Спасибо за долгий путь со мной, вот тебе название фильма: \n\n'
                            f'<b>{name_film}</b>\n\n'
                            'И наконец, чтобы закончить этот приятный диалог нажми /end ,пожалуйста! Удачи! =)', reply_markup=markup, parse_mode="html"
                            )

    # Сцеарий 1.1.2.1.1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, данное сообщение (пользователь) есть ли в списке рекомендателей и было ли последнее сообщение от пользователя "Хочу рекомендацию от конкретного пользователя!"
    elif message.text != "Подходящего рекомендателя, к сожалению, нет =(" and text_last_message == "Хочу рекомендацию от конкретного пользователя!":
        # Получаем фильм для рекомендации с учетом жанра и рекомендующего
        name_film = get_film_with_filter(message.chat.id, message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/end"))
        # Записываем сообщение в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        await message.reply('Спасибо за долгий путь со мной, вот тебе название фильма: \n\n'
                            f'<b>{name_film}</b>\n\n'
                            'И наконец, чтобы закончить этот приятный диалог нажми /end ,пожалуйста! Удачи! =)', reply_markup=markup, parse_mode="html"
                            )

    # Сценарий 1.1.2.1.1.1.2 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    # Проверяем, новое сообщение соответствует ли кнопке в предыдущем шаге и было ли последнее сообщение от пользователя 'Очень хочу посмотреть фильм!'
    elif message.text == "Подходящего рекомендателя, к сожалению, нет =(" and text_last_message == "Хочу рекомендацию от конкретного пользователя!":
        # Получаем фильм для рекомендации с учетом жанра и реомендующего
        name_film = get_film_with_filter(message.chat.id)
        # Записываем сообщение в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Формируем кнопки для выдачи пользователю
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/end"))
        await message.reply('Спасибо за долгий путь со мной, вот тебе название фильма: \n\n'
                            f'<b>{name_film}</b>\n\n'
                            'И наконец, чтобы закончить этот приятный диалог нажми /end ,пожалуйста! Удачи! =)', reply_markup=markup, parse_mode="html"
                            )

    # Обработчик ошибок, если вдруг пользователь случайно нажал 2 раза на кнопку
    # Проверяем, последнее сообщение такое же как и вновь поступившее
    elif message.text == text_last_message:
        # Удаляем последнее сообщение из базы
        delete_last_messages_from_user(message.chat.id)
        await message.reply('Кажется, кнопка нажалась 2 раза =( \n'
                            'Попробуй снова...')


    else:
        await message.reply('Упс, такой вариант я не предусмотрел. \n'
                            'Попробуй заново, нажми /start')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
