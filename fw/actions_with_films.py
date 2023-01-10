# Проверяем, есть ли жанр в рекомендованных фильмах
from data.group_data import type_films
from fw.db.tables.table_films import get_type_which_is_recommended, add_info_about_film_in_table_films, get_info_about_film_which_is_recommended
from fw.db.tables.table_text_message_from_user import get_text_message_with_type_film
from fw.db.tables.table_users import get_full_name_user


# Получаем жанры, которые уже рекомендавали ранее
def get_type_films_in_db_films():
    # Получаем список жанров, которые уже рекомендовали
    type_films_which_recommended = get_type_which_is_recommended()
    # Создаем пустой список на будущее
    list_type_films = []
    # Перебираем все жанры
    for type_film in type_films:
        # Проверяем, есть ли жанр в списке рекомендованных
        if type_film in str(type_films_which_recommended):
            # Если есть - добавляем его
            list_type_films.append(type_film)
    return list_type_films

# Получаем жанры, которые уже рекомендовали ранее, без учета уже выбранного жанра
def get_type_films_without_type_which_user_select(user_id):
    # Получаем жанр, который пользователь уже выбирал
    type_films_which_user_select = get_text_message_with_type_film(user_id)
    # Создаем пустой список на будущее
    list_type_films = []
    # Перебираем все жанры
    for type_film in type_films:
        # Проверяем, соответствует ли жанр, который пользователь выбирал уже ранее с тем, который мы перебираем. Чтобы исключить и не показывать выбранный жанр снова
        if type_films_which_user_select != type_film:
            # Если не соответствует, добавляем его в список
            list_type_films.append(type_film)
    return list_type_films


# Записываем рекомендованный фильм в бд, если там его еще нет
def add_film_in_db(name_film, type_film, user_id):
    flag = True
    # Получаем информацию о фильмов
    name_films_which_recommended = get_info_about_film_which_is_recommended()
    for i in range(0, len(name_films_which_recommended)):
        if name_films_which_recommended[i][0].lower() == name_film.lower():
            flag = False
            count = i
            break
    if flag == True:
        add_info_about_film_in_table_films(name_film, type_film, user_id)
        return True
    else:
        user_recommended = get_full_name_user(name_films_which_recommended[count][2])
        result = {
            'name': name_films_which_recommended[count][0],
            'type_film': name_films_which_recommended[count][1],
            'user_recommended': user_recommended,
            'film_id': name_films_which_recommended[count][3]
        }
        return result
