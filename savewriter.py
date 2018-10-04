# writeSave takes a dictionary where the keys are the relevant data (e.g. game level) with their respective values:
def writeSave(save_dict):
    with open(r"savefile.txt", 'w+') as f:

        for key in save_dict:
            new_str = key + ': ' + str(save_dict[key])
            f.write(new_str + '\n')


# Test lines:
new_save = {'game_level': 91, 'total_score': 9, 'enemies_killed': 80, 'lives_left': 100}
writeSave(new_save)
