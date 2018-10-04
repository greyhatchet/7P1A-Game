# readScores reads the list of high scores from the text file and saves it as a list of tuples of format ('name', score)
def readScores():
    score_list = []
    with open(r"scoresfile.txt", 'r') as f:

        for line in f:
            (key, val) = line.split(':')
            try:
                (key, val) = (str(key), int(val))
            except:
                (key, val) = ('', 0)
            score_list.append((key, val))

    return score_list


# Test lines:
#print(readScores())