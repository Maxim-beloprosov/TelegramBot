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
    list_users = []
    for user in information_about_users:
        if user[0] not in list_users:
            list_users.append(user[0])

    return list_users