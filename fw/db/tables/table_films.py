from fw.db.db_base import connection
from random import randint
from data.group_data import type_films

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
def get_count_string():
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT count(*) FROM {name_database}"
    )
    return cursor.fetchall()[0][0]

# Возвращаем рандомный фильм
def get_random_film():
    count = get_count_string()
    cursor = connection.cursor()
    random = randint(0, count - 1)
    cursor.execute(
        f"SELECT name FROM {name_database} "
    )
    return cursor.fetchall()[int(random)][0]

# Возвращаем фильм с учетом фильтра
def get_film_with_filter_from_db(type_film, user_id_recommended=None):
    count = get_count_string_with_filter(type_film, user_id_recommended)
    cursor = connection.cursor()
    if count > 1:
        random = randint(0, count - 1)
    elif count == 1:
        random = 0
    if user_id_recommended == None:
        cursor.execute(
            f"SELECT name FROM {name_database} "
            f"where type Like '%{type_film}%'"
        )
    else:
        cursor.execute(
            f"SELECT name FROM {name_database} "
            f"where type Like '%{type_film}%' and user_id_recommended = {user_id_recommended}"
        )
    if count == 1:
        name_film = cursor.fetchall()[0][0]
    else:
        name_film = cursor.fetchall()[int(random)][0]
    return name_film

# Возвращаем количество строк из таблицы films с фильтром жанра и рекомендующего (если он есть)
def get_count_string_with_filter(type_film, user_id_recommended=None):
    cursor = connection.cursor()
    if user_id_recommended == None:
        cursor.execute(
            f"SELECT count(*) FROM films "
            f"where type Like '%{type_film}%'"
        )
    else:
        cursor.execute(
            f"SELECT count(*) FROM films "
            f"where type Like '%{type_film}%' and user_id_recommended = {user_id_recommended}"
        )
    return cursor.fetchall()[0][0]

# Проверяем, есть ли жанр в рекомендованных фильмах
def check_type_films_in_db_films():
    # Получаем список жанров, которые уже рекомендовали
    type_films_which_recommended = get_type_which_is_recommended()
    # Создаем пустой список на будущее
    list_type_films = []
    # Перебираем все жанры
    for type_film in type_films:
        # Перебираем все жанры, которые уже рекомендовали
        for type_film_from_table_films in type_films_which_recommended:
            # Проверяем, есть ли жанр в списке рекомендованных
            if type_film in type_film_from_table_films:
                # Проверяем, есть ли жанр уже в нашем списке, который мы формировали вначале
                if type_film not in list_type_films:
                    # Если нет - добавляем его
                    list_type_films.append(type_film)
    return list_type_films

# Возвращаем информацию о жанрах из таблицы films, которые рекомендовали
def get_type_which_is_recommended():
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT type FROM {name_database} "
    )
    return cursor.fetchall()