# readScores reads the list of high scores from the text file and saves it as a list of tuples of format ('name', score)
def readScores(file_path):
    score_dict = {}
    try:
        with open(file_path, 'r') as f:

            for line in f:
                line = line.strip('\n')
                (key, val) = line.split(':')
                try:
                    score_dict[str(key)] = int(val)
                except(ValueError):
                    score_dict[" "] = 0

        return score_dict

    except(FileNotFoundError):
        print(str(file_path) + ' not found, returning empty dict')
        return score_dict

    except(OSError):
        print(str(file_path) + ' is not a valid file path, return empty dict')
        return score_dict


# Test lines:
#print(readScores('scoresfile.txt'))