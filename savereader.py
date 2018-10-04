# readSave() reads the save text file into a new dictionary and returns it
def readSave():
    save_dict = {}
    with open(r"savefile.txt", 'r') as f:

        for line in f:
            (key, val) = line.split(':')
            save_dict[str(key)] = float(val)

    return save_dict


# Test lines:
#print(readSave())
