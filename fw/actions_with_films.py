# Проверяем, есть ли жанр в рекомендованных фильмах
from data.group_data import type_films
from fw.db.tables.table_films import get_type_which_is_recommended


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
                # Проверяем, нет ли жанра уже в нашем списке, который мы формировали вначале
                if type_film not in list_type_films:
                    # Если нет - добавляем его
                    list_type_films.append(type_film)
                    break
    return list_type_films