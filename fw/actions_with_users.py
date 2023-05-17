from data.group_data import database
from fw.db.tables.table_users import get_everybody_users



# Получаем имена пользователей, которые рекомендовали фильмы
def get_users_who_recommended_films():
    users = ''
    list_users = get_everybody_users()
    for user in list_users:
        users = users + user[1] + ' - ' + user[2] + '\n'
    users = users + '\n' + 'Всего: ' + str(len(list_users))
    return users

def all_info_from_table_users():
    all_info = get_everybody_users()
    # Создаем пустой словарь
    users = {}
    users['items'] = {}
    # Задаем число для списка
    count = 1
    # Перебираем все строки из таблицы
    for user in all_info:
        users['items'][count] = {}
        # Перебираем все столбцы из таблицы
        for i in range(0, len(database['users'])):
            users['items'][count][database['users'][i]] = user[i]
        count = count + 1
    return users