import telebot

bot = telebot.TeleBot('')
users = {}


@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.chat.id
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    get = telebot.types.KeyboardButton('Я в магазине!')
    send = telebot.types.KeyboardButton('Нужны продукты...')
    done = telebot.types.KeyboardButton('Всё куплено!')
    cancel = telebot.types.KeyboardButton('Отмени мой заказ...')
    etc = telebot.types.KeyboardButton('Что просили купить другие?')
    markup.add(get, send, done, cancel, etc)
    bot.send_message(user_id,
                     f'Добро пожаловать, {users[user_id][0]}!\nЯ - бот для покупок продуктов семьей '
                     f’Х.\nПоехали!',
                     reply_markup=markup)


@bot.message_handler(regexp='Я в магазине!')
def get_f(message):
    user_id = message.chat.id
    if users[209162838][1] or users[5281036062][1] or users[1624081542][1] or users[471463089][1]:
        for user in users:
            if user != user_id:
                if users[user][1]:
                    bot.send_message(user,
                                     f'{users[user_id][0]} сейчас в магазине.\nНапомню, ваш список покупок: "{', '.join(users[user][1])}"')
                else:
                    bot.send_message(user, f'{users[user_id][0]} сейчас в магазине!\nВы ничего не просили купить...')
            if users[user][1]:
                bot.send_message(user_id, f'{users[user][0]} просит купить: {', '.join(users[user][1])}')
            else:
                bot.send_message(user_id, f'{users[user][0]} ничего не просил купить...')
    else:
        bot.send_message(user_id, 'Никто ничего не просил, но я оповестил всех, что Вы в магазине...')


@bot.message_handler(regexp='Нужны продукты...')
def send_f(message):
    user_id = message.chat.id
    bot.send_message(user_id, 'Отправь список продуктов одним сообщением!')
    bot.register_next_step_handler(message, products_f)


@bot.message_handler(regexp='Всё куплено!')
def done_f(message):
    user_id = message.chat.id
    for user in users:
        if user != user_id:
            if users[user][1]:
                bot.send_message(user, f'{users[user_id][0]} купил то, что вы просили: "{', '.join(users[user][1])}"')
            else:
                bot.send_message(user, f'{users[user_id][0]} был в магазине, вы ничего не просили купить...')
        else:
            bot.send_message(user, 'Вы купили всё, что нужно.\nСпасибо!!!')
        users[user][1] = []


@bot.message_handler(regexp='Отмени мой заказ...')
def get_f(message):
    user_id = message.chat.id
    bot.send_message(user_id, f'Слушаюсь и повинуюсь...\nВаш заказ "{', '.join(users[user_id][1])}" отменён!')
    users[user_id][1] = []


@bot.message_handler(regexp='Что просили купить?')
def get_f(message):
    user_id = message.chat.id
    for user in users:
        if users[user][1]:
            if user != 1624081542:
                bot.send_message(user_id, f'{users[user][0]} просил купить: "{', '.join(users[user][1])}"')
            else:
                bot.send_message(user_id, f'{users[user][0]} просила купить: "{', '.join(users[user][1])}"')
        else:
            if user != 1624081542:
                bot.send_message(user_id, f'{users[user][0]} ничего не просил купить...')
            else:
                bot.send_message(user_id, f'{users[user][0]} ничего не просила купить...')


@bot.message_handler(content_types=['text'])
def products_f(message):
    user_id = message.chat.id
    users[user_id][1].append(message.text)
    bot.send_message(user_id, 'Записал!')


bot.infinity_polling()
