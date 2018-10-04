# writeScores takes a list of tuples of format ('name', score) and writes it to the score text file:
def writeScores(scores):
    with open(r"scoresfile.txt", 'w+') as f:

        for i in range(10):

            try:
                new_name = scores[i][0]
                new_score = scores[i][1]
                new_str = new_name + ': ' + str(new_score)
                f.write(new_str + '\n')

            except:
                new_str = ':'
                f.write(new_str + '\n')


# Test lines:
new_scores = [('ASD', 202), ('asdsa', 2312)]
writeScores(new_scores)