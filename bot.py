import telebot
import config
from telebot import types

bot = telebot.TeleBot(config.TOKEN)
alphabet = 'абвгдеёжзийклмнопрстуфхцчшщъыьэюя'
original_string = ''
changed_string = ''
shift = 0
action = 0

@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    
    item1 = types.KeyboardButton("Зашифровать текст")
    item2 = types.KeyboardButton("Расшифровать текст")

    markup.add(item1, item2)

    sticker = open('stickers/welcome.webp', 'rb')
    bot.send_sticker(message.chat.id, sticker)
    bot.send_message(message.chat.id, "Добро пожаловать, {0.first_name}!\nЯ - {1.first_name}, бот для шифрования текста с помощью шифра Цезаря и его дешифрования\nПриятного пользования!)".format(message.from_user, bot.get_me()), parse_mode='html', reply_markup=markup)

@bot.message_handler(content_types=['text'])
def get_type_of_action(message):
    global action
    if message.text == 'Зашифровать текст':
        action = 1
        msg = bot.send_message(message.chat.id, "Введите слово или предложение, которое хотите зашифровать:")
        bot.register_next_step_handler(msg, get_string)
    elif message.text == 'Расшифровать текст':
        action = 2
        msg = bot.send_message(message.chat.id, "Введите слово или предложение, которое хотите расшифровать:")
        bot.register_next_step_handler(msg, get_string)
    else:
        bot.send_message(message.chat.id, "Я не знаю такой команды(")

def get_string(message):
    global original_string
    original_string = message.text.lower()
    msg = bot.send_message(message.chat.id, 'Введите сдвиг:')
    bot.register_next_step_handler(msg, get_shift)

def get_shift(message):
    global original_string
    global changed_string
    global shift
    global action
    shift = int(message.text)
    bot.send_message(message.chat.id, 'Отлично!\nРезультат:')
    changed_string = ''
    if action == 1:
        for i in range(len(original_string)):
            if alphabet.find(original_string[i]) != -1:
                for j in range(len(alphabet)):
                    if original_string[i] == alphabet[j]:
                        if j + shift > len(alphabet):
                            temp = 0 + (j + shift - len(alphabet))
                            changed_string += alphabet[temp]
                        else:
                            changed_string += alphabet[j + shift]
                        break
            else:
                changed_string += original_string[i]
    elif action == 2:
        for i in range(len(original_string)):
            if alphabet.find(original_string[i]) != -1:
                for j in range(len(alphabet)):
                    if original_string[i] == alphabet[j]:
                        if j - shift < 0:
                            temp = len(alphabet) - (j - shift + len(alphabet))
                            changed_string += alphabet[temp]
                        else:
                            changed_string += alphabet[j - shift]
                        break
            else:
                changed_string += original_string[i]
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    
    item1 = types.KeyboardButton("Зашифровать текст")
    item2 = types.KeyboardButton("Расшифровать текст")

    bot.send_message(message.chat.id, changed_string, reply_markup=markup)


bot.polling(none_stop=True)

