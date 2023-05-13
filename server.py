import datetime
import logging
from data.group_data import type_films
from aiogram import Bot, Dispatcher, executor, types
from config import API_TOKEN
from fw.actions_with_message import get_film_with_filter
from fw.actions_with_users import get_users_who_recommended_films
from fw.db.tables.table_text_message_from_user import write_message_from_user_in_table_with_type_films, write_message_from_user_in_table, get_messages_from_user, delete_all_messages_from_user, get_text_message_with_type_film
from fw.db.tables.table_films import get_random_film
from fw.db.db_base import get_users_who_recommended_with_correct_type_film
from fw.db.tables.table_user_recommended import add_info_about_user_in_table_user_recommended
from fw.db.tables.table_users import add_info_about_user_in_table_users, rename_user
from fw.actions_with_films import get_type_films_in_db_films, get_type_films_without_type_which_user_select, add_film_in_db, get_films_which_recommended

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)



# Функция, обрабатывающая команду /users
@dp.message_handler(commands=["users"])
async def users(message):
    users = get_users_who_recommended_films()
    # Формируем кнопки для выдачи пользователю
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/rename")
    item2 = types.KeyboardButton("/films")
    item3 = types.KeyboardButton("/end")
    markup.add(item1)
    markup.add(item2)
    markup.add(item3)
    await message.reply(users, reply_markup=markup)

@dp.message_handler(commands=["/обещаем_порекомендовать_фильмы"])
async def quiz_1(message):
    img = open('C:\\Users\\Administrator\\ChatBot\\data\\Картинка 2.jpg', 'rb')
    await message.reply('Привет! Минутка рекламы, куда без нее в наше время.\n'
                  'Вы знаете для чего данный бот?\n'
                  'Поднимите руку те, кто уже рекомендовал фильмы... Молодцы! А теперь постыдите тех людей, кто не рекомендовал =)\n'
                  'Я знаю, чем вы будете заниматься сегодня вечером или даже уже ночью, удачи! =)'
                  'РЕКЛАМА ЗАКОНЧИЛАСЬ d[-_-]b\n'
                  'Вот вам подсказка на следующий этап. Бегиииите ГЛУПЦЫ...')
    await bot.send_photo(message.chat.id, img)


@dp.message_handler(commands=["/будем_рекомендовать_фильмы"])
async def quiz_2(message):
    img = open('C:\\Users\\Administrator\\ChatBot\\data\\Картинка 1.jpg', 'rb')
    await message.reply('Привет!\n\n'
                        'Минутка рекламы, куда без нее в наше время.\n'
                        '"ООО Белопросовы"\n'
                        'Заветы Мичурина 3В\n'
                        'С любовью и уважением!\n\n'
                        'Вы знаете для чего данный бот?\n'
                        'Он решает великую проблему человечества, которая подразумевает под собой рекомендацию хороших (а может и лучших) фильмов от друзей для просмотра. ВОТ ТАК\n'
                        
                        'Поднимите руку те, кто уже рекомендовал фильмы... Молодцы! А теперь постыдите тех, кто не рекомендовал =)\n'
                        'Я знаю, чем вы будете заниматься сегодня вечером или даже уже ночью, удачи! =)\n'
                        'РЕКЛАМА ЗАКОНЧИЛАСЬ d[-_-]b\n\n'
                        'Вот вам подсказка на следующий этап. И помните, главное не куда, а главное - сколько фильмов ты порекомедовал друзьям! =*')
    await bot.send_photo(message.chat.id, img)


@dp.message_handler(commands=["films"])
async def films(message):
    # Формируем кнопки для выдачи пользователю
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/users")
    item2 = types.KeyboardButton("/end")
    markup.add(item1)
    markup.add(item2)
    films = get_films_which_recommended()
    await message.reply(films, reply_markup=markup)

@dp.message_handler(commands=["rename"])
async def rename(message):
    # Записываем сообщение от пользователя в базу данных
    write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
    # Удаляем все предыдущие кнопки
    a = types.ReplyKeyboardRemove()
    await message.reply('Давай переименуем пользователя. \n'
                        'Сначала укажи его имя и фамилию в телеграме, а через запятую укажи полное имя на русском языкe', reply_markup=a)

# Функция, обрабатывающая команду /start
@dp.message_handler(commands=["start"])
async def start(message):
    # 1 шаг
    # Записываем пользователя в базу данных users если он пишет впервые
    add_info_about_user_in_table_users(message.chat.id, message.chat['first_name'] + ' ' + message.chat['last_name'])
    # Формируем кнопки для выдачи пользователю
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Очень хочу посмотреть фильм!")
    item2 = types.KeyboardButton("Готов пополнить список фильмов =)")
    markup.add(item1)
    markup.add(item2)
    # Записываем сообщение от пользователя в базу данных
    write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
    # Проверка на ID Максима и Любаву Белопросовых
    if message.chat.id == 120642569 or message.chat.id == 182953665:
        item3 = types.KeyboardButton("/users")
        item4 = types.KeyboardButton("/films")
        markup.add(item3)
        markup.add(item4)
    # Отвечаем пользователю с новыми кнопками
    await message.reply('Привет, ' + message.chat['first_name'] + '! \n'
                                'Ты уже знаешь, хотел(а) бы ты быть полезен(на) друзьям или они тебе? =) ', reply_markup=markup)

@dp.message_handler(commands=["end"])
async def end(message):
    # Последний шаг
    # Записываем пользователя в базу данных users если он пишет впервые
    add_info_about_user_in_table_users(message.chat.id, message.chat['first_name'] + ' ' + message.chat['last_name'])
    # Получаю время сервера
    time = datetime.datetime.now().strftime("%H")
    # Формирую ответ исходя из времени
    if 5 <= int(time) <= 15:
        answer = 'Хорошего дня, '
    elif 16 <= int(time) <= 21:
        answer = 'Хорошего вечера, '
    elif 22 <= int(time) <= 23:
        answer = 'Доброй ночи, '
    elif 0 <= int(time) <= 5:
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
    # Формируем предпредпоследнее сообщение от пользователя, если оно есть
    if len(all_messages_from_user) > 2:
        text_before_and_before_last_message = all_messages_from_user[2][0]
    # Получаем жанры фильмов, которые рекомендовали
    type_films_which_recommended = get_type_films_in_db_films()
    if get_text_message_with_type_film != []:
        # Получаем жанры фильмов без жанра, который пользователь уже порекомендавал
        type_films_without_type_which_user_select = get_type_films_without_type_which_user_select(message.chat.id)
    # Записываем пользователя в базу данных users если он пишет впервые
    add_info_about_user_in_table_users(message.chat.id, message.chat['first_name'] + ' ' + message.chat['last_name'])

    # 2 шаг
    # Сценарий 1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
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
                            'Или ты готов(а) ответить на несколько вопросов?', reply_markup=markup)

    # 2 шаг
    # Сценарий 1.2 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
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

    # 3 шаг
    # Сценарий 1.1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text == 'Готов отдаться богу рандома! НЕ ВАЖНО, КАКОЙ ФИЛЬМ, ВАЖНО, КТО ЕГО ПОСОВЕТОВАЛ...' and text_last_message == 'Очень хочу посмотреть фильм!':
        # Берем рандомный фильм из списка фильмов в базе данных
        info_film = get_random_film(message.chat.id)
        # Записываем сообщение от пользователя в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Добавляем кнопку /end
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/end"))
        # Отвечаем пользователю с возможностью окончания диалога
        await message.reply('Отличный выбор! Вот тебе название фильма: \n\n'
                            f'<b>{info_film["name"]}</b> ({info_film["type_film"]}) \n'
                            f'Рекомендовал(а): {info_film["user_recommended"]} \n\n'
                            'Чтобы закончить этот приятный диалог нажми /end.  Приятного просмотра! =)'
                            , reply_markup=markup, parse_mode="html")

    # 3 шаг
    # Сценарий 1.1.2 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text == "Рандом не мой вариант, давай выберем фильм под мои пожелания..." and text_last_message == 'Очень хочу посмотреть фильм!':
        # Формируем кнопки для выдачи пользователю из списка жанров
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(0, len(type_films_which_recommended)):
            markup.add(types.KeyboardButton(type_films_which_recommended[i]))
        # Записываем сообщение от пользователя в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Отвечаем пользователю
        await message.reply('Фильм какого жанра ты хочешь посмотреть сегодня?', reply_markup=markup)

    # 3 шаг
    # Сценарий 1.2.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text in type_films and text_last_message == "Готов пополнить список фильмов =)":
        # Записываем сообщение от пользователя с учетом жанра
        write_message_from_user_in_table_with_type_films(message.chat.id, message.message_id, message.text, message.text)
        # Формируем кнопки для выдачи пользователю
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Достаточно. 1ого жанра хватит.")
        item2 = types.KeyboardButton("Недостаточно, нужно добавить еще 1 жанр.")
        markup.add(item1)
        markup.add(item2)
        # Отвечаем пользователю
        await message.reply('Достаточно ли указать один жанр у данного фильма?', reply_markup=markup)

    # 4 шаг
    # Сценарий 1.1.2.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text in type_films_which_recommended and text_last_message == "Рандом не мой вариант, давай выберем фильм под мои пожелания...":
        # Формируем кнопки для выдачи пользователю
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Хочу рекомендацию от конкретного друга!")
        item2 = types.KeyboardButton("Уверен в каждом из рекомендателей =)")
        markup.add(item1)
        markup.add(item2)
        # Записываем сообщение от пользователя с учетом жанра
        write_message_from_user_in_table_with_type_films(message.chat.id, message.message_id, message.text, message.text)
        # Отвечаем пользователю
        await message.reply('С жанром определились. \n'
                            'Давай теперь определимся, хочешь ли ты выбрать рекомендацию фильма от конкретного друга?', reply_markup=markup)

    # 4 шаг
    # Сценарий 1.2.1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text == 'Достаточно. 1ого жанра хватит.' and text_last_message in type_films:
        # Записываем сообщение от пользователя с учетом жанра
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Удаляем все предыдущие кнопки
        a = types.ReplyKeyboardRemove()
        # Отвечаем пользователю
        await message.reply('С жанром определились. \n'
                            'Теперь укажи название фильма...', reply_markup=a)

    # 4 шаг
    # Сценарий 1.2.1.2 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text == 'Недостаточно, нужно добавить еще 1 жанр.' and text_last_message in type_films:
        # Записываем информацию о фильме в базу films
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Формируем кнопки для выдачи пользователю из списка жанров
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        for i in range(0, len(type_films_without_type_which_user_select)):
            markup.add(types.KeyboardButton(type_films_without_type_which_user_select[i]))
        # Отвечаем пользователю
        await message.reply('Мы уже близки к концу... \n'
                            'Выбирай еще 1 жанр', reply_markup=markup)

    # 5 шаг
    # Сценарий 1.1.2.1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text == "Хочу рекомендацию от конкретного друга!" and text_last_message in type_films_which_recommended:
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

    # 5 шаг
    # Сценарий 1.1.2.1.2 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text == "Уверен в каждом из рекомендателей =)" and text_last_message in type_films_which_recommended:
        # Получаем фильм для рекомендации с учетом жанра и реомендующего
        info_film = get_film_with_filter(message.chat.id)
        # Записываем сообщение в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Формируем кнопки для выдачи пользователю
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/end"))
        # Отвечаем пользователю
        await message.reply('Спасибо за долгий путь со мной, вот тебе название фильма: \n\n'
                            f'<b>{info_film["name"]}</b> ({info_film["type_film"]}) \n'
                            f'Рекомендовал(а): {info_film["user_recommended"]} \n\n'
                            'Чтобы закончить этот приятный диалог нажми /end.  Приятного просмотра! =)'
                            , reply_markup=markup, parse_mode="html")


    # 5 шаг
    # Сценарий 1.2.1.1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif text_last_message == 'Достаточно. 1ого жанра хватит.' and text_before_last_message in type_films:
        # Записываем информацию о фильме в базу films
        result = add_film_in_db(message.text, text_before_last_message, message.chat.id)
        if result == True:
            # Формируем кнопки для выдачи пользователю
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("/end"))
            # Отвечаем пользователю
            await message.reply('Спасибо за рекомендацию фильма! \n'
                                'Благодаря тебе наш список пополняется =) \n'
                                'Чтобы закончить этот приятный диалог нажми /end. Приятного просмотра! =)', reply_markup=markup
                                )
        else:
            # Формируем кнопки для выдачи пользователю
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("/start"))
            markup.add(types.KeyboardButton("/end"))
            add_info_about_user_in_table_user_recommended(message.chat.id, result['film_id'])
            # Отвечаем пользователю
            # Проверяем, есть ли те, кто рекомендовали этот фильм, но не первыми
            if result['users_id_recommended'] == []:
                await message.reply('Спасибо, но кажется этот фильм уже порекомендовали! \n\n'
                                    f'<b>{result["name"]}</b> ({result["type_film"]}) \n'
                                    f'Рекомендовал(а): {result["user_recommended"]} \n\n'
                                    'Чтобы закончить этот приятный диалог нажми /end.  Приятного просмотра! =)', reply_markup=markup, parse_mode="html")
            else:
                await message.reply('Спасибо, но кажется этот фильм уже порекомендовали! \n\n'
                                    f'<b>{result["name"]}</b> ({result["type_film"]}) \n'
                                    f'Рекомендовали: {result["user_recommended"] + result["users_id_recommended"]} \n\n'
                                    'Чтобы закончить этот приятный диалог нажми /end.  Приятного просмотра! =)', reply_markup=markup, parse_mode="html")

    # 5 шаг
    # Сценарий 1.2.1.2.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text in type_films_without_type_which_user_select and text_last_message == 'Недостаточно, нужно добавить еще 1 жанр.':
        # Записываем сообщение от пользователя с учетом жанра
        write_message_from_user_in_table_with_type_films(message.chat.id, message.message_id, message.text, message.text)
        # Удаляем все предыдущие кнопки
        a = types.ReplyKeyboardRemove()
        # Отвечаем пользователю
        await message.reply('С жанром определились. \n'
                            'Теперь укажи название фильма...', reply_markup=a)

    # 6 шаг
    # Сценарий 1.1.2.1.1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text != "Подходящего рекомендателя, к сожалению, нет =(" and text_last_message == "Хочу рекомендацию от конкретного друга!":
        # Получаем фильм для рекомендации с учетом жанра и рекомендующего
        info_film = get_film_with_filter(message.chat.id, message.text)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/end"))
        # Записываем сообщение в базу данных
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Отвечаем пользователю
        await message.reply('Спасибо за долгий путь со мной, вот тебе название фильма: \n\n'
                            f'<b>{info_film["name"]}</b> ({info_film["type_film"]}) \n'
                            f'Рекомендовал(а): {info_film["user_recommended"]} \n\n'
                            'Чтобы закончить этот приятный диалог нажми /end.  Приятного просмотра! =)'
                            , reply_markup=markup, parse_mode="html")

    # 6 шаг
    # Сценарий 1.1.2.1.1.2 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif message.text == "Подходящего рекомендателя, к сожалению, нет =(" and text_last_message == "Хочу рекомендацию от конкретного друга!":
        # Получаем фильм для рекомендации с учетом жанра и реомендующего
        info_film = get_film_with_filter(message.chat.id)
        # Записываем сообщение в базу данныхият
        write_message_from_user_in_table(message.chat.id, message.message_id, message.text)
        # Формируем кнопки для выдачи пользователю
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("/end"))
        # Отвечаем пользователю
        await message.reply('Спасибо за долгий путь со мной, вот тебе название фильма: \n\n'
                            f'<b>{info_film["name"]}</b> ({info_film["type_film"]}) \n'
                            f'Рекомендовал(а): {info_film["user_recommended"]} \n\n'
                            'Чтобы закончить этот приятный диалог нажми /end.  Приятного просмотра! =)'
                            , reply_markup=markup, parse_mode="html")

    # 6 шаг
    # Сценарий 1.2.1.2.1.1 СЦЕНАРИЙ ОПИСАН В ФАЙЛЕ scenarios
    elif text_last_message in type_films and text_before_last_message == 'Недостаточно, нужно добавить еще 1 жанр.':
        # Записываем информацию о фильме в базу films
        result = add_film_in_db(message.text, text_before_and_before_last_message + ', ' + text_last_message, message.chat.id)
        if result == True:
            # Формируем кнопки для выдачи пользователю
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("/end"))
            # Отвечаем пользователю
            await message.reply('Спасибо за рекомендацию фильма! \n'
                                'Благодаря тебе наш список пополняется =) \n'
                                'Чтобы закончить этот приятный диалог нажми /end. Приятного просмотра! =)', reply_markup=markup
                                )
        else:
            # Формируем кнопки для выдачи пользователю
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            markup.add(types.KeyboardButton("/start"))
            markup.add(types.KeyboardButton("/end"))
            add_info_about_user_in_table_user_recommended(message.chat.id, result['film_id'])
            # Отвечаем пользователю
            # Проверяем, есть ли те, кто рекомендовали этот фильм, но не первыми
            if result['users_id_recommended'] == []:
                await message.reply('Спасибо, но кажется этот фильм уже порекомендовали! \n\n'
                                f'<b>{result["name"]}</b> ({result["type_film"]}) \n'
                                f'Рекомендовал(а): {result["user_recommended"]} \n\n'
                                'Чтобы закончить этот приятный диалог нажми /end.  Приятного просмотра! =)', reply_markup=markup, parse_mode="html")
            else:
                await message.reply('Спасибо, но кажется этот фильм уже порекомендовали! \n\n'
                                    f'<b>{result["name"]}</b> ({result["type_film"]}) \n'
                                    f'Рекомендовали: {result["user_recommended"] + result["users_id_recommended"]} \n\n'
                                    'Чтобы закончить этот приятный диалог нажми /end.  Приятного просмотра! =)', reply_markup=markup, parse_mode="html")

    # Обработчик ошибок, если вдруг пользователь случайно нажал 2 раза на кнопку
    # Проверяем, последнее сообщение такое же как и вновь поступившее
    elif message.text == text_last_message:
        # Отвечаем пользователю
        await message.reply('Кажется, кнопка нажалась 2 раза =( \n'
                            'Попробуй снова...')

    elif text_last_message == '/rename':
        info_name_user = message.text.split(',')
        actual_name = info_name_user[0]
        correct_name = info_name_user[1][1:]
        rename_user(actual_name, correct_name)
        # Отвечаем пользователю
        await message.reply('Все удалось, Ура! \n'
                            'Можешь проверить командой /users.')



    else:
        # Отвечаем пользователю
        await message.reply('Упс, такой вариант я не предусмотрел. \n'
                            'Попробуй заново, нажми /start')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
