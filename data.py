import datetime
# from datetime import datetime, timedelta
import datetime
import pytz

def ret_min(date_string):
    date_format = "%d %b %Y %H:%M:%S"
    given_date = datetime.datetime.strptime(date_string, date_format)
    # Отримання поточної дати та часу
    current_date = datetime.datetime.now()

    # Додавання однієї години до заданої дати
    target_date = given_date + datetime.timedelta(hours=0.1)
    minutes_remaining = (target_date - current_date).seconds // 60
    return minutes_remaining

def one_hourse(date_string):
    date_format = "%d %b %Y %H:%M:%S"
    given_date = datetime.datetime.strptime(date_string, date_format)

    # Отримання поточної дати та часу
    current_date = datetime.datetime.now()

    # Додавання однієї години до заданої дати
    target_date = given_date + datetime.timedelta(hours=0.1)
    # Перевірка, чи пройшла вже година
    print(current_date,"-", target_date)
    return current_date >= target_date

def print_time():
    tz = pytz.timezone('Europe/Kiev')
    now = datetime.datetime.now(tz)
    return(now.strftime("%H:%M:%S"))

def print_data():
    tz = pytz.timezone('Europe/Kiev')
    now = datetime.datetime.now(tz)
    return now.strftime("%d %B %Y")

def print_data_time():
    timezone = pytz.timezone('Europe/Kiev')

    # Отримуємо поточну дату і час у часовому поясі Києва
    current_datetime = datetime.datetime.now()

    # Форматуємо дату і час у вказаний формат
    formatted_datetime = current_datetime.strftime('%d %b %Y %H:%M:%S')

    return formatted_datetime

def yesterday_date():
    tz = pytz.timezone('Europe/Kiev')
    today = datetime.datetime.now(tz)
    yesterday = today - datetime.timedelta(days=1)
    return yesterday.strftime("%d %B %Y")

def print_today():
    tz = pytz.timezone('Europe/Kiev')
    today = datetime.datetime.now(tz).date()
    day_of_week = today.weekday() + 1
    return day_of_week
def subota():
    with open("subota.txt","r", encoding='utf-8') as file:
        fil = file.readline()
        if '5' == fil:
            with open("subota.txt","w", encoding='utf-8') as f:
                f.write("1")
        else:
            with open("subota.txt","w", encoding='utf-8') as f:
                f.write(str(int(fil)+1))
