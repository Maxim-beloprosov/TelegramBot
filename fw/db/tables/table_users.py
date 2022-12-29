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
def add_info_about_user_in_table_users(user_id, full_name):
    cursor = connection.cursor()
    # Проверяем, нет ли такого пользователя уже в таблице users
    if check_is_there_id_user_in_table_users(user_id) == False:
        cursor.execute(
            f"INSERT INTO public.{name_database}(id, full_name, full_name_in_telegram) VALUES ('{user_id}', '{full_name}', '{full_name}');"
        )
        connection.commit()

# Возвращаем id юзера
def get_id_user(full_name):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT id FROM {name_database} "
        f"where full_name = '{full_name}'"
    )
    return cursor.fetchall()[0][0]

def get_full_name_user(user_id):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT full_name FROM {name_database} "
        f"where id = '{user_id}'"
    )
    result = cursor.fetchall()[0][0]
    return result