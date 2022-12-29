from fw.db.db_base import connection
from random import randint

from fw.db.tables.table_users import get_full_name_user

name_database = 'films'

# Возвращаем всю информацию из таблицы films
def get_everybody_films():
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
    condition = f"where NOT user_id_recommended = {user_id}"
    count = get_count_string(condition)
    cursor = connection.cursor()
    random = randint(0, count - 1)
    cursor.execute(
        f"SELECT name, type, user_id_recommended FROM {name_database} " + condition
    )
    info_about_film = cursor.fetchall()
    info_about_film = info_about_film[int(random)]

    user_recommended = get_full_name_user(info_about_film[2])

    film = {
        'name': info_about_film[0],
        'type_film': info_about_film[1],
        'user_recommended': user_recommended
    }
    return film

# Возвращаем фильм с учетом фильтра
def get_film_with_filter_from_db(type_film, user_id_who_write_message, user_id_recommended=None):
    condition = f"NOT user_id_recommended = {user_id_who_write_message}"
    count = get_count_string_with_filter(type_film, condition, user_id_recommended)
    cursor = connection.cursor()
    if count > 1:
        random = randint(0, count - 1)
    elif count == 1:
        random = 0
    if user_id_recommended == None:
        cursor.execute(
            f"SELECT name, type, user_id_recommended FROM {name_database} "
            f"where type Like '%{type_film}%' and " + condition
        )
    else:
        cursor.execute(
            f"SELECT name, type, user_id_recommended FROM {name_database} "
            f"where type Like '%{type_film}%' and user_id_recommended = {user_id_recommended}"
        )
    if count == 1:
        info_about_film = cursor.fetchall()[0]
        user_recommended = get_full_name_user(info_about_film[2])
        film = {
            'name': info_about_film[0],
            'type_film': info_about_film[1],
            'user_recommended': user_recommended
        }
    else:
        info_about_film = cursor.fetchall()
        info_about_film = info_about_film[int(random)]
        user_recommended = get_full_name_user(info_about_film[2])
        film = {
            'name': info_about_film[0],
            'type_film': info_about_film[1],
            'user_recommended': user_recommended
        }
    return film

# Возвращаем количество строк из таблицы films с фильтром жанра и рекомендующего (если он есть)
def get_count_string_with_filter(type_film, condition, user_id_recommended=None):
    cursor = connection.cursor()
    if user_id_recommended == None:
        cursor.execute(
            f"SELECT count(*) FROM films "
            f"where type Like '%{type_film}%' and " + condition
        )
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
def get_name_film_which_is_recommended():
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT name FROM {name_database} "
    )
    return cursor.fetchall()