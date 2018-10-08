# writeScores takes a list of tuples of format ('name', score) and writes it to the score text file:
# Boolean returns added to facilitate unit testing
def writeScores(scores):

    try:
        with open(r"scoresfile.txt", 'w+') as f:

            if len(scores) == 0:
                raise(ValueError)

            if not isinstance(scores, list):
                raise(TypeError)

            for i in range(10):

                try:
                    new_name = scores[i][0]
                    new_score = scores[i][1]
                    new_str = new_name + ': ' + str(new_score)
                    f.write(new_str + '\n')

                except(IndexError):
                    new_str = ':'
                    f.write(new_str + '\n')

            return True

    except(FileNotFoundError):
        print(str(file_path) + ' not found!')
        return False

    except(ValueError):
        print('Input score list is empty')
        return False

    except(TypeError):
        print('Input score list is not a list of tuples')
        return False

    except(NameError):
        print('Invalid/undefined input')
        return False

'''
Need to sort the file by the scores to display the top 3 scores
'''

# Test lines:
# new_scores = [('a', 1), ('z', 2), ('c', 12), ('x', 4), ('e', 5), ('f', 6),
#              ('g', 7), ('h', 8), ('i', 9), ('j', 10), ('k', 11), ('l', 12)]

# writeScores(new_scores)
