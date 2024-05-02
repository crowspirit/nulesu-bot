import telebot
from telebot import types
import config
from data import *
import os
from parser_z import *
import traceback
import sqlite3
# from GPT_request import request
from time import sleep
import io

def get_group_id(user):
    try:
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Виконуємо запит для отримання group за user_id
        cursor.execute("SELECT groups_name FROM users WHERE user_id = ?", (user,))
        result = cursor.fetchone()

        # Закриваємо з'єднання
        conn.close()

        group = result[0]
        return group
    except:
        return None

def get_teacher(user):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Виконуємо запит для отримання group за user_id
    cursor.execute("SELECT nick_name FROM users WHERE user_id = ?", (user,))
    result = cursor.fetchone()

    # Закриваємо з'єднання
    conn.close()

    teacher = result[0]
    return teacher == "teacher"



# def parse_groups(): #повертає кортеж груп та кількості користувачів в групах
#     groups = {}
#     with open("Users.txt", "r", encoding="UTF-8") as file:
#         for user in file.readlines():
#             with open(f"Users/{user[:-1]}/{user[:-1]}_group.txt") as group:
#                 gr = group.readline()
#                 if not gr in groups:
#                     groups[gr] = 1
#                 else:
#                     groups[gr] += 1
#     return (groups)
def parse_group(user):#повертає групу студента за його tg-id
    with open(f"Users/{user}/{user}_group.txt") as file:
        return file.readline()

# def parse_user():
#     text = ''
#     with open("Users.txt","r",encoding="UTF-8") as file:
#         for user in file.readlines():
#             if not '-' in user:
#                 try:
#                     chat_member = bot.get_chat_member(chat_id=user, user_id=user)
#                     text += parse_group(user[:-1]) + " - "
#                     text += user[:-1] + " - "
#                     text += str(chat_member.user.first_name) + " - "
#                     text += str(chat_member.user.last_name) + " - @"
#                     text += str(chat_member.user.username) + "\n"
#                 except Exception as e:
#                     print(e)
#                     text += user[:-1] + " - ban\n"

#         return(text)

markup_menu = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_menu_admin = types.ReplyKeyboardMarkup(resize_keyboard=True)
markup_menu_abiturient = types.ReplyKeyboardMarkup(resize_keyboard=True)
buttons = types.KeyboardButton(text="Заміни")
buttons1 = types.KeyboardButton(text="Розклад")
buttons3 = types.KeyboardButton(text="Викладачі")
button_register = types.KeyboardButton(text="Реєстрація")
button_file = types.KeyboardButton(text="/file")
button_weather = types.KeyboardButton(text="Погода")
button_response = types.KeyboardButton(text="Відгук")
button_news = types.KeyboardButton(text="/новини")
button_number_of_users = types.KeyboardButton(text="/користувачі")
button_game = types.KeyboardButton(text="Game")
button_info = types.KeyboardButton(text="Про коледж")
button_rozsulka = types.KeyboardButton(text="/розсилка")
button_all_info_users = types.KeyboardButton(text="/all_users")



markup_menu_admin.add(buttons,buttons1,button_game)
markup_menu_admin.add(button_weather,button_response,buttons3)
markup_menu_admin.add(button_register)
markup_menu_admin.add(button_file,button_number_of_users, button_all_info_users)
markup_menu_admin.add(button_news, button_rozsulka)



markup_menu.add(buttons,buttons1,button_game)
markup_menu.add(button_weather,button_response,buttons3)
markup_menu.add(button_register)

markup_menu_abiturient.add(button_info,buttons3)
markup_menu_abiturient.add(button_weather,button_response)
markup_menu_abiturient.add(button_register)


teachers_by_department = {
    "Відділення заг. підготовки": ["Шапілова Катерина Петрівна","Черняк Руслана Олегівна","Лисяк Оксана Миколаївна","Гринкевич Ірина Володимирівна","Мазепа Олександр Миколайович","Музичук Ірина Володимирівна","Сорока Мирослава Василівна","Талімончук Олександр Григорович","Троцюк Вікторія Віталіївна","Коняхін Юрій Олександрович","Гуменюк Валерій Дмитрович","Тригубець Лариса Романівна","Капітула Ігор Карпович","Петрівська Людмила Олексіївна","Юхимчук Юлія Петрівна","Шалапенко Олексій Ігорович","Грицик Тетяна Андріївна","Зіняч Вікторія Вікторівна","Рафальський Олег Антонович","Христянович Володимир Миколайович","Дячук Валерій Петрович","Бойко Людмила Анатоліївна","Лидич Володимир Адамович","Свінтозельський Назар Віталійович"],
    "Відділення програмування": [ "Якимчук Ірина Олександрівна", "Куделя Оксана Олексіївна", "Собко Валентина Григорівна", "Кот Василь Васильович","Матвійчук Тетяна Адамівна","Масталярчук Євгеній Володимирович","Панасюк Василь Олексійович","Новіцький Сергій Броніславович","Стрик Павло Миколайович","Нікітська Оксана Віталіївна","Черняк Тетяна Григорівна","Кондюк Сергій Миколайович","Бабич Сергій Васильович","Надозірний Святослав Вікторович","Черняк Вадим Андрійович","Дедюхіна Юлія Олександрівна"],
    "Відділення технічне": ["Люльчик Вадим Олександрович","Качановський Олег Ігорович","Русіна Неля Григорівна","Бусленко Галина Михайлівна","Малимон Стефанія Стефанівна","Петрова Ольга Миколаївна","Кийко Неля Миколаївна","Рудько Ольга Миколаївна","Кушнірук Олександр Миколайович","Біда Петро Іванович","Сасовський Тарас Анатолійович","Павленко Олександр Іванович","Масюк Григорій Харитонович","Шалай Сергій Васильович","Сафонов Генадій Ігнатович","Петриковська Алла Анатоліївна","Свінтозельський Віктор Петрович","Іванченко Анатолій Миронович","Грищук Юрій Миколайович","Сорока Тетяна Петрівна","Медвідь Михайло Михайлович","Шаперчук Степан Віталійович","Ковальчук Сергій Васильович","Масло Ольга Андріївна","Чорна Ірина Василівна"],
    "Відділення економічне": ["Царук Василь Юрійович","Корсун Ярослав Петрович","Мартинова Ірина Миколаївна","Балдич Людмила Володимирівна","Бондарчук Ірина Павлівна","Конончук Оксана Миколаївна","Матвійчук Любов Анатоліївна","Немкович Оксана Борисівна","Обарчук Елліна Всеволодівна","Пастушенко Наталія Володимирівна","Прончук Людмила Василівна","Чернега Ірина Григорівна","Познаховський Віктор Анатолійович","Гнатюк Алла Аркадіївна","Плахтій Тетяна Федорівна","Моцнюк Віта Юріївна","Кучерук Олена Миколаївна","Черначук Оксана Олександрівна"],
    "Відділення Юридичне": ["Хряпченко Валентина Павлівна","Іванців Михайло Романович","Ільїн Вадим Анатолійович","Захарчук Володимир Михайлович","Басюк Оксана Петрівна","Купчишина Тетяна Володимирівна","Лук'янчук Світлана Василівна","Матковська Ірина Дмитрівна","Навозняк Людмила Михайлівна","Чорнобрива Ольга Вікторівна","Гулюк Сергій Іванович"]
}
workbook = openpyxl.load_workbook('schedule.xlsx')
GROUPS = workbook.sheetnames
group_by_department = {
    "Загальноосвітнє відділення":["11-О","11-Ф","11-П","11-М","11-З","11-Б","11-Д","12-Д","11-Ю","12-Ю","13-ЮЗ","11-ІП","12-ІП","13-ІП","11-К","12-К"],
    "Відділення програмування": ["21-К","22-К","21-ІП","22-ІП","23-ІП","31-ІП","32-ІП","33-ІП","41-ІП","42-ІП","43-ІП"],
    "Економічне відділення": ["21-О","31-О","32-О","21-П","31-П","21-Ф","31-Ф","21-М","31-М","41-М"],
    "Будівельне відділення": ["21-Б","22-Б","31-Б","32-Б","41-Б","21-Д","22-Д","31-Д","32-Д","41-Д"],
    "Земельно-правове відділення": ["21-Ю","22-Ю","31-Ю","32-Ю","41-Ю","21-З","22-З","21-ДЗ","31-З","32-З","41-З"]
}


bot = telebot.TeleBot(config.TOKEN)
bot.send_message(config.Admin, 'БОТ ЗАПУЩЕН')



try:

# -----------------------------------Реєстрація-------------------------------

    @bot.message_handler(func=lambda message: message.text =="Реєстрація" or message.text =="/start")
    def info(message):
        try:
            if "-" in str(message.chat.id):
                return
            # log(message)
            # keyboard = types.InlineKeyboardMarkup()
            # button = types.InlineKeyboardButton(text="Студент", callback_data="rigester_student")
            # keyboard.add(button)
            # button = types.InlineKeyboardButton(text="Викладач", callback_data="rigester_teacher")
            # keyboard.add(button)
            # # button = types.InlineKeyboardButton(text="Викладач", callback_data="rigester_teacher")
            # # keyboard.add(button)
            # with open("sticker.webp","rb") as sticker_file:
            #     sticker = sticker_file.read()
            # bot.send_sticker(message.chat.id,sticker)
            # bot.send_message(message.chat.id, "Привіт! Я бот, який допоможе вам бути в курсі вашого розкладу та будь-яких змін у ньому. \nВиберіть хто ви.",reply_markup=keyboard)
            keyboard = types.InlineKeyboardMarkup()
            for department in group_by_department.keys():
                button = types.InlineKeyboardButton(text=department, callback_data=f"r_s_d_{department}")
                keyboard.add(button)
            with open("sticker.webp","rb") as sticker_file:
                sticker = sticker_file.read()
            bot.send_sticker(message.chat.id,sticker)
            mess = bot.send_message(chat_id=message.chat.id, text="Привіт! Я бот, який допоможе вам бути в курсі вашого розкладу та будь-яких змін у ньому. \nВиберіть своє відділення.")
            bot.edit_message_reply_markup(chat_id=message.chat.id,message_id=mess.message_id, reply_markup=keyboard)


            # for department in group_by_department.keys():
            #     button = types.InlineKeyboardButton(text=department, callback_data=department+"_Groups")
            #     keyboard.add(button)

            # if os.path.exists(os.path.join("Users",str(message.chat.id), str(message.chat.id)+".txt")):
            #     with open(os.path.join("Users",str(message.chat.id), str(message.chat.id)+".txt"), "w") as f:
            #         f.write("REG_0")
            #         log(message,"Новий користувач ("+str(message.chat.id)+")")
            #         with open("sticker.webp","rb") as sticker_file:
            #             sticker = sticker_file.read()
            #         bot.send_sticker(message.chat.id,sticker)
            #         bot.send_message(message.chat.id, "Привіт! Я бот, який допоможе вам бути в курсі вашого розкладу та будь-яких змін у ньому. \nВиберіть своє відділення.",reply_markup=keyboard)
            # else:
            #     os.mkdir("Users/"+str(message.chat.id))
            #     print("Файл не знайдено в папці")
            #     with open(os.path.join("Users",str(message.chat.id), str(message.chat.id)+".txt"), "w") as f:
            #         f.write("REG_0")
            #         log(message,"Новий користувач ("+str(message.chat.id)+")")
            #         with open("sticker.webp","rb") as sticker_file:
            #             sticker = sticker_file.read()
            #         bot.send_sticker(message.chat.id,sticker)
            #         bot.send_message(message.chat.id, "Привіт! Я бот, який допоможе вам бути в курсі вашого розкладу та будь-яких змін у ньому. \nВиберіть своє відділення.",reply_markup=keyboard)
        except Exception as e:
            print("ERROR "+str(e))
    @bot.callback_query_handler(func=lambda call: call.data == "rigester_student")
    def handle_teachers_callback(call):
        try:
            keyboard = types.InlineKeyboardMarkup()
            for department in group_by_department.keys():
                button = types.InlineKeyboardButton(text=department, callback_data=f"r_s_d_{department}")
                keyboard.add(button)
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Привіт! Я бот, який допоможе вам бути в курсі вашого розкладу та будь-яких змін у ньому. \nВиберіть своє відділення.")
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=keyboard)

        #     elif "r_s_d" in call.data:
        #         keyboard = types.InlineKeyboardMarkup()
        #         department = call.data.split("_")[-1]
        #         print("111")
        #         buttons_per_row = 4 # кількість кнопок у рядку
        #         buttons = [] # список кнопок
        #         for i in group_by_department[department]:
        #             button = types.InlineKeyboardButton(i, callback_data=f"register_student_group_{i}")
        #             if len(buttons) == 0 or len(buttons[-1]) == buttons_per_row: # якщо останній рядок заповнений
        #                 buttons.append([button]) # створимо новий рядок і додамо кнопку в нього
        #             else:
        #                 buttons[-1].append(button)
        #         keyboard = types.InlineKeyboardMarkup(buttons)
        #         bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Привіт! Я бот, який допоможе вам бути в курсі вашого розкладу та будь-яких змін у ньому. \nВиберіть свою групу.")
        #         bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=keyboard)
        #     elif "register_student_group" in call.data:
        #         keyboard = types.InlineKeyboardMarkup()
        #         mess = bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Увведіть своє Ім'я.")
        #         bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=keyboard)
        #         bot.register_next_step_handler(mess, register,call.data.split("_")[-1])
        #     elif call.data == "rigester_teacher":
        #         pass
        except Exception as e:
            print("ERROR "+str(e))
    @bot.callback_query_handler(func=lambda call: "r_s_d" in call.data)
    def handle_teachers_callback(call):
        keyboard = types.InlineKeyboardMarkup()
        department = call.data.split("_")[-1]
        buttons_per_row = 4 # кількість кнопок у рядку
        buttons = [] # список кнопок
        for i in group_by_department[department]:
            button = types.InlineKeyboardButton(i, callback_data=f"register_student_group_{i}")
            if len(buttons) == 0 or len(buttons[-1]) == buttons_per_row: # якщо останній рядок заповнений
                buttons.append([button]) # створимо новий рядок і додамо кнопку в нього
            else:
                buttons[-1].append(button)
        keyboard = types.InlineKeyboardMarkup(buttons)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Привіт! Я бот, який допоможе вам бути в курсі вашого розкладу та будь-яких змін у ньому. \nВиберіть свою групу.")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: "register_student_group" in call.data)
    def handle_teachers_callback(call):
        # keyboard = types.InlineKeyboardMarkup()
        mess = bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Уведіть своє Ім'я.")
        # bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        bot.register_next_step_handler(mess, register_student,call.data.split("_")[-1])


    def register_student(message, group):
        add_or_update_user(str(message.chat.id), message.text, group, message)
        print(f"register - {str(message.chat.id)} - {message.text} - {group}")
        with open("sticker_ok.webp","rb") as sticker_file:
            sticker = sticker_file.read()
        bot.send_sticker(message.chat.id,sticker)
        if str(message.chat.id) == Admin:
            bot.send_message(message.chat.id, f"Вітаю! Ви зареєструвались під групою {group} та ім'ям {message.text}. Відтепер ви кожен день будете отримувати розклад та заміни. Якщо у вас виникне якась помилка чи побажання, можете відправити нам відгук. \nДля зміни групи натисніть /start, або кнопку Реєстрація", reply_markup=markup_menu_admin)
        else:
            bot.send_message(message.chat.id, f"Вітаю! Ви зареєструвались під групою {group} та ім'ям {message.text}. Відтепер ви кожен день будете отримувати розклад та заміни. Якщо у вас виникне якась помилка чи побажання, можете відправити нам відгук. \nДля зміни групи натисніть /start, або кнопку Реєстрація", reply_markup=markup_menu)

    @bot.callback_query_handler(func=lambda call: call.data == "rigester_teacher")
    def handle_teachers_callback(call):
        try:
            keyboard = types.InlineKeyboardMarkup()
            for department in teachers_by_department.keys():
                button = types.InlineKeyboardButton(text=department, callback_data=f"r_s_t_{department}")
                keyboard.add(button)
            bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Привіт! Я бот, який допоможе вам бути в курсі вашого розкладу та будь-яких змін у ньому. \nВиберіть своє відділення.")
            bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=keyboard)
        except Exception as e:
            print("ERROR "+str(e))

    @bot.callback_query_handler(func=lambda call: "r_s_t" in call.data)
    def handle_teachers_callback(call):
        keyboard = types.InlineKeyboardMarkup()
        department = call.data.split("_")[-1]
        buttons_per_row = 1 # кількість кнопок у рядку
        buttons = [] # список кнопок
        for i in teachers_by_department[department]:
            button = types.InlineKeyboardButton(i, callback_data=f"register_teacher_name_{i.split()[0]} {i.split()[1][0]}.")
            if len(buttons) == 0 or len(buttons[-1]) == buttons_per_row: # якщо останній рядок заповнений
                buttons.append([button]) # створимо новий рядок і додамо кнопку в нього
            else:
                buttons[-1].append(button)
        keyboard = types.InlineKeyboardMarkup(buttons)
        bot.edit_message_text(chat_id=call.message.chat.id,message_id=call.message.message_id, text="Привіт! Я бот, який допоможе вам бути в курсі вашого розкладу та будь-яких змін у ньому. \nВиберіть своє Ім'я.")
        bot.edit_message_reply_markup(chat_id=call.message.chat.id,message_id=call.message.message_id, reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: "register_teacher_name" in call.data)
    def handle_teachers_callback(call):
        teacher = call.data.split("_")[-1]
        add_or_update_user(str(call.message.chat.id), "teacher", teacher, call.message)
        print(f"register - {str(call.message.chat.id)} - teacher - {teacher}")
        with open("sticker_ok.webp","rb") as sticker_file:
            sticker = sticker_file.read()
        bot.delete_message(call.message.chat.id,call.message.id)
        bot.delete_message(call.message.chat.id,call.message.id-1)
        bot.send_sticker(call.message.chat.id,sticker)
        bot.send_message(call.message.chat.id, f"Вітаю! Ви зареєструвались під  ім'ям {teacher} Відтепер ви кожен день будете отримувати розклад та заміни. Якщо у вас виникне якась помилка чи побажання, можете відправити нам відгук. \nДля того, щоб зареєструватись спочатку, натисніть /start, або кнопку Реєстрація.", reply_markup=markup_menu)


    # ---------------------------------------------всі користувачі------------------------------------
    @bot.message_handler(commands=['all_users'])
    def Users(message):
        if str(message.chat.id)==config.Admin:
            mess = bot.send_message(message.chat.id, "Enter user id > ")
            bot.register_next_step_handler(mess, search_user)
    def search_user(message):
        bot.send_message(message.chat.id, parse_all_users(message.text),parse_mode="HTML")
    # ----------------------------------------------------новини---------------------------------------
    @bot.message_handler(commands=['новини'])
    def Users(message):
        if str(message.chat.id)==config.Admin:
            keyboards = types.InlineKeyboardMarkup(row_width=1)
            buttons = types.InlineKeyboardButton('користувачу', callback_data='news_user')
            buttons1 = types.InlineKeyboardButton("Всім", callback_data='news_all')
            keyboards.add(buttons)
            keyboards.add(buttons1)
            bot.send_message(chat_id=Admin,text="Виберіть",reply_markup=keyboards)

    @bot.callback_query_handler(func=lambda call:   call.data.split("_")[0] in ["news"])
    def handle_teachers_callback(call):
        if call.data.split("_")[1] == "all":
            mess = bot.send_message(call.message.chat.id, "Надішліть повідомлення:")
            bot.register_next_step_handler(mess, news,call)
        else:
            mess = bot.send_message(call.message.chat.id, "Надішліть id:")
            bot.register_next_step_handler(mess, id_news,call)

    def id_news(message,call):
        mess = bot.send_message(call.message.chat.id, "Надішліть повідомлення:")
        bot.register_next_step_handler(mess, news_user,message.text)

    def news_user(message,user):
        try:
            if message.content_type == "sticker":
                bot.send_sticker(user,message.sticker.file_id)
            elif message.content_type == "photo":
                bot.send_photo(user,message.photo[-1].file_id)
                if message.caption :
                    bot.send_message(user,message.caption)
            elif message.content_type == "text":
                bot.send_message(user,message.text)
            bot.send_message(Admin,"good")
        except:
            print(f"{user}  ban")
            bot.send_message(Admin,"ban")

    def news(message,call):
        if call.data.split("_")[1] == "all":
            Users = get_chat_ids()
            for user in Users:
                try:
                    if message.content_type == "sticker":
                        bot.send_sticker(user,message.sticker.file_id)
                    elif message.content_type == "photo":
                        bot.send_photo(user,message.photo[-1].file_id)
                        if message.caption:
                            bot.send_message(user,message.caption)
                    elif message.content_type == "text":
                        if str(user[:-1]) == Admin:
                            bot.send_message(user,message.text, reply_markup=markup_menu_admin)
                        else:
                            markup = types.ReplyKeyboardRemove(selective=False)
                            bot.send_message(user,message.text, reply_markup=markup)
                    elif message.content_type == "document":
                        bot.send_document(user, message.document.file_id)
                except Exception as e:
                    print(f"{user}  ban - {e}")
            bot.send_message(Admin,"good")


    @bot.message_handler(content_types=['text', 'photo', 'sticker'], func=lambda message: str(message.chat.id) == response_chat and message.reply_to_message is not None)
    def on_reply(message):
        try:
            id = message.reply_to_message.text.split()[0]
            if message.content_type == 'text':
                bot.send_message(id,message.text)
            elif message.content_type == 'photo':
                bot.send_photo(id,message.photo[-1].file_id)
            elif message.content_type == 'sticker':
                bot.send_sticker(id,message.sticker.file_id)
        except:
            bot.send_message(response_chat,"Помилка")


    # ------------------------------------------відправка файлів адміну----------------------------
    @bot.message_handler(commands=["file"])
    def info(message):
        if str(message.chat.id) == Admin:
            try:
                keyboard = types.InlineKeyboardMarkup()
                with open("database.db","rb") as file:
                    bot.send_document(message.chat.id,file)
                with open("user_db.db","rb") as file:
                    bot.send_document(message.chat.id,file)

                folder_path = "LOG/"
                files = os.listdir(folder_path)
                files = [(os.path.join(folder_path, file), os.path.getmtime(os.path.join(folder_path, file))) for file in files]
                files.sort(key=lambda x: x[1], reverse=True)
                recent_files = files[:5]
                for filename in recent_files:
                    filename = filename[0].split("/")[1]
                    button = types.InlineKeyboardButton(text=filename, callback_data=filename)
                    keyboard.add(button)
                    # file_path = os.path.join("LOG", filename)
                    # if os.path.isfile(file_path):
                    #     with open(file_path, 'rb') as file:
                    #         bot.send_document(Admin, file)
                bot.send_message(chat_id=Admin, text="_",reply_markup=keyboard)
            except Exception as e:
                bot.send_message(message.chat.id,e)
    @bot.callback_query_handler(func=lambda call: ".txt" in call.data)
    def handle_teachers_callback(call):
        file_path = os.path.join("LOG", call.data)
        if os.path.isfile(file_path):
            with open(file_path, 'rb') as file:
                bot.send_document(Admin, file)
    # -------------------------------------заміни------------------------------------------------
    @bot.message_handler(func=lambda message: message.text =="Заміни" or message.text =="/Заміни")
    def info(message):
        log(message)
        try:
            # bot.send_message(chat_id=message.chat.id, text="Тимчасово не працюють")
            user = message.chat.id
            if os.path.exists('zaminu/'+print_data()+'.png'):
                with open('zaminu/'+print_data()+'.png',"rb")as photo:
                    bot.send_photo(user,photo=photo)
            elif os.path.exists('zaminu/'+yesterday_date()+'.png'):
                with open('zaminu/'+yesterday_date()+'.png',"rb")as photo:
                    bot.send_photo(user,photo=photo)
            else:
                parse_z()
                with open('zaminu/'+print_data()+'.png',"rb")as photo:
                    bot.send_photo(user,photo=photo)
        except Exception as e:
            print(f"440 : {e}")
    # ---------------------------------------розклад------------------------------------------------
    @bot.message_handler(func=lambda message: message.text =="Розклад" or message.text =="/Розклад")
    def info(message):
        log(message)

        keyboard = types.InlineKeyboardMarkup(row_width=6)
        button_today = types.InlineKeyboardButton(text="Сьогодні", callback_data="schedule_today")
        button_tomorrow = types.InlineKeyboardButton(text="Завтра", callback_data="schedule_tomorrow")
        button_week = types.InlineKeyboardButton(text="Весь тиждень", callback_data="schedule_week")
        button_week_1 = types.InlineKeyboardButton(text="Пн", callback_data="schedule_day_1")
        button_week_2 = types.InlineKeyboardButton(text="Вт", callback_data="schedule_day_2")
        button_week_3 = types.InlineKeyboardButton(text="Ср", callback_data="schedule_day_3")
        button_week_4 = types.InlineKeyboardButton(text="Чт", callback_data="schedule_day_4")
        button_week_5 = types.InlineKeyboardButton(text="Пт", callback_data="schedule_day_5")
        button_week_6 = types.InlineKeyboardButton(text="Сб", callback_data="schedule_day_6")

        keyboard.add(button_today)
        keyboard.add(button_tomorrow)
        keyboard.add(button_week)
        keyboard.add(button_week_1,button_week_2,button_week_3,button_week_4,button_week_5,button_week_6)
        bot.send_message(chat_id=message.chat.id, text="Тимчасово не працюють")

    @bot.callback_query_handler(func=lambda call: "schedule" in call.data)
    def handle_teachers_callback(call):
        user = str(call.message.chat.id)
        teacher = False
        # get_teacher(user)
        group = get_group_id(user)
        if group:
            if "today" in call.data:
                if print_today() == 7 :
                    with open("sticker_ok.webp","rb") as sticker_file:
                        sticker = sticker_file.read()
                    bot.send_sticker(user,sticker)
                    bot.send_message(user,"Сьогодні вихідний, відпочивай")
                elif print_today() == 6:
                    with open("subota.txt", "r") as subota:
                        bot.send_message(user,parse_r(group,int(subota.readline()),True,teacher=teacher))
                else:
                    roz = parse_r(group,data.print_today(),teacher=teacher)
                    # print(roz)
                    bot.send_message(user,roz)

            elif "tomorrow" in call.data:
                if print_today() == 6 :
                    with open("sticker_ok.webp","rb") as sticker_file:
                        sticker = sticker_file.read()
                    bot.send_sticker(user,sticker)
                    bot.send_message(user,"Завтра вихідний, відпочивай")
                elif print_today() == 7:
                    bot.send_message(user,parse_r(group,1,teacher=teacher))
                elif print_today() == 5:
                    with open("subota.txt", "r") as subota:
                        bot.send_message(user,parse_r(group,int(subota.readline()),True,teacher=teacher))
                else:
                    bot.send_message(user,parse_r(group,data.print_today()+1,teacher=teacher))
            elif "week" in call.data:
                text = ""
                week = ["Понеділок","Вівторок","Середа","Четвер","П'ятниця","Субота"]
                for i in range(1,7):
                    if i <6:
                        text = parse_r(group,i,teacher=teacher)
                    else:
                        with open("subota.txt", "r") as subota:
                            text = parse_r(group,int(subota.readline()),True,teacher=teacher)
                    text = f"{week[i-1]}\n{text}"
                    bot.send_message(user,text=text)
            elif "day" in call.data:
                week = ["Понеділок","Вівторок","Середа","Четвер","П'ятниця","Субота"]
                day = int(call.data.split("_")[-1])
                if day <6:
                    text = parse_r(group,day,teacher=teacher)
                else:
                    with open("subota.txt", "r") as subota:
                        text = parse_r(group,int(subota.readline()),True,teacher=teacher)
                text = f"{week[day-1]}\n{text}"
                bot.send_message(user,text=text)
        else:
            bot.send_message(user,"Будь ласка, зареєструйтесь❤️.\n/start")



    # ------------------------Викладачі----------та їх оцінка-----------------------------------
    @bot.message_handler(func=lambda message: message.text =='Викладачі' or message.text =='/Викладачі')
    def handle_departments(message):
        log(message)
        # створюємо клавіатуру з кнопками відділів
        keyboard = types.InlineKeyboardMarkup()
        for department in teachers_by_department.keys():
            button = types.InlineKeyboardButton(text=department, callback_data=department)
            keyboard.add(button)
        # відправляємо повідомлення зі списком відділів та клавіатурою
        bot.send_message(chat_id=message.chat.id, text="Виберіть відділ", reply_markup=keyboard)

    # створюємо обробник натискання на callback-кнопки відділів
    @bot.callback_query_handler(func=lambda call: call.data in teachers_by_department.keys())
    def handle_departments_callback(call):
        department = call.data
        # створюємо клавіатуру з кнопками викладачів вибраного відділу
        keyboard = types.InlineKeyboardMarkup()
        for teacher in teachers_by_department[department]:
            button = types.InlineKeyboardButton(text=teacher, callback_data=teacher)
            keyboard.add(button)
        # відправляємо повідомлення зі списком викладачів та клавіатурою
        bot.delete_message(call.message.chat.id, call.message.id)
        bot.send_message(chat_id=call.message.chat.id, text="Виберіть викладача", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data in [teacher for teachers in teachers_by_department.values() for teacher in teachers])
    def handle_teachers_callback(call):
        try:
            teacher = call.data
            print(teacher)
            # знаходимо відділ, до якого належить викладач
            department = [department for department, teachers in teachers_by_department.items() if teacher in teachers][0]
            # формуємо текст повідомлення
            text = f"Викладач: {teacher}\n{department.split()[0]}: {department.split()[1]}\n"
            # відправляємо повідомлення з інформацією про викладача
            conn = sqlite3.connect('teachers.db')
            # Вибірка даних з таблиці
            cursor = conn.cursor()
            cursor.execute('SELECT photo FROM teachers WHERE initials = ?', (teacher,))
            photo_data = cursor.fetchone()[0]
            bot.send_photo(chat_id=call.message.chat.id,photo=photo_data)
            cursor.execute('SELECT description FROM teachers WHERE initials = ?', (teacher,))
            description = cursor.fetchone()[0]

            for i in description.split("\n"):
                if "@" in i:
                    i = i.split()[0]+" ["+i.split()[1]+"](mailto{"+i.split()[1]+"})"
                text+=i+"\n"
            text += "Щоб оцінити викладача, виберіть оцінку нижче."
            teacher = call.data.split()[0]+" "+call.data.split()[1][0]
            markup = types.InlineKeyboardMarkup(row_width=5)
            item1 = types.InlineKeyboardButton("1", callback_data=teacher+'_1')
            item2 = types.InlineKeyboardButton("2", callback_data=teacher+'_2')
            item3 = types.InlineKeyboardButton("3", callback_data=teacher+'_3')
            item4 = types.InlineKeyboardButton("4", callback_data=teacher+'_4')
            item5 = types.InlineKeyboardButton("5", callback_data=teacher+'_5')
            markup.add(item1, item2, item3, item4, item5)
            bot.delete_message(call.message.chat.id, call.message.id)
            if os.path.exists(f"teacher_rang/{teacher}.txt"):
                with open(f"teacher_rang/{teacher}.txt","r",encoding="UTF-8") as file:
                    suma = 0
                    kil = 0
                    for i in file:
                        suma+=int(i.split("/")[1])
                        kil+=1
                bot.send_message(chat_id=call.message.chat.id, text=f"Рейтинг викладача : {suma/kil}.\nКількість голосів : {kil}")
            bot.send_message(chat_id=call.message.chat.id, text=text, parse_mode='Markdown', reply_markup=markup)
        except Exception as e:
            print(f"error_440 {e}")

    @bot.callback_query_handler(func=lambda call: call.data.split("_")[1] in ["1","2","3","4","5"])
    def handle_teachers_callback(call):
        print(f"{call.message.chat.id}  {call.data}")
        teacher = call.data.split("_")[0]
        bal = call.data.split("_")[1]
        bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id)
        text = ''
        user = False
        if not os.path.exists(f"teacher_rang/{teacher}.txt"):
            open(f"teacher_rang/{teacher}.txt","w",encoding="UTF-8")
        with open(f"teacher_rang/{teacher}.txt","r",encoding="UTF-8") as file:
            for index, line in enumerate(file):
                if len(line)> 2:
                    if line.split("/")[0] == str(call.message.chat.id):
                        text+=str(call.message.chat.id)+"/"+bal+"\n"
                        user = True
                    else:
                        text+=line
            if not user:
                text+=str(call.message.chat.id)+"/"+bal+"\n"
            with open(f"teacher_rang/{teacher}.txt","w",encoding="UTF-8") as f:
                f.write(text)
        with open(f"teacher_rang/{teacher}.txt","r",encoding="UTF-8") as file:
            suma = 0
            kil = 0
            for i in file:
                suma+=int(i.split("/")[1])
                kil+=1
            bot.send_message(call.message.chat.id,f"Вітаю, ви оцінили викладача. \nТепер його рейтинг складає ({round(suma/kil,2)}).\nВи також можете подивитись загальний рейтинг всіх викладачів, за допомогою цієї команди /rating")
    # --------------------------------------рейтинг викладачів--------------------------
    @bot.message_handler(commands=['rating'])
    def Users(message):
        log(message)
        rating = []
        for file_name in os.listdir("teacher_rang"):
            with open("teacher_rang/"+file_name,"r",encoding="UTF-8") as file:
                suma = 0
                kil = 0
                for i in file:
                    suma+=int(i.split("/")[1])
                    kil+=1
                rating.append(f"{file_name[:-4]}/{suma/kil}")
        text = ''
        place = 1
        while len(rating)>0:
            max ="0/0"
            for i in rating:
                if float(i.split("/")[1]) > float(max.split("/")[1]):
                    max = i
            rating.remove(max)
            text += str(place)+") "+str(round(float(max.split("/")[1]),2 ))+" - "+max.split("/")[0]+".\n"
            place+=1
        bot.send_message(message.chat.id,text)
    # --------------------------------------користувачі--------та рандом--------------------------------------------
    @bot.message_handler(commands=['користувачі'])
    def Users(message):
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        # Виконуємо запит на підрахунок кількості елементів в таблиці
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        # Закриваємо з'єднання
        conn.close()
        bot.send_message(message.chat.id,f"{count} - користувачів")



    # @bot.callback_query_handler(func=lambda call:   call.data.split("/")[0] in ["user"])
    # def handle_teachers_callback(call):
    #     send = ''
    #     with open("Users.txt", "r", encoding="UTF-8") as file:
    #         for user in file.readlines():
    #             text = ""
    #             with open(f"Users/{user[:-1]}/{user[:-1]}_group.txt") as group:
    #                 gr = group.readline()
    #                 if gr == call.data.split("/")[1]:
    #                     if not '-' in user:
    #                         try:
    #                             chat_member = bot.get_chat_member(chat_id=user, user_id=user)
    #                             text += parse_group(user[:-1]) + " - "
    #                             text += user[:-1] + " - "
    #                             text += str(chat_member.user.first_name) + " - "
    #                             text += str(chat_member.user.last_name) + " - @"
    #                             text += str(chat_member.user.username) + "\n"
    #                         except Exception as e:
    #                             print(e)
    #                             text += user[:-1] + " - ban\n"
    #                         send += text
    #     bot.send_message(Admin,str(send))

# -----------------------------------рандом---------------------------------------
    @bot.message_handler(commands=['rand'])
    def Users(message):
        log(message)
        bot.send_dice(message.chat.id)
    # ------------------------------зміна чисельника\знаменика та дня в суботу

    @bot.message_handler(commands=['субота'])
    def Users(message):
        if str(message.chat.id)==config.Admin:
            zmina_ch_z()
            data.subota()
    #-------------------------Погода------------------------------------#

    @bot.message_handler(func=lambda message: message.text =='Погода' or message.text =='/Погода')
    def Users(message):
        log(message)
        markup = types.InlineKeyboardMarkup(row_width=1)
        item1 = types.InlineKeyboardButton("Сьогодні", callback_data='0_weather')
        item2 = types.InlineKeyboardButton("Завтра", callback_data='1_weather')
        item3 = types.InlineKeyboardButton("Післязавтра", callback_data='2_weather')
        markup.add(item1, item2, item3)
        bot.send_message(chat_id=message.chat.id, text="Оберіть день", reply_markup=markup)

    @bot.callback_query_handler(func=lambda call:   call.data.split("_")[1] in ["weather"])
    def handle_teachers_callback(call):
        bot.send_message(chat_id=call.message.chat.id, text=parse_weather(int(call.data.split("_")[0])).split("~")[0] )


        # bot.send_photo(chat_id=call.message.chat.id, photo=photo_stream)
    #------------------------------Розсилка замін та розкаладу---------обновлення замін-------------------------------
    @bot.message_handler(commands=['update'])
    def Users(message):
        if str(message.chat.id)==config.Admin:
            if parse_z():
                bot.send_message(Admin,"good")

    @bot.message_handler(commands=['розсилка'])
    def Users(message):
        if str(message.chat.id)==config.Admin:
            if parse_z():
                users = get_chat_ids()

                lens = len(users)
                mess = bot.send_message(Admin,"start")
                for user in users:
                    teacher = get_teacher(user)
                    group = get_group_id(user)
                    print(lens)
                    bot.edit_message_text(text = str(lens),chat_id = Admin,message_id= mess.message_id)
                    with open('zaminu/'+print_data()+'.png',"rb")as photo:
                        print(user," ")
                        try:
                            bot.send_photo(user,photo=photo)
                        except:
                            print(user,"помилка")
  
                    # try:
                    #     if print_today() == 6:
                    #         with open("sticker_ok.webp","rb") as sticker_file:
                    #             sticker = sticker_file.read()
                    #         bot.send_sticker(user,sticker)
                    #         bot.send_message(user,"Завтра вихідний, відпочивай. Тримай заміни на понеділок.")
                    #         with open('zaminu/'+print_data()+'.png',"rb")as photo:
                    #             print(user," ")
                    #             bot.send_photo(user,photo=photo)
                    #     elif print_today() == 5:
                    #         with open('zaminu/'+print_data()+'.png',"rb")as photo:
                    #             print(user," ")
                    #             bot.send_photo(user,photo=photo)
                    #         with open("subota.txt","r") as subota:
                    #             bot.send_message(user,parse_r(group,int(subota.readline()),True,teacher=teacher))
                    #     elif print_today() == 7:
                    #         with open('zaminu/'+print_data()+'.png',"rb")as photo:
                    #             print(user," ")
                    #             bot.send_photo(user,photo=photo)
                    #         bot.send_message(user,parse_r(group,1,teacher=teacher))
                    #     else:
                    #         with open('zaminu/'+print_data()+'.png',"rb")as photo:
                    #             print(user," ")
                    #             bot.send_photo(user,photo=photo)
                    #         bot.send_message(user,parse_r(group,data.print_today()+1,teacher=teacher))
                    # except Exception as e:
                    #     print(f"{user} - помилка \n{e}")
                        # bot.send_message(Admin,f"{user} ban")
                    lens -= 1
                bot.edit_message_text("good",Admin,mess.message_id)
    # -------------------------------Game------------------------------------------
    # @bot.message_handler(commands=['update'])

    @bot.message_handler(func=lambda message: message.text =='Game')
    def Game(message):
        if message.text =='Game':
            log(message)
        if user_health(str(message.chat.id))>0:
            id_question, question, answers, correct_answer = random_question(str(message.chat.id))
            if question and answers and correct_answer:
                markup_question = types.ReplyKeyboardMarkup(resize_keyboard=True)
                for i in answers:
                    markup_question.add(types.KeyboardButton(i))
                markup_question.add(types.KeyboardButton("Завершити❌"),types.KeyboardButton("Інше питання➡️"))
                bot.send_message(chat_id=message.chat.id,text=question, reply_markup=markup_question)
                bot.register_next_step_handler(message, process_question, correct_answer, id_question)
        else:
            if add_health(message.chat.id):
                Game(message)
            else:
                if str(message.chat.id) == Admin:
                    bot.send_message(chat_id=message.chat.id,text=f"У вас залишилось 0 спроб. Вони поповняться через {return_minets(str(message.chat.id))} хвилин. Щоб переглянути рейтинг гравців натисніть /TOP",reply_markup=markup_menu_admin)
                else:
                    bot.send_message(chat_id=message.chat.id,text=f"У вас залишилось 0 спроб. Вони поповняться через {return_minets(str(message.chat.id))} хвилин. Щоб переглянути рейтинг гравців натисніть /TOP",reply_markup=markup_menu)
    def process_question(message, correct_answer, id_question):
        log(message)
        if message.text == "Завершити❌":
            if str(message.chat.id) == Admin:
                bot.send_message(chat_id=message.chat.id,text="Щоб переглянути рейтинг гравців натисніть /TOP",reply_markup=markup_menu_admin)
            else:
                bot.send_message(chat_id=message.chat.id,text="Щоб переглянути рейтинг гравців натисніть /TOP",reply_markup=markup_menu)
        elif message.text == "Інше питання➡️":
            Game(message)
        elif message.text == correct_answer:
            users_db(str(message.chat.id),True,id_question)
            if str(message.chat.id) == Admin:
                bot.send_message(chat_id=message.chat.id,text="Вірно")
            else:
                bot.send_message(chat_id=message.chat.id,text="Вірно")
            Game(message)
        else:
            users_db(str(message.chat.id),False,id_question)

            if str(message.chat.id) == Admin:
                bot.send_message(chat_id=message.chat.id,text=f"Не вірно. У вас залишилось {user_health(str(message.chat.id))} спроб.")
            else:
                bot.send_message(chat_id=message.chat.id,text=f"Не вірно. У вас залишилось {user_health(str(message.chat.id))} спроб.")
            Game(message)
    @bot.message_handler(commands=['stats'])
    def stats(message):
        log(message)
        bot.send_message(message.chat.id, f"Вітаю! Ви пройшли {emount_answer(str(message.chat.id))}/4000 питань.")
    @bot.message_handler(commands=['TOP'])
    def top_users(message):
        bot.send_message(message.chat.id, users_rating(message.chat.id), parse_mode="HTML")
    # --------------------------------Відгуки----------------------------------------
    @bot.message_handler(func=lambda message: message.text =='Відгук' or message.text =='/Відгук' )
    def Users(message):
        log(message)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton("Відмінити"))
        bot.send_message(message.chat.id, "Надішліть свій відгук:",reply_markup=markup)
        bot.register_next_step_handler(message, process_feedback)
    def process_feedback(message):
        if str(message.chat.id) == config.Admin:
            markup = markup_menu_admin
        else:
            markup = markup_menu
        if message.text != "Відмінити":
            feedback = f"{message.chat.id} - <a href='tg://user?id={message.chat.id}'>{message.from_user.first_name}</a> \n{message.content_type}"
            bot.send_message(chat_id=response_chat,text=feedback, parse_mode="HTML")
            # Повідомлення про успішне збереження відгуку
            user = response_chat
            if message.content_type == "sticker":
                bot.send_sticker(user,message.sticker.file_id)
            elif message.content_type == "photo":
                bot.send_photo(user,message.photo[-1].file_id)
                if message.caption:
                    bot.send_message(user,message.caption)
            elif message.content_type == "text":
                bot.send_message(user,message.text)
            bot.send_message(message.chat.id, "Дякуємо за ваш відгук!",reply_markup=markup)
        else:
            bot.send_message(message.chat.id,"Відгук скасовано",reply_markup=markup)

    # -----------------------------GPT--------------------------------------------------
    # @bot.message_handler(func=lambda message: message.text =='GPT' )
    # def Users(message):
    #     log(message)
    #     markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    #     markup.add(types.KeyboardButton("Відмінити"))
    #     bot.send_message(message.chat.id, "Надішліть свій запит:",reply_markup=markup)
    #     bot.register_next_step_handler(message, process)
    # def process(message):
    #     log(message)
    #     if str(message.chat.id) == config.Admin:
    #         markup = markup_menu_admin
    #     else:
    #         markup = markup_menu


    #     if message.text != "Відмінити":
    #         mess = bot.send_message(message.chat.id, "<i>Запит обробляється</i>",parse_mode="HTML")
    #         bot.send_message(message.chat.id, request(message.text))
    #         bot.delete_message(message.chat.id,mess.id)
    #         bot.register_next_step_handler(message, process)
    #     else:
    #         bot.send_message(message.chat.id,"Запит скасовано",reply_markup=markup)
    @bot.message_handler(func=lambda message: message.text =='Відмінити' or message.text == "Завершити❌")
    def User(message):
        if str(message.chat.id) == config.Admin:
            markup = markup_menu_admin
        else:
            markup = markup_menu
        bot.send_message(chat_id=message.chat.id,text="скасовано",reply_markup=markup)
    bot.polling(none_stop=True)
except Exception as e:
    traceback.print_exc()