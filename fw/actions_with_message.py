from fw.db.tables.table_films import get_film_with_filter_from_db
from fw.db.tables.table_users import get_id_user
from fw.db.tables.table_text_message_from_user import get_text_message_with_type_film

# Возвращаем фильм с учетом фильтра
def get_film_with_filter(user_id_who_write_message, name_and_surname_user=None):
    if name_and_surname_user != None:
        # Разбиваем имя и фамилию
        name_and_surname_user = name_and_surname_user.split(' ')
        name = name_and_surname_user[0]
        surname = name_and_surname_user[1]

        # Получаем id пользователя через базу данных users, зная имя и фамилию
        user_id_recommended = get_id_user(name, surname)
    else:
        user_id_recommended = None

    # Получаем жанр из последних сообщений пользователя
    type_film = get_text_message_with_type_film(user_id_who_write_message)

    # Получаем фильм с учетом фильтра (Жанр и рекомендующий, если он есть)
    name_film = get_film_with_filter_from_db(type_film, user_id_recommended)

    return name_film