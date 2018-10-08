# readScores reads the list of high scores from the text file and saves it as a list of tuples of format ('name', score)
def readScores(file_path):
    score_list = []
    try:
        with open(file_path, 'r') as f:

            for line in f:
                (key, val) = line.split(':')
                try:
                    (key, val) = (str(key), int(val))
                except:
                    (key, val) = ('', 0)
                score_list.append((key, val))

        return score_list

    except(FileNotFoundError):
        print(str(file_path) + ' not found, returning empty list')
        return score_list

    except(OSError):
        print(str(file_path) + ' is not a valid file path, return empty list')
        return score_list


# Test lines:
#print(readScores())