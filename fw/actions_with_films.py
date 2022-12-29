# Проверяем, есть ли жанр в рекомендованных фильмах
from data.group_data import type_films
from fw.db.tables.table_films import get_type_which_is_recommended
from fw.db.tables.table_text_message_from_user import get_text_message_with_type_film


def get_type_films_in_db_films():
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
                # Проверяем, нет ли жанра уже в нашем списке, который мы формировали вначале
                if type_film not in list_type_films:
                    # Если нет - добавляем его
                    list_type_films.append(type_film)
                    break
    return list_type_films

def get_type_films_without_type_which_user_select(user_id):
    # Получаем жанр, который пользователь уже выбирал
    type_films_which_user_select = get_text_message_with_type_film(user_id)
    # Создаем пустой список на будущее
    list_type_films = []
    # Перебираем все жанры
    for type_film in type_films:
        if type_films_which_user_select != type_film:
            list_type_films.append(type_film)
    return list_type_films