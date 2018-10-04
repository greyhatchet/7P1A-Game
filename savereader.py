saveDict = {}

def readSave():
    with open("savefile.txt") as f:
        for line in f:
            (key, val) = line.split(':')
            newDict[str(key)] = float(val)

print(saveDict)