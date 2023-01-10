import psycopg2
from config import host, user, password, db_name

connection = psycopg2.connect(
    host=host,
    user=user,
    password=password,
    database=db_name
)

# Возвращаем пользователей, которые рекомендовали фильмы
def get_users_who_recommended_with_correct_type_film(type):
    cursor = connection.cursor()
    cursor.execute(
        f"SELECT users.full_name "
        "FROM users "
        "INNER JOIN films ON users.id = films.user_id_recommended "
        f"where type Like '%{type}%';"
    )
    information_about_users = cursor.fetchall()
    # Формируем список на будущее
    list_users = []
    # Перебираем пользователей из рекомендателей
    for user in information_about_users:
        # Если пользователя нет в списке для выдачи, то добавляем его туда
        if user[0] not in list_users:
            list_users.append(user[0])

    cursor.execute(
        f"SELECT users_recommended_films.user_id FROM users_recommended_films "
        "INNER JOIN films ON users_recommended_films.film_id = films.id "
        f"where type Like '%{type}%';"
    )
    # Получаем информацию о пользователях, которые рекомендовали фильм, но не первые
    information_about_users_id = cursor.fetchall()

    if information_about_users_id != []:
        # Формируем тело для получения имен пользователей, которые рекомендовали фильм, но сделали это не первыми
        request = "SELECT full_name FROM users "
        for i in range(len(information_about_users_id[0])):
            request = request + f"where id = {information_about_users_id[0][i]} "

        cursor.execute(request)
        new_list_user = cursor.fetchall()
        # Перебираем пользователей из рекомендателей
        for user in new_list_user[0]:
            # Если пользователя нет в списке для выдачи, то добавляем его туда
            if user not in list_users:
                list_users.append(user)

    return list_users