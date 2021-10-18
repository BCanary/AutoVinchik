from config import *

def log(text):
    print(text)
    with open("log.txt", "a", encoding="UTF-8") as file:
        file.write("\n" + text)

def checkSkip(text):
    text = text.replace("нашел кое-кого для тебя, смотри:", "").replace("\n", " ")
    for i in WHITELIST:
        if i in text:
            print("\n")
            log("[!!!] Whitelist >>> " + i + " <<< " + text)
            print("\n")
            return False
    if len(text) < MIN_SYMBOL:
        log("Too small >>> " + text)
        return True
    for i in BLACKLIST:
        if i in text:
            log("Blacklist >>> " + i + " <<< " + text)
            return True
    print("\n")
    log("Nonelist >>> " + text)
    print("\n")
    return SKIP_ALL