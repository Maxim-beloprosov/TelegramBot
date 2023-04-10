from fw.db.db_base import connection
from random import randint

from fw.db.tables.table_users import get_full_name_user

name_database = 'films'

# Возвращаем всю информацию из таблицы films
def get_all_information_from_table_films():
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM {name_database}"
    )
    return cursor.fetchall()

# Добавляем информацию о фильме в таблицу films
def add_info_about_film_in_table_films(name_film, type_film, user_id):
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO public.{name_database}(name, type, user_id_recommended) VALUES ('{name_film}', '{type_film}', '{user_id}');"
    )
    connection.commit()

# Возвращаем количество строк из таблицы films
def get_count_string(condition=''):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT count(*) FROM {name_database} " + condition
    )
    return cursor.fetchall()[0][0]

# Возвращаем рандомный фильм
def get_random_film(user_id):
    # Задаем условие, чтобы не рекомендовались фильмы от того пользователя, который запрашивает
    condition = f" where NOT user_id_recommended = {user_id}"
    # Получаем количество строк в таблице films с условием
    count = get_count_string(condition)
    cursor = connection.cursor()
    # Определяем рандомное число
    random = randint(0, count - 1)
    cursor.execute(
        f"SELECT name, type, user_id_recommended FROM {name_database} " + condition
    )
    info_about_film = cursor.fetchall()
    # Получаем информацию о фильме с рандомным номером
    info_about_film = info_about_film[int(random)]

    # Получаем полное имя рекомендателя
    user_recommended = get_full_name_user(info_about_film[2])

    # Формируем информацию о фильме в один json
    film = {
        'name': info_about_film[0],
        'type_film': info_about_film[1],
        'user_recommended': user_recommended
    }
    return film

# Возвращаем фильм с учетом фильтра
def get_film_with_filter_from_db(type_film, user_id_who_write_message, user_id_recommended=None):
    # Задаем условие
    condition = f" NOT user_id_recommended = {user_id_who_write_message}"
    # Получаем количество строк в таблице films с условием
    count = get_count_string_with_filter(type_film, condition, user_id_recommended)
    cursor = connection.cursor()

    # Проверяем, пришло ли условие на конкретного рекомендателя
    # Если не пришло, то формируем запрос на конкретный жанр и условие (не показывая фильмы того, кто запрашивает)
    if user_id_recommended == None:
        cursor.execute(
            f"SELECT name, type, user_id_recommended FROM {name_database} "
            f"where type Like '%{type_film}%' and " + condition
        )
    else:
        # Если пришло, то формируем запрос на конкретный жанр и конкретного пользователя
        cursor.execute(
            f"SELECT name, type, user_id_recommended FROM {name_database} "
            f"where type Like '%{type_film}%' and user_id_recommended = {user_id_recommended}"
        )

    # Проверяем на количество строк
    # Если пришла только 1 строка, то берем первый фильм
    if count == 1:
        info_about_film = cursor.fetchall()[0]
        # Получаем полное имя рекомендателя
        user_recommended = get_full_name_user(info_about_film[2])
        # Формируем информацию о фильме в один json
        film = {
            'name': info_about_film[0],
            'type_film': info_about_film[1],
            'user_recommended': user_recommended
        }
    # Если пришло больше одной строки, то используем рандом
    else:
        info_about_film = cursor.fetchall()
        random = randint(0, count - 1)
        info_about_film = info_about_film[int(random)]
        # Получаем полное имя рекомендателя
        user_recommended = get_full_name_user(info_about_film[2])
        # Формируем информацию о фильме в один json
        film = {
            'name': info_about_film[0],
            'type_film': info_about_film[1],
            'user_recommended': user_recommended
        }
    return film

# Возвращаем количество строк из таблицы films с фильтром жанра и рекомендующего (если он есть)
def get_count_string_with_filter(type_film, condition, user_id_recommended=None):
    cursor = connection.cursor()
    # Проверка, пришла ли информация о рекомендателе
    # Если не пришла, то формируем запрос на конкретный жанр и условие (не показывая фильмы того, кто запрашивает)
    if user_id_recommended == None:
        cursor.execute(
            f"SELECT count(*) FROM films "
            f"where type Like '%{type_film}%' and " + condition
        )
    # Если пришла, то формируем запрос на конкретный жанр и конкретного пользователя
    else:
        cursor.execute(
            f"SELECT count(*) FROM films "
            f"where type Like '%{type_film}%' and user_id_recommended = {user_id_recommended}"
        )
    return cursor.fetchall()[0][0]

# Возвращаем информацию о жанрах из таблицы films, которые рекомендовали
def get_type_which_is_recommended():
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT type FROM {name_database} "
    )
    return cursor.fetchall()

# Возвращаем информацию о названиях фильма из таблицы films, которые рекомендовали
def get_info_about_film_which_is_recommended():
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT name, type, user_id_recommended, id FROM {name_database} "
    )
    return cursor.fetchall()