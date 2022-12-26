import json
from logging import exception
from colorama import Fore
#from playsound import playsound - через жопу всё работает. Можете раскоментировать и попробовать реализовать сами в notify()

config_is_loaded = False
config = {}

def notify():
    #playsound("sound.mp3")
    pass
    
def load_config():
    _config = {}
    config_exists = True
    with open("config.json", "a+") as file:
        pass

    with open("config.json", "r") as file:
        if(len(file.read()) < 3):
            print(f"{Fore.RED}Конфиг не существует")
            config_exists=False

    if not config_exists:
        with open("config.json", "w", encoding="UTF-8") as file:
            with open("config.json.example", "r", encoding="UTF-8") as config:
                print(f"{Fore.YELLOW}Копируем стандартный конфиг...")
                file.write(config.read())
                print(f"{Fore.GREEN}Конфиг создан!")

    with open("config.json", "r", encoding="UTF-8") as file:
        data = json.load(file)
        for i in data:
            _config[i] = data[i]
    return _config

def update_config(new_config):
    global config
    config = new_config
    config_is_loaded = False
    with open("config.json", "w", encoding="UTF-8") as file:
        json.dump(config, file, ensure_ascii=False)


def log(text):
    print(text)
    with open("log.txt", "a", encoding="UTF-8") as file:
        file.write("\n" + text)

def checkSkip(text):
    global config_is_loaded, config
    if "пришли мне свое местоположение и увидишь кто находится рядом" in text or "хочешь больше взаимок?" in text:
        log(f"{Fore.YELLOW}Скипаем сообщение от дайвинчика... >>>" + text)
        return 2
    if "заканчивай с вопросом выше" in text:
        log(f"{Fore.GREEN}[!!!] Вас кто-то лайкнул.")
        return False
    if "смотреть анкеты" in text or "нет такого варианта ответа" in text:
        log(f"{Fore.RED}[!!!] Возможно вы не запустили поиск >>>" + text)
        log(f"{Fore.YELLOW}[!!!] Пробуем запустить поиск...")
        findtext = text.replace(" ", "")
        a = findtext.find("смотретьанкеты")
        if a == -1:
            log(f"{Fore.RED}[!!!] Не удалось запустить поиск. Пожалуйста, запустите режим поиска вручную.")
            raise Exception("Запустите режим поиска в дайвинчике")
        else:
            log(f"{Fore.GREEN}[!!!] Режим поиска запущен автоматически.")
            return int(findtext[a-2])
            
    if not config_is_loaded:
        config = load_config()
        config_is_loaded = True
    text = text.replace("нашел кое-кого для тебя, смотри:", "").replace("\n", " ").strip().lower()
    for i in config["WHITELIST"]:
        if i.lower() in text:
            print("\n")
            log(f"{Fore.GREEN}[!!!] Искомый ключ {Fore.RESET}>>> " + i + " <<< " + text)
            print("\n")
            notify()
            return False
    for i in config["BLACKLIST"]:
        if i.lower() in text:
            log(f"{Fore.RED}Запрещённый ключ {Fore.RESET}>>> " + i + " <<< " + text)
            return True
    #if "на самом деле" in text:
    #    log(f"{Fore.CYAN}Возраст? {Fore.RESET}>>>" + text)
    #    return config["SKIP_ALL"]
    if len(text) < config["MIN_SYMBOL"]:
        log(f"{Fore.YELLOW}Мало текста {Fore.RESET}>>> " + text.strip())
        return True
    log(f"{Fore.CYAN}Нейтральная анкета {Fore.RESET}>>> " + text)
    notify()
    return config["SKIP_ALL"]