from data.group_data import database
from fw.db.tables.table_films import get_film_with_filter_from_db
from fw.db.tables.table_user_recommended import get_all_info_from_table_users_recommended_films
from fw.db.tables.table_users import get_id_user
from fw.db.tables.table_text_message_from_user import get_text_message_with_type_film, get_all_information_from_table


# Возвращаем фильм с учетом фильтра
def get_film_with_filter(user_id_who_write_message, full_name=None):
    # Проверяем, пришла ли информация о полном имени пользователя
    if full_name != None:
        # Получаем id пользователя через базу данных users, зная полное имя
        user_id_recommended = get_id_user(full_name)
    else:
        user_id_recommended = None

    # Получаем жанр из последних сообщений пользователя
    type_film = get_text_message_with_type_film(user_id_who_write_message)

    # Получаем фильм с учетом фильтра (Жанр и рекомендующий, если он есть)
    info_about_film = get_film_with_filter_from_db(type_film, user_id_who_write_message, user_id_recommended)

    return info_about_film

def all_info_from_table_text_messages_from_user():
    all_info = get_all_information_from_table()
    # Создаем пустой словарь
    messages = {}
    messages['items'] = {}
    # Задаем число для списка
    count = 1
    # Перебираем все строки из таблицы
    for message in all_info:
        messages['items'][count] = {}
        # Перебираем все столбцы из таблицы
        for i in range(0, len(database['text_messages_from_user'])):
            messages['items'][count][database['text_messages_from_user'][i]] = message[i]
        count = count + 1
    return messages

def all_info_from_table_users_recommended_films():
    all_info = get_all_info_from_table_users_recommended_films()
    # Создаем пустой словарь
    recommendations = {}
    recommendations['items'] = {}
    # Задаем число для списка
    count = 1
    # Перебираем все строки из таблицы
    for recommendation in all_info:
        recommendations['items'][count] = {}
        # Перебираем все столбцы из таблицы
        for i in range(0, len(database['users_recommended_films'])):
            recommendations['items'][count][database['users_recommended_films'][i]] = recommendation[i]
        count = count + 1
    return recommendations