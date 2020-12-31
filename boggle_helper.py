'''Made by Jackson Bremen ||| Summer 2018
Sorry for the garbage code
Trie Datastructure copied from github linked below, one additional function added
https://www.wordplays.com/boggle has line crossing be legal
'''

import readline
from Trie import Trie

dictionary = Trie()
with open('allScrabbleWords.txt','r') as file:
    for i in file.read().split():
        dictionary.insert(i)

board = []
with open('boggleBoard.txt','r') as file:
    for line in file.readlines():
        board.append([])
        for char in line.split():
            board[-1].append(char.upper())

def print_board(board):
    for y in board:
        for x in y:
            if len(x) == 2:
                print(x, end=' ')
            else:
                print(x, end='  ')
        print()

def adjacent(val1,val2,lst):
    try:
        return (lst.index(val1) - lst.index(val2) in [-1,1])
    except ValueError:
        return False
    return False

def solve_board(board):
    def turtle(board, x, y, curr_path, letters=''):
        #crossing lets the path cross over itself diagonaly [if true]; min_num_lett is the min number of letters for a word
        crossing, min_num_lett = False, 3
        
        curr_path.append((x,y))
        letters += str(board[x][y])
        
        #checking to see if the current path has made a letter, and if it has been the right length
        if dictionary.contains(letters) and len(letters) >= min_num_lett:
            all_words.append(letters)
       
        #if there are no more possible words
        elif not dictionary.one_autocomplete(letters):
          return 0

        if (x+1,y) not in curr_path:
            turtle(board,x+1,y, list(curr_path), str(letters))

        if (x-1,y) not in curr_path:
            turtle(board,x-1,y, list(curr_path), str(letters))

        if (x,y-1) not in curr_path:
            turtle(board,x,y-1, list(curr_path), str(letters))

        if (x,y+1) not in curr_path:
            turtle(board,x,y+1, list(curr_path), str(letters))

        if not crossing:
            if (x-1,y+1) not in curr_path and not adjacent((x-1,y),(x,y+1), curr_path):
                turtle(board,x-1,y+1,list(curr_path), str(letters))

            if (x+1,y+1) not in curr_path and not adjacent((x+1,y), (x,y+1), curr_path):
                turtle(board,x+1,y+1,list(curr_path), str(letters))
            
            if (x-1,y-1) not in curr_path and not adjacent((x-1,y), (x,y-1), curr_path):
                turtle(board,x-1,y-1,list(curr_path), str(letters))
            
            if (x+1,y-1) not in curr_path and not adjacent((x+1,y), (x,y-1), curr_path):
                turtle(board,x+1,y-1,list(curr_path), str(letters))
        else:
            #diagonals, allows crossing over
            if (x+1,y+1) not in curr_path:
                turtle(board,x+1,y+1, list(curr_path), str(letters))

            if (x+1,y-1) not in curr_path:
                turtle(board,x+1,y-1, list(curr_path), str(letters))

            if (x-1,y-1) not in curr_path:
                turtle(board,x-1,y-1, list(curr_path), str(letters))

            if (x-1,y+1) not in curr_path:
                turtle(board,x-1,y+1, list(curr_path), str(letters))
   
    # all_words is global, as lists are global by default in python
    all_words = []
    # board exterior is a list of the points on the exterior of the board, such that the turtle won't go to them
    board_exterior = [(-1,-1)] + [(-1,i) for i in range(len(board)+1)] + [(len(board), i) for i in range(len(board)+1)] + [(i,-1) for i in range(len(board)+1)] + [(i,len(board)) for i in range(len(board)+1)]

    for x, y_l in enumerate(board):
        for y, x_l in enumerate(y_l):
            turtle(board,x,y, [i for i in board_exterior])          
    return all_words

def score_calc(words):
    val_table = {0:0,1:0,2:0,3:1,4:1,5:2,6:3,7:5,8:11}
    total = 0
    numChars = 0
    for item in words:
        if len(item) not in val_table:
            total += 11
        else:
            total += val_table[len(item)]
        numChars+= len(item)
    return total,numChars

print_board(board)
solution = solve_board(board)
print(','.join(solution), '\n', len(solution),'words, max score is:', str(score_calc(solution)),'characters' )
