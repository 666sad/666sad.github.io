import telebot
from telebot import types

TOKEN = '7493842537:AAEuXYsyg9k05E3t-nvcVrA0uLjfuSK3in8'
bot = telebot.TeleBot(TOKEN)
SUPPORT_USER_ID = 'Voricty'  # Замените на ID пользователя поддержки

# Состояние для отслеживания персональных заказов
user_states = {}

# Класс для хранения состояния пользователя
class UserState:
    def __init__(self):
        self.collecting_order = False

@bot.message_handler(commands=['start'])
def send_welcome(message):
    web_app_info = types.WebAppInfo(url="https://666sad.github.io/")  # URL вашего Web App
    markup = types.InlineKeyboardMarkup()
    button_catalog = types.InlineKeyboardButton('Каталог', web_app=web_app_info)
    button_personal_order = types.InlineKeyboardButton('Персональный заказ', callback_data='personal_order')
    button_ask_question = types.InlineKeyboardButton('Задать вопрос', url=f'https://t.me/{SUPPORT_USER_ID}')
    markup.add(button_catalog)
    markup.add(button_personal_order)
    markup.add(button_ask_question)
    bot.send_message(
        message.chat.id,
        "Здравствуйте! Добро пожаловать в онлайн-бутик элитных швейцарских часов V&S Time! "
        "У нас Вы найдете любые часы люкс-сегмента по лучшим ценам.",
        reply_markup=markup
    )

# Обработчик для начала сбора персонального заказа
@bot.callback_query_handler(func=lambda call: call.data == 'personal_order')
def personal_order_handler(call):
    chat_id = call.message.chat.id
    
    # Подготовка состояния пользователя
    user_states[chat_id] = UserState()
    user_states[chat_id].collecting_order = True
    
    markup = types.InlineKeyboardMarkup()
    button_upload_text = types.InlineKeyboardButton('Далее', callback_data='upload_text')
    markup.add(button_upload_text)
    
    bot.send_message(
        chat_id,
        "Цель функции «Персональный заказ» - возможность приобрести любые часы, которые Вы хотите. Это создаёт удобство и максимальную свободу для каждого нашего клиента. Пожалуйста, отправьте нам картинку часов, которые Вы бы хотели приобрести и нажмите кнопку «Далее». Если таковой у Вас нет, просто нажмите «Далее».",
        reply_markup=markup
    )

# Обработчик для кнопки "Загрузить текст"
@bot.callback_query_handler(func=lambda call: call.data == 'upload_text')
def upload_text_handler(call):
    chat_id = call.message.chat.id
    
    if chat_id in user_states and user_states[chat_id].collecting_order:
        bot.send_message(
            chat_id,
            "Здесь просим Вас подробно описать желаемые часы (бренд, модель, реф-номер, цвет и материал, размер и др.). Также просьба оставить Ваши контактные данные, чтобы наша команда могла связаться с Вами для уточнения всех деталей заказа."
        )

# Обработчик для сообщений от пользователя
@bot.message_handler(content_types=['photo', 'text'])
def collect_order_info(message):
    chat_id = message.chat.id
    
    if chat_id in user_states and user_states[chat_id].collecting_order:
        # Персональные заказы будут пересылаться в этот чат
        TARGET_CHAT_ID = '-4189468251'  # Замените YOUR_TARGET_CHAT_ID на ID чата, куда будут пересылаться заказы
        
        if message.content_type == 'photo':
            bot.forward_message(TARGET_CHAT_ID, chat_id, message.message_id)
        elif message.content_type == 'text':
            bot.forward_message(TARGET_CHAT_ID, chat_id, message.message_id)
            
            # Добавить финальное сообщение после сбора информации
            bot.send_message(
                chat_id,
                "Спасибо! Мы получили ваш заказ и свяжемся с вами в ближайшее время."
            )
            
            # Сброс состояния пользователя
            user_states[chat_id].collecting_order = False

# Запуск бота
bot.infinity_polling()