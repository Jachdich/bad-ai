import random, json
def clean(text):
    chars = "\n.':;,!?’‘-”“"
    for char in chars:
        text = text.replace(char, "")
    return text


#text = clean(open("trainlong.txt", "r").read().lower())
#text = open("/media/pi/JamsFiles/Programs/asd/total.py", "r").read()

def shift(last_words, word):
    last_words = last_words[1:]
    last_words.append(word)
    return last_words

def getFromDict(dataDict, mapList):    
    for k in mapList:
        dataDict = dataDict.get(k)
        if dataDict == None: return None
    return dataDict

def setInDict(dataDict, mapList, value): 
    for k in mapList[:-1]: dataDict = dataDict[k]
    dataDict[mapList[-1]] = value

def train(text, histsize):
    probs = {}
    last_words = [i for i in text[:histsize]]
    i = 0
    for word in text:
        if getFromDict(probs, last_words + [word,]) != None:
            setInDict(probs, last_words + [word,], getFromDict(probs, last_words + [word,]) + 1)
        else:
            y = []
            for x in last_words:
                y.append(x)
                if getFromDict(probs, y) == None:
                    setInDict(probs, y, {})

            setInDict(probs, y + [word,], 0)
        last_words = shift(last_words, word)
    return probs

def predict(starting_letters, num_chars, trained_model):
    out = ""
    last_words = list(starting_letters)
    probs = trained_model
    for i in range(num_chars):
        d = getFromDict(probs, last_words)
        keys = list(d.keys())
        values = list(d.values())
        random_key = random.choices(keys, weights=values)
        last_words = shift(last_words, random_key[0])
        out += random_key[0]
    return out
