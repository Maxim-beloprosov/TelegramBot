from aiogram import types
from server import dp

# Функция, обрабатывающая команду /start
@dp.message_handler(commands=["start"])
async def start(message):
    user_name = message.chat['first_name']
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("/Очень хочу посмотреть фильм!")
    item2 = types.KeyboardButton("/Готов пополнить список фильмов =)")
    markup.add(item1)
    markup.add(item2)
    await message.reply('Привет, ' + user_name + '! \n'
                                'Выбирай свой вариант. ', reply_markup=markup)
