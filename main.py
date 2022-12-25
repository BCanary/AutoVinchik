from json import encoder
from typing import Container
import vk_api
import time
import emoji 
from vk_api.utils import get_random_id
from skipper import checkSkip, load_config, config, update_config
from telethon import TelegramClient, events, sync
import os
import colorama
from colorama import Fore
import random
from collections import Counter

is_vk_connected = False
is_tg_connected = False
#logging.basicConfig(format='[%(levelname) 5s/%(asctime)s] %(name)s: %(message)s', level=logging.WARNING)

colorama.init(autoreset=True)
os.system("cls")
def logo():
    with open("banner.txt", "r", encoding="UTF-8") as file:
        for i in file.readlines():
            text = i.strip().split("|")
            print(Fore.RED + text[0], Fore.YELLOW + text[1])
    print("\n")

logo()

print(Fore.YELLOW + "Загрузка конфигурации")

config = load_config()
print(Fore.YELLOW + "Подключение ключа ВК")
try:
    vk = vk_api.VkApi(token=config["TOKEN_VK"])
    vk.method("messages.getHistory", {"count": 1, "peer_id": -91050183})["items"][0]["text"].lower() # TESTING
    print(Fore.GREEN + "Ключ ВК подключен")
    is_vk_connected = True
    
except:
    print(Fore.RED + "Ключ ВК не подключен")

print(Fore.YELLOW + "Подключение ключа Телеграм")
try:
    client = TelegramClient('AutoVinchik', config["API_ID"], config["API_HASH"])
    client.start()
    print(Fore.GREEN + "Ключ Телеграм подключен")
    is_tg_connected = True
except:
    print(Fore.RED + "Ключ Телеграм не подключен")
print(Fore.YELLOW + "Инициализация запуска")
time.sleep(0.3)

BOT = 'leomatchbot'
BOT_ID = 1234060895
mode = 0
quotes = []
with open("quotes.txt", "r", encoding="UTF-8") as file:
    quotes = [x.strip() for x in file.readlines()]

def telegram():
    time.sleep(0.5) # Не спрашивайте
    
    print(f"{Fore.CYAN}TG |{Fore.RESET} ", end="")
    message = client.get_messages(BOT,limit=1)[0].message.lower()
    
    if len(message.replace(" ", "")) < 2:
        message = client.get_messages(BOT)[0].message
        for i in client.iter_messages(BOT):
            if (len(i.message) > 0):
                message = i.message
                #print(message)
                break
        #input("ZXFC")
    skip = checkSkip(message)
    try:
        if str(type(skip)) == str(type(1)):
            client.send_message(BOT, str(skip))
            time.sleep(2)
            message = client.get_messages(BOT)[0].text.lower()
            skip = checkSkip(message)
    except:
        pass

    if (skip):
        client.send_message(BOT, emoji.emojize(":thumbs_down:"))
        time.sleep(config["DELAY_TG"])
    else:
        input(f"{Fore.CYAN}Для пропуска анкеты нажмите ENTER")
        client.send_message(BOT, emoji.emojize(":thumbs_down:"))

def vkontakte():
    print(f"{Fore.CYAN}VK |{Fore.RESET} ", end="")
    message = vk.method("messages.getHistory", {"count": 1, "peer_id": -91050183})["items"][0]["text"].lower()

    skip = checkSkip(message)
    try:
        if type(skip) == type(1):
            vk.method("messages.send", {"peer_id": -91050183, "message": str(skip), "random_id": get_random_id()})
            time.sleep(2)
            message = vk.method("messages.getHistory", {"count": 1, "peer_id": -91050183})["items"][0]["text"].lower()
            skip = checkSkip(message)
    except:
        pass

    if (skip):
        vk.method("messages.send", {"peer_id": -91050183, "message": "3", "random_id": get_random_id()})
        time.sleep(config["DELAY_VK"])
    else:
        input(f"{Fore.CYAN}Для пропуска анкеты нажмите ENTER")
        vk.method("messages.send", {"peer_id": -91050183, "message": "3", "random_id": get_random_id()})


leave_config = False
while True:
    os.system("cls")
    logo()
    print(f"{Fore.CYAN}[0].{Fore.RESET} Конфигурация")
    print(f"{Fore.CYAN}[1].{Fore.RESET} Поиск только по телеграм")
    print(f"{Fore.CYAN}[2].{Fore.RESET} Поиск только по вконтакте")
    print(f"{Fore.CYAN}[3].{Fore.RESET} Комбинированный поиск")
    print(f"{Fore.CYAN}[4].{Fore.RESET} Подвести статистику")
    do = input(f"{Fore.CYAN}>>>{Fore.RESET} ")

    if do == "0":
        while True:
            os.system("cls")
            logo()
            neutral = Fore.RED
            n_text = "Отключено"
            if config["SKIP_ALL"]:
                neutral = Fore.GREEN
                n_text = "Включено"
            print(f"{Fore.CYAN} Получить токен ВК (Нужен только доступ к сообщениям) - https://vkhost.github.io/")
            print(f"{Fore.CYAN} Получить токен Телеграм - https://tlgrm.ru/docs/api/obtaining_api_id")
            print(f"{Fore.CYAN} Вы можете задать эти значения вручную через файл config.json")
            print("\n")
            print(f"{Fore.YELLOW} [!] Винчик любит присылать всякую рекламу и предложения на которых бот может сломаться. При такой проблеме пропустите объявление и перезапустите программу если она вылетела.")
            print("\n")
            print(f"{Fore.CYAN}[1].{Fore.RESET} Токен ВК " + Fore.YELLOW + "(" + config["TOKEN_VK"][:4] + "***" + config["TOKEN_VK"][-4::] + ")")
            print(f"{Fore.CYAN}[2].{Fore.RESET} Токен Телеграм " + Fore.YELLOW + "(" + str(config["API_ID"])[:2] + "***:***" + config["API_HASH"][-4::] + ")")
            print(f"{Fore.CYAN}[3].{Fore.RESET} Настройка запрещённых ключей " + Fore.YELLOW + str(config["BLACKLIST"]))
            print(f"{Fore.CYAN}[4].{Fore.RESET} Настройка искомых ключей " + Fore.YELLOW + str(config["WHITELIST"]))
            print(f"{Fore.CYAN}[5].{Fore.RESET} Задержка для ВК " + Fore.YELLOW + "(" + str(config["DELAY_VK"]) + " сек)")
            print(f"{Fore.CYAN}[6].{Fore.RESET} Задержка для Телеграм " + Fore.YELLOW + "(" + str(config["DELAY_TG"]) + " сек)")
            print(f"{Fore.CYAN}[7].{Fore.RESET} Останавливаться только на искомых ключах " + neutral + "(" + n_text + ")")
            print(f"{Fore.CYAN}[8].{Fore.RESET} Минимальное количество символов для пропуска " + Fore.YELLOW + "(" + str(config["MIN_SYMBOL"]) + ")")
            print(f"{Fore.CYAN}[0].{Fore.RESET} Выход из конфигурации")
            do = input(f"{Fore.CYAN}>>>{Fore.RESET} ")
            if do == "0":
                leave_config = True
                break
            elif do == "1":
                token = input("Введите токен ВК: ")
                config["TOKEN_VK"] = token
            elif do == "2":
                api_id = input("Введите API_ID: ")
                api_hash = input("Введите API_HASH: ")
                config["API_ID"] = api_id
                config["API_HASH"] = api_hash
            elif do == "3" or do == "4":
                type = "BLACKLIST"
                if do == "4":
                    type = "WHITELIST"
                while True:
                    os.system("cls")
                    logo()
                    print(f"{Fore.CYAN}ID | Все значения:")
                    for index, i in enumerate(config[type]):
                        print(f"{Fore.CYAN}[{index}]{Fore.RESET}. {i}")
                    print("\n")
                    print(f"{Fore.CYAN}Можно указать сразу несколько значений через точку с запятой (;)")
                    print(f"{Fore.CYAN}[1].{Fore.RESET} Удалить значения")
                    print(f"{Fore.CYAN}[2].{Fore.RESET} Добавить значения")
                    print(f"{Fore.CYAN}[0].{Fore.RESET} Выход из редактора")
                    do = input(f"{Fore.CYAN}>>>{Fore.RESET} ")
                    if do == "0":
                        break
                    elif do == "1":
                        sid = input(f"{Fore.CYAN}Введите ID значений: {Fore.RESET}")
                        for i in sid.split(";"):
                            config[type][int(i)] = "//TODELETE//"
                        while "//TODELETE//" in config[type]:
                            config[type].remove("//TODELETE//")
                    elif do == "2":
                        new_value = input(f"{Fore.CYAN}Новые значение: {Fore.RESET}")
                        for i in new_value.split(";"):
                            config[type].append(i.lower())
                    update_config(config)
            elif do == "5":
                data = input("Новая задержка для ВК: ")
                config["DELAY_VK"] = float(data)
            elif do == "6":
                data = input("Новая задержка для Телеграм: ")
                config["DELAY_TG"] = float(data)
            elif do == "7":
                config["SKIP_ALL"] = not config["SKIP_ALL"]
            elif do == "8":
                data = input("Новое количество символов: ")
                config["MIN_SYMBOL"] = int(data)
            
            update_config(config)
    if leave_config:
        leave_config = False
        continue
    elif do == "1":
        mode = 0
    elif do == "2":
        mode = 1
    elif do == "3":
        mode = 2
    elif do == "4":
        print(f"{Fore.RED} Этот модуль может работать нестабильно. Используйте свою реализацию анализа сообщений если хотите достичь большей точности.")
        print(f"{Fore.YELLOW} Подводим статистику...")
        if is_vk_connected:
            print(f"{Fore.CYAN} Считаем ВК")
            a = vk.method("messages.getHistory", {"count": 1, "offset": 0, "peer_id": -91050183})
            count = a["count"]
            print(f"{Fore.GREEN} Всего {count} сообщений. Доступная глубина {int(count/200)} обращений к вк")
            depth = int(input(f"{Fore.CYAN} Глубина анализа (Число от 1 до {int(count/200)})>> "))
            
            with open("messages.txt", "w", encoding="UTF-8") as file:
                for j in range(0, depth):
                    print(f"{Fore.CYAN} Обращение номер: {j+1}")
                    a = vk.method("messages.getHistory", {"count": 200, "offset": j*200, "peer_id": -91050183})["items"]
                    
                    for i in a:
                        
                        if (i["from_id"] == -91050183) and (len(i["attachments"]) > 0) and not "Вот твоя анкета:" in i["text"] and not "Так выглядит твоя анкета:" in i["text"]:
                            file.write(i["text"].replace("\n", " ").replace("Кому-то понравилась твоя анкета:", "").replace("Нашел кое-кого для тебя, смотри:", "") + "\n")
        if is_tg_connected:  
            print(f"{Fore.CYAN} Считаем ТГ")
            #a = vk.method("messages.getHistory", {"count": 1, "offset": 0, "peer_id": -91050183})
            count = client.get_messages(BOT).total
            print(f"{Fore.GREEN} Всего {count} сообщений. Доступная глубина {int(count/200)} обращений к телеграм")
            depth = int(input(f"{Fore.CYAN} Глубина анализа (Число от 1 до {int(count/200)})>> "))
            #print(f"{Fore.RED} Подгрузка может занять некоторое время...")
            
            with open("messages.txt", "a", encoding="UTF-8") as file:
                for j in range(0, depth):
                    print(f"{Fore.CYAN} Обращение номер: {j+1}")
                    messages = client.get_messages(BOT, limit=200, add_offset=200*j)
                    for index, i in enumerate(messages):
                        if len(i.message) < 4:
                            continue
                        if i.out == True:
                            continue
                        if "Вот твоя анкета:" in i.message or "1." in i.message:
                            continue
                            
                        file.write(i.message.replace("\n", " ").replace("Кому-то понравилась твоя анкета:", "").replace("Нашел кое-кого для тебя, смотри:", "") + "\n")
                        
                        #if (index % 10 == 0):
                        #    print(f"{Fore.CYAN} Готово {index} сообщений")
                            
        with open("stat.txt", "w", encoding="UTF-8") as file:
            a = ""
            with open("messages.txt", "r", encoding="UTF-8") as file2:
                #for i in file2.readlines():
                 #   if "," in i:
                  #      if len(i) < 40:
                   #         empty+=1;
                a = [i.replace(",", " ").replace(".", " ").replace("\n", " ").replace(" ", "").lower() for i in file2.read().replace("Too small", "").replace("<<<", "").replace(">>>", "").split(" ")]
                #print(a)
            c = dict(sorted(Counter(a).items(), key=lambda x: x[1]))
            for i in c:
                file.write(str(i) +  " : " + str(c[i]) + "\n")
                
        input(f"{Fore.GREEN} Завершено: Результаты в файле stat.txt - Нажмите ENTER")
        continue

    os.system("cls")
    logo()
    print(f"{Fore.CYAN}{random.choice(quotes)}")
    time.sleep(1)
    print(f"{Fore.YELLOW}Не забудьте запустить режим поиска в сообщениях винчика! {Fore.RESET}\n")
    print(f"{Fore.YELLOW}Для выхода из поиска нажмите CTRL+C {Fore.RESET}\n")
    while True:
        try:
            if(mode == 0 or mode==2):
                telegram()
            if(mode == 1 or mode==2):
                vkontakte()
        except KeyboardInterrupt:
            print(f"{Fore.YELLOW}\nВыход в меню... {Fore.RESET}")
            time.sleep(0.3)
            break
