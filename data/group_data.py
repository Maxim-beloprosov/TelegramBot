
type_films = [
    'Боевик',
    'Комедия',
    'Мелодрама',
    'Детектив',
    'Драма',
    'Фантастика',
    'Исторический фильм',
    'Мультфильм',
    'Приключения',
    'Триллер',
    'Мюзикл',
    'Документальный фильм'
]

database = {
    'films': ['name', 'type', 'user_id_recommended', 'id'],
    'users': ['id', 'full_name', 'full_name_in_telegram'],
    'text_messages_from_user': ['user_id', 'message_id', 'message_text', 'type_films', 'user_id_for_recommended'],
    'users_recommended_films': ['user_id', 'film_id']
}