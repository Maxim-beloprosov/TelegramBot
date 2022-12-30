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
        # Проверяем, есть ли жанр в списке рекомендованных
        if type_film in str(type_films_which_recommended):
            # Если есть - добавляем его
            list_type_films.append(type_film)
    return list_type_films

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