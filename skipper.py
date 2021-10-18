from config import *

def log(text):
    print(text)
    with open("log.txt", "a", encoding="UTF-8") as file:
        file.write("\n" + text)

def checkSkip(text):
    text = text.replace("нашел кое-кого для тебя, смотри:", "").replace("\n", "")
    if len(text) < MIN_SYMBOL:
        log("Too small >>> " + text)
        return True
    for i in BLACKLIST:
        if i in text:
            log("Blacklist >>> " + i + " <<< " + text)
            return True
    for i in WHITELIST:
        if i in text:
            log("[!!!] Whitelist >>> " + i + " <<< " + text)
            return False
    log("Nonelist >>> " + text)
    return SKIP_ALL