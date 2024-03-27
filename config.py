from data import print_data,print_time

TOKEN='6141936678:AAEzFFrByAXncrw1Z1VdChXaRGHIQYOP4wc'
Admin='893937933'
Admin_chat='-720181603'
response_chat = "-969136900"
nubip = "https://rfc.nubip.edu.ua/to-a-student/changes-to-the-schedule"
api_key_pars_foto = '93dff8edeb1c499ca9c5fb9866c0060e'
api_key_pars_weather = 'c38727daba7c43f6a2e104114231804'

def log_error(text):
    data = {
            "error":"error",
            "date": str(print_time()),
            "text_":text
        }
    with open("LOG/"+print_data()+".txt","a",encoding="UTF-8") as f:
        f.write(str(data)+"\n")

def log(message,text = ''):
    if text == '':
        # Отримуємо необхідні дані з об'єкту message та створюємо словник
        data = {
            "text": str(message.text),
            "chat_id": message.chat.id,
            "date": str(print_time()),
            "username": str(message.from_user.username),
            "first_name": str(message.from_user.first_name),
            "last_name":str(message.from_user.last_name)
        }
        # Записуємо дані у файл JSON з табуляцією
        with open("LOG/"+print_data()+".txt","a",encoding="UTF-8") as f:
            f.write(str(data)+text+'\n')
    else:
        # Отримуємо необхідні дані з об'єкту message та створюємо словник
        data = {
            "text": str(message.text),
            "chat_id": message.chat.id,
            "date": str(print_time()),
            "username": str(message.from_user.username),
            "first_name": str(message.from_user.first_name),
            "last_name":str(message.from_user.last_name),
            "text_":text
        }
        # Записуємо дані у файл JSON з табуляцією
        with open("LOG/"+print_data()+".txt","a",encoding="UTF-8") as f:
            f.write(str(data)+text+'\n')
    print(str(message.chat.id)+"  "+str(message.from_user.username)+"  "+message.text+"    "+text)