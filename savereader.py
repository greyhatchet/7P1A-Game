# readSave() reads the desired save text file into a new dictionary and returns it
save_files = ['savefile1.txt', 'savefile2.txt', 'savefile3.txt']

def readSave(save_num):
    save_dict = {}
    try:
        with open(save_files[save_num], 'r') as f:

            for line in f:
                (key, val) = line.split(':')
                save_dict[str(key)] = float(val)

        return save_dict

    except(IndexError):
        print('Save file not found, returning empty dictionary')
        return save_dict

    except(OSError):
        print(str(file_path) + ' is not a valid file path, returning empty dictionary')
        return save_dict

    except(TypeError):
        print('Input is not a valid save file number, returning empty dictionary')
        return save_dict


# Test lines:
#print(readSave())
