from fw.db.db_base import connection

name_database = 'users'


# Возвращаем всю информацию из таблицы users
def get_everybody_users():
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT * FROM {name_database}"
    )
    return cursor.fetchall()

# Проверяем, есть id пользователя в таблице users
def check_is_there_id_user_in_table_users(id):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT id FROM {name_database} "
        f"where id = {id}"
    )
    if cursor.fetchall() == []:
        # Если список приходит пустым, отправляем False
        return False
    else:
        # Если список не пустой, значит нужный id мы нашли и отправляем True
        return True

# Добавляем информацию о пользователе в таблицу users
def add_info_about_user_in_table_users(user_id, name, surname):
    cursor = connection.cursor()
    # Проверяем, нет ли такого пользователя уже в таблице users
    if check_is_there_id_user_in_table_users(user_id) == False:
        cursor.execute(
            f"INSERT INTO public.{name_database}(id, name, surname) VALUES ('{user_id}', '{name}', '{surname}');"
        )
        connection.commit()

# Возвращаем id юзера
def get_id_user(name, surname):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT id FROM {name_database} "
        f"where name = '{name}' and surname = '{surname}'"
    )
    return cursor.fetchall()[0][0]