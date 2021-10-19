import json
from colorama import Fore
config_is_loaded = False
config = {}
def load_config():
    _config = {}
    config_exists = True
    with open("config.json", "a+") as file:
        if(len(file.read()) < 3):
            config_exists=False

    if not config_exists:
        with open("config.json", "w", encoding="UTF-8") as file:
            with open("config.json.example", "r", encoding="UTF-8") as config:
                file.write(config.read())

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
    if not config_is_loaded:
        config = load_config()
        config_is_loaded = True
    text = text.replace("нашел кое-кого для тебя, смотри:", "").replace("\n", " ")
    if "на самом деле" in text:
        log(f"{Fore.CYAN}Возраст? {Fore.RESET}>>>" + text)
        return False
    if len(text) < config["MIN_SYMBOL"]:
        log(f"{Fore.YELLOW}Мало текста {Fore.RESET}>>> " + text)
        return True
    for i in config["BLACKLIST"]:
        if i in text:
            log(f"{Fore.RED}Запрещённый ключ {Fore.RESET}>>> " + i + " <<< " + text)
            return True
    for i in config["WHITELIST"]:
        if i in text:
            print("\n")
            log(f"{Fore.GREEN}[!!!] Искомый ключ {Fore.RESET}>>> " + i + " <<< " + text)
            print("\n")
            return False
    log(f"{Fore.CYAN}Нейтральная анкета {Fore.RESET}>>> " + text)
    return config["SKIP_ALL"]