import telebot
import random
import time
from telebot import types

bot = telebot.TeleBot("7331775736:AAGC62Zw_JuzPtG9kqPyibnrqi2Aiiq1TRM")  # Замените "YOUR_BOT_TOKEN" на токен вашего бота


# Функция для генерации случайного текста с датой
def generate_signal():
    random_image = random.choice([
        "IMG/mines/1.jpg", "IMG/mines/2.jpg", "IMG/mines/3.jpg", "IMG/mines/4.jpg", "IMG/mines/5.jpg",
        "IMG/mines/6.jpg",
        "IMG/mines/7.jpg", "IMG/mines/8.jpg", "IMG/mines/9.jpg", "IMG/mines/10.jpg", "IMG/mines/11.jpg",
        "IMG/mines/12.jpg",
        "IMG/mines/13.jpg", "IMG/mines/14.jpg", "IMG/mines/15.jpg", "IMG/mines/16.jpg", "IMG/mines/17.jpg",
        "IMG/mines/18.jpg",
        "IMG/mines/19.jpg", "IMG/mines/20.jpg", "IMG/mines/21.jpg", "IMG/mines/22.jpg", "IMG/mines/23.jpg",
        "IMG/mines/24.jpg",
        "IMG/mines/25.jpg", "IMG/mines/26.jpg", "IMG/mines/27.jpg", "IMG/mines/28.jpg", "IMG/mines/29.jpg"
    ])
    current_date = time.strftime("%d.%m.%Y %H:%M")
    chance = random.uniform(65, 93)
    chance_str = f"{chance:.2f}%"
    return f"Game №{random.randint(100000, 999999)}\n\n{current_date}\n\nChance - {chance_str}", random_image


# Хранение данных о пользователях
users = {}


# Команда /start
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("🇷🇺 Russian", callback_data="ru"),
               types.InlineKeyboardButton("🇹🇷 Turkey", callback_data="tr"))
    bot.send_message(message.chat.id, "Select language", reply_markup=markup)


# Обработка кнопок выбора языка
@bot.callback_query_handler(func=lambda call: call.data in ["ru", "tr"])
def handle_language(call):
    # Вывод сообщения в зависимости от выбранного языка
    bot.delete_message(call.message.chat.id, call.message.message_id)
    global current_language
    current_language = call.data  # Сохраняем выбранный язык
    if current_language == "ru":
        main_menu(call.message)
    elif current_language == "tr":
        main_menu_tr(call.message)


# Функция для отображения главного меню (русский)
def main_menu(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📱РЕГИСТРАЦИЯ", callback_data="registration"))
    markup.add(types.InlineKeyboardButton("📚ИНСТРУКЦИЯ", callback_data="instruction"))
    markup.add(types.InlineKeyboardButton("💣ВЫДАТЬ СИГНАЛ💣", callback_data="signal"))

    text = """
    <b>Добро пожаловать в 🔸ABUZOK Mines🔸!</b>

    <i>💣Mines - это гэмблинг игра в букмекерской конторе 1win, которая основывается на классическом “Сапёре”.
    Ваша цель - открывать безопасные ячейки и не попадаться в ловушки.</i>

    <code>Наш бот основан на нейросети Chatgpt4</code>
    <code>Он может предугадать расположение звёзд с вероятностью 93%.</code>

    ❗️Бот работает корректно только с аккаунтами 1win, которые были зарегистрированы через раздел «регистрация» в боте❗️

    ✅После прочтения данного  сообщения, переходи в раздел регистрация, а далее в раздел инструкция.
    """

    bot.send_photo(message.chat.id, photo=open("IMG/abuz.jpg", 'rb'),
                   caption=text, reply_markup=markup, parse_mode='HTML')


def main_menu_tr(message):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📱KAYIT OL", callback_data="registration"))  # Registration
    markup.add(types.InlineKeyboardButton("📚TALİMATLAR", callback_data="instruction"))  # Instructions
    markup.add(types.InlineKeyboardButton("💣SİNYAL VER💣", callback_data="signal"))  # Give Signal

    text = """
       <b>🔸ABUZOK Mines🔸'e hoş geldiniz!</b>

       <i>💣Mines, klasik "Mayın Tarlası" oyununa dayalı olarak 1win bahis şirketinde oynanan bir kumar oyunudur.
       Amacınız, güvenli hücreleri açmak ve tuzaklardan kaçınmaktır. </i>


        <code>Botumuz, Chatgpt4 sinir ağı üzerine kuruludur.</code>
        <code>Yıldızların konumunu %93 olasılıkla tahmin edebilir.</code>

       ❗️Bot, yalnızca bottaki "kayıt" bölümünden kayıt olunan 1win hesaplarında düzgün çalışır❗️

       ✅Bu mesajı okuduktan sonra, kayıt bölümüne ve ardından talimatlar bölümüne gidin.
       """

    bot.send_photo(message.chat.id, photo=open("IMG/abuz.jpg", 'rb'),
                   caption=text, reply_markup=markup, parse_mode='HTML')


# Обработка callback запросов
@bot.callback_query_handler(func=lambda call: True)
def handle_callback(call):
    global users, current_language
    user_id = call.from_user.id
    chat_id = call.message.chat.id
    if call.data == "registration":
        if user_id in users:
            bot.delete_message(chat_id, call.message.message_id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton(
                "🤖Перерегистрация ID 1WIN" if current_language == "ru" else "🤖1WIN ID Yeniden Kaydı",
                callback_data="re_registration"))
            markup.add(types.InlineKeyboardButton("💣Выдача сигнала💣" if current_language == "ru" else "💣Sinyal Verme💣",
                                                  callback_data="signal"))
            markup.add(types.InlineKeyboardButton("🔙Главное меню" if current_language == "ru" else "🔙Ana Menü",
                                                  callback_data="main_menu"))
            bot.send_message(chat_id, f"Вы уже зарегистрированы!\n\nВаш ID: {users[user_id]}" if current_language == "ru" else f"Zaten kayıtlısınız.!\n\nSizin ID: {users[user_id]}",  reply_markup=markup)
        else:
            bot.delete_message(chat_id, call.message.message_id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("🔙Главное меню" if current_language == "ru" else "🔙Ana Menü",
                                                  callback_data="main_menu"))
            if current_language == "ru":
                # Текст под фото
                text = "🔷 1. Для начала зарегистрируйтесь по ссылке на сайте <a href='https://1wqsg.com/casino/list?open=register#zvcn'>1WIN (CLICK)</a> и добавьте промокод <b>«ABUZMINES»</b>.️\n\n"
                text += "🔷 2. После успешной регистрации cкопируйте ваш айди на сайте (Вкладка 'пополнение' и в правом верхнем углу будет ваш ID).\n\n"
                text += "🔷 3. И отправьте его боту в ответ на это сообщение! ️\n\n"
                bot.send_photo(chat_id, photo=open('IMG/reg.jpg', 'rb'),
                               caption=text, reply_markup=markup, parse_mode='HTML')
            elif current_language == "tr":
                text = "🔷 1. <a href='https://1wqsg.com/casino/list?open=register#zvcn'>1WIN (TIKLA)</a>  sitesindeki bağlantıdan kayıt olun ve " \
                       " <b>«ABUZMINES»</b> promosyon kodunu ekleyin.️\n\n"
                text += "🔷 2. Başarılı kayıt işleminden sonra, web sitenizdeki ID'nizi kopyalayın ('Para Yatırma' sekmesinde, sağ üst köşede ID'niz yer almaktadır).\n\n"
                text += "🔷 3. Ve bu mesajı yanıt olarak bot'a gönderin! \n\n"
                bot.send_photo(chat_id, photo=open('IMG/regt.jpg', 'rb'),
                               caption=text, reply_markup=markup, parse_mode='HTML')
    elif call.data == "re_registration":
        bot.delete_message(chat_id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("Регистрация" if current_language == "ru" else "Kayıt",
                                              callback_data="registration"))
        markup.add(types.InlineKeyboardButton("📱Главное меню" if current_language == "ru" else "📱Ana Menü",
                                              callback_data="main_menu"))
        bot.send_message(chat_id,
                         "Вы успешно удалили прошлый ID 1WIN\n\nПройдите регистрация заново" if current_language == "ru" else "Önceki 1WIN ID'nizi başarıyla sildiğiniz için teşekkür ederiz. \n\nLütfen yeniden kayıt olun",
                         reply_markup=markup)
        del users[user_id]
    elif call.data == "instruction":
        bot.delete_message(chat_id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🔙главное меню" if current_language == "ru" else "🔙Ana Menü",
                                              callback_data="main_menu"))
        if current_language == "ru":
            # Текст под фото
            text = "Бот основан и обучен на кластере нейросети 🖥 Chatgpt4.️\n\n"
            text += "Для тренировки бота было сыграно 🎰10.000+ игр.)\n\n"
            text += "Для получения максимального профита следуйте следующей инструкции: ️\n\n"
            text += "🟢 1. Пройти регистрацию в букмекерской конторе <a href='https://1wqsg.com/casino/list?open=register#zvcn'>1WIN (CLICK)</a> Если не открывается - заходим с включенным VPN (Швеция). В Play Market/App Store полно бесплатных сервисов, например: Vpnify, Planet VPN, Hotspot VPN и так далее! \n\n"
            text += "🟢 2. Пополнить баланс своего аккаунта используя промокод <b>ABUZMINES</b>, который даст +500% к депозиту.\n\n"
            text += "🟢 3. Перейти в раздел 1win games и выбрать игру 💣'MINES'.\n\n"
            text += "🟢 4. Выставить кол-во ловушек в размере трёх. Это важно!\n\n"
            text += "🟢 5. Запросить сигнал в боте и ставить по сигналам из бота.\n\n"
            text += "🟢 6. При неудачном сигнале советуем удвоить ставку что бы полностью перекрыть потерю при следующем сигнале.\n\n"
            text += "🟢 7. После выполнения данных шагов нажимайте на кнопку “выдать сигнал”\n\n"
            bot.send_photo(chat_id, photo=open('IMG/ins.jpg', 'rb'),
                           caption=text, reply_markup=markup, parse_mode='HTML')
        elif current_language == "tr":
            # Текст под фото
            text = "Bot, 🖥️ Chatgpt4 sinir ağı kümesi üzerinde eğitildi..️\n\n"
            text += "Botu eğitmek için 🎰10.000+ oyun oynandı.\n\n"
            text += "Maksimum kar elde etmek için aşağıdaki talimatları izleyin: ️\n\n"
            text += "🟢 1. <a href='https://1wqsg.com/casino/list?open=register#zvcn'>1WIN (CLICK)</a> bahis şirketinde kayıt olun. Açılmazsa VPN (İsveç) açıkken giriş yapın. Play Market/App Store'da Vpnify, Planet VPN, Hotspot VPN gibi birçok ücretsiz hizmet mevcut! \n\n"
            text += "🟢 2. Bakiyenizi <b>ABUZMINES</b> promosyon kodunu kullanarak doldurun, bu kod %500 depozito bonusu sağlayacaktır.\n\n"
            text += "🟢 3. 1win oyunlar bölümüne gidin ve 💣'MAYINLAR' oyununu seçin.\n\n"
            text += "🟢 4. Tuzağın sayısını üç olarak ayarlayın. Bu önemli!\n\n"
            text += "🟢 5. Bottan sinyal isteyin ve bottan gelen sinyallere göre bahis yapın.\n\n"
            text += "🟢 6. Sinyalleriniz yanlış çıkarsa, bir sonraki sinyalde kaybınızı tamamen kapatmak için bahsi ikiye katlamanızı öneririz.\n\n"
            text += "🟢 7. Bu adımları uyguladıktan sonra “sinyal ver” düğmesine basın”\n\n"
            bot.send_photo(chat_id, photo=open('IMG/inst.jpg', 'rb'),
                           caption=text, reply_markup=markup, parse_mode='HTML')
    elif call.data == "signal":
        if user_id in users:
            bot.delete_message(chat_id, call.message.message_id)
            # Отправляем сообщение "Получаю данные с сервера..."
            message_id = bot.send_message(chat_id,
                                          "Получаю данные с сервера..." if current_language == "ru" else "Sunucudan veri alıyorum...").message_id
            time.sleep(3)  # Пауза 3 секунды
            # Удаляем сообщение
            bot.delete_message(chat_id, message_id)
            # Генерируем и отправляем сигнал
            signal_text, random_image = generate_signal()
            photo = open(random_image, 'rb')
            markup = types.InlineKeyboardMarkup()
            markup.add(
                types.InlineKeyboardButton("💣Выдача сигнала💣" if current_language == "ru" else "💣SİNYAL GÖNDER💣",
                                           callback_data="signal"))
            markup.add(
                types.InlineKeyboardButton("❓Выбрать кол-во мин❓" if current_language == "ru" else "❓Mayın Sayısı Seç❓",
                                           callback_data="mines_count"))
            markup.add(types.InlineKeyboardButton("📱Главная" if current_language == "ru" else "📱Ana Menü",
                                                  callback_data="main_menu"))
            bot.send_photo(chat_id, photo, signal_text, reply_markup=markup)
        else:
            bot.delete_message(chat_id, call.message.message_id)
            markup = types.InlineKeyboardMarkup()
            markup.add(types.InlineKeyboardButton("📱Регистрация" if current_language == "ru" else "📱Kayıt",
                                                  callback_data="registration"))
            markup.add(types.InlineKeyboardButton("🔙Главное меню" if current_language == "ru" else "🔙Ana Menü",
                                                  callback_data="main_menu"))
            bot.send_message(chat_id,
                             "Для начала зарегистрируйтесь" if current_language == "ru" else "Kayıt olmanız gerekiyor",
                             reply_markup=markup)
    elif call.data == "mines_count":
        bot.delete_message(chat_id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("1 мин" if current_language == "ru" else "1 Tuzağı", callback_data="1_trap"))
        markup.add(
            types.InlineKeyboardButton("3 мин" if current_language == "ru" else "3 Tuzağı", callback_data="3_traps"))
        markup.add(
            types.InlineKeyboardButton("5 мин" if current_language == "ru" else "5 Tuzağı", callback_data="5_traps"))
        markup.add(
            types.InlineKeyboardButton("7 мин" if current_language == "ru" else "7 Tuzağı", callback_data="7_traps"))
        markup.add(types.InlineKeyboardButton("📱Главное меню" if current_language == "ru" else "📱Ana Menü",
                                              callback_data="main_menu"))
        bot.send_message(chat_id, "❓Выберите количество мин❓" if current_language == "ru" else "❓Mayın sayısını seçin❓",
                         reply_markup=markup)
    elif call.data in ["1_trap", "3_traps", "5_traps", "7_traps"]:
        bot.delete_message(chat_id, call.message.message_id)
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("💣Выдача сигнала💣" if current_language == "ru" else "💣SİNYAL GÖNDER💣",
                                              callback_data="signal"))
        markup.add(
            types.InlineKeyboardButton("❓Выбрать кол-во мин❓" if current_language == "ru" else "❓Mayın Sayısı Seç❓",
                                       callback_data="mines_count"))
        markup.add(types.InlineKeyboardButton("📱Главное меню📱" if current_language == "ru" else "📱Ana Menü📱",
                                              callback_data="main_menu"))
        bot.send_message(chat_id,
                         "Количество мин успешно изменено!" if current_language == "ru" else "Mayın sayısı başarıyla değiştirildi!",
                         reply_markup=markup)
    elif call.data == "main_menu":
        bot.delete_message(chat_id, call.message.message_id)
        if current_language == "ru":
            main_menu(call.message)
        elif current_language == "tr":
            main_menu_tr(call.message)
    else:
        pass


# Обработка сообщений от пользователя
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    global users, current_language
    user_id = message.from_user.id
    chat_id = message.chat.id
    if message.text.startswith("/start"):
        bot.delete_message(chat_id, message.message_id)
        start(message)
    elif message.text.isdigit() and not user_id in users:
        bot.delete_message(chat_id, message.message_id)
        users[user_id] = message.text
        markup = types.InlineKeyboardMarkup()
        markup.add(
            types.InlineKeyboardButton("❓Выбрать кол-во мин❓" if current_language == "ru" else "❓Mayın Sayısı Seç❓",
                                       callback_data="mines_count"))
        markup.add(types.InlineKeyboardButton("📱Главное меню" if current_language == "ru" else "📱Ana Menü",
                                              callback_data="main_menu"))
        bot.send_message(chat_id,
                         "Вы успешно прошли регистрацию" if current_language == "ru" else "Kayıt işleminiz tamamlandı.",
                         reply_markup=markup)
    elif user_id in users:
        bot.delete_message(chat_id, message.message_id)


# Запускаем бота
bot.polling(none_stop=True, interval=0)
