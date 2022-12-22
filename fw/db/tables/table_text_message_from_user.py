from fw.db.db_base import connection

name_database = 'text_messages_from_user'


# Возвращаем всю информацию из таблицы text_message_from_user
def get_all_information_from_table():
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM {name_database}"
    )
    return cursor.fetchall()

# Записываем сообщение от пользователя в таблицу
def write_message_from_user_in_table(user_id, message_id, message_text):
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO public.{name_database}(user_id, message_id, message_text) VALUES ('{user_id}', '{message_id}', '{message_text}');"
    )
    connection.commit()

# Записываем сообщение от пользователя в таблицу с учетом жанра
def write_message_from_user_in_table_with_type_films(user_id, message_id, message_text, type_films):
    cursor = connection.cursor()
    cursor.execute(
        f"INSERT INTO public.{name_database}(user_id, message_id, message_text, type_films) VALUES ('{user_id}', '{message_id}', '{message_text}', '{type_films}');"
    )
    connection.commit()

# Возвращаем все сообщения от пользователя
def get_messages_from_user(user_id):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT message_text FROM {name_database} WHERE user_id = {user_id} "
        "order by message_id desc;"
    )
    return cursor.fetchall()


# Удаляем все сообщения от пользователя
def delete_all_messages_from_user(user_id):
    cursor = connection.cursor()
    cursor.execute(
        f"DELETE FROM public.{name_database} "
        f"where user_id = {user_id}"
    )
    connection.commit()

# Возвращаем текст последнего сообщения с жанром от пользователя
def get_text_message_with_type_film(user_id):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT type_films FROM {name_database} "
        f"WHERE user_id = {user_id} and type_films is not null "
        "order by message_id desc;"
    )
    type_film = cursor.fetchall()[0][0]
    return type_film

# Возвращаем id всех сообщений от пользователя с сортировкой по убыванию
def get_id_messages_from_user(user_id):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT message_id FROM {name_database} WHERE user_id = {user_id} "
        "order by message_id desc;"
    )
    return cursor.fetchall()

# Удаляем последнее сообщение от пользователя
def delete_last_messages_from_user(user_id):
    id_message = get_id_messages_from_user(user_id)[0][0]
    cursor = connection.cursor()
    cursor.execute(
        f"DELETE FROM public.{name_database} "
        f"where user_id = {user_id} and message_id = {id_message}"
    )
    connection.commit()