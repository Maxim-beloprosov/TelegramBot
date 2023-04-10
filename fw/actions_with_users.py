from fw.db.tables.table_users import get_everybody_users



# Получаем имена пользователей, которые рекомендовали фильмы
def get_users_who_recommended_films():
    users = ''
    list_users = get_everybody_users()
    for user in list_users:
        users = users + user[2] + '\n'
    return users