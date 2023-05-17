from fw.db.db_base import connection

name_database = 'users_recommended_films'

# Добавляем информацию о пользователях, которые тоже рекомендовали фильм
def add_info_about_user_in_table_user_recommended(user_id, film_id):
    cursor = connection.cursor()
    # Проверяем, нет ли такой рекомендации от пользователя в базе
    if check_is_there_recommendation_in_table_users_recommended_films(user_id, film_id) == False:
        cursor.execute(
            f"INSERT INTO public.{name_database}(user_id, film_id) VALUES ('{user_id}', '{film_id}');"
        )
        connection.commit()

# Проверяем, есть ли в базе уже данная рекомендация от пользователя
def check_is_there_recommendation_in_table_users_recommended_films(user_id, film_id):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT user_id FROM {name_database} "
        f"where user_id = {user_id} and film_id = {film_id}"
    )
    # Проверяем, пришел ли ответ пустой или нет
    if cursor.fetchall() == []:
        # Если список приходит пустым, отправляем False
        return False
    else:
        # Если список не пустой, значит нужный id мы нашли и отправляем True
        return True

# Возвращаем всю информацию из таблицы users_recommended_films
def get_all_info_from_table_users_recommended_films():
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM {name_database}"
    )
    return cursor.fetchall()