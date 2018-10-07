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

'''
Need to sort the file by the scores to display the top 3 scores
'''

# Test lines:
new_scores = [('a', 1), ('z', 2), ('c', 12), ('x', 4), ('e', 5), ('f', 6),
              ('g', 7), ('h', 8), ('i', 9), ('j', 10), ('k', 11), ('l', 12)]

writeScores(new_scores)
