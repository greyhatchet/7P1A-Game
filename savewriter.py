# writeSave takes a dictionary where the keys are the relevant data (e.g. game level) with their respective values:
# Added boolean returns to facilitate unit testing
save_files = ['savefile0.txt', 'savefile1.txt', 'savefile2.txt', 'savefile3.txt', 'savefile4.txt',
              'savefile5.txt', 'savefile6.txt', 'savefile7.txt', 'savefile8.txt', 'savefile9.txt']

def writeSave(save_dict, save_num):
    try:
        with open(save_files[save_num], 'w+') as f:

            if len(save_dict) == 0:
                raise(TypeError)

            for key in save_dict:
                new_str = key + ': ' + str(save_dict[key])
                f.write(new_str + '\n')

        return True

    except(IndexError):
        print('Save file not found!')
        return False

    except(TypeError):
        print('Invalid/incorrect number of inputs')
        return False


# Test lines:
# new_save = {'game_level': 91, 'total_score': 9, 'enemies_killed': 80, 'lives_left': 100}
# writeSave(new_save, 1)
