score_list = []

def readScores():
    with open("scoresfile.txt") as f:
        for line in f:
            (key, val) = line.split(':')
            (key, val) = (str(key), int(val))
            score_list.append((key, val))

readScores()
print(score_list)