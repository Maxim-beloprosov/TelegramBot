from fw.db.tables.table_films import get_film_with_filter_from_db
from fw.db.tables.table_users import get_id_user
from fw.db.tables.table_text_message_from_user import get_text_message_with_type_film

# Возвращаем фильм с учетом фильтра
def get_film_with_filter(user_id_who_write_message, full_name=None):
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