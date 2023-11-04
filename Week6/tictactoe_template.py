'''
Human is X and play as max by placing 1 on the board
The program is O and plays as min by placing -1 on the board

What needs to be completed are:
1) Code for maxPlay
2) Code for minPlay
3) Code for program_turn
'''

'''
Team Members:
1) Tanat Arora, ID: 6410381
2) Aung Cham Myae, ID: 6411325
'''
import copy
import sys
sys.setrecursionlimit(10000)


def result(board):
    maxScore = minScore = 0
    for i in range(3):
        rowScore = 0
        for j in range(3):
            rowScore += board[i][j]
        maxScore = max(maxScore, rowScore)
        minScore = min(minScore, rowScore)
    for j in range(3):
        colScore = 0
        for i in range(3):
            colScore += board[i][j]
        maxScore = max(maxScore, colScore)
        minScore = min(minScore, colScore)
    diagScore1 = 0
    for i in range(3):
        diagScore1 += board[i][i]
    maxScore = max(maxScore, diagScore1)
    minScore = min(minScore, diagScore1)
    diagScore2 = 0
    for i in range(3):
        diagScore2 += board[2-i][i]
    maxScore = max(maxScore, diagScore2)
    minScore = min(minScore, diagScore2)

    unfilled = 0
    for i in range(3):
        for j in range(3):
            if board[i][j] == 0:
                unfilled += 1

    if maxScore == 3:
        return 1    # max wins
    elif minScore == -3:
        return -1   # min wins
    else:   # no winner
        if unfilled > 0:  # game is not over yet
            return None
        return 0    # ended with a tie


class state:
    def __init__(self, board):
        self.board = copy.deepcopy(board)
        self.play = 0  # to be set later (1 for max play, -1 for min play)


def successor(u):
    succ = []
    for i in range(3):
        for j in range(3):
            if u.board[i][j] == 0:      # unfilled position
                v = copy.deepcopy(u)
                v.board[i][j] = v.play  # program's action
                v.play *= -1            # indicate that next play will be by opponent
                succ.append(v)
    return succ


def maxPlay(u, alpha, beta):
    score = result(u.board)
    if score is not None:  # ended
        return score

    max_score = float('-inf')
    for v in successor(u):
        max_score = max(max_score, minPlay(v, alpha, beta))
        alpha = max(alpha, max_score)
        if beta <= alpha:
            break  # Prune the search tree
    return max_score


def minPlay(u, alpha, beta):
    score = result(u.board)
    if score is not None:  # ended
        return score

    min_score = float('inf')
    for v in successor(u):
        min_score = min(min_score, maxPlay(v, alpha, beta))
        beta = min(beta, min_score)
        if beta <= alpha:
            break  # Prune the search tree
    return min_score


def print_board(board):
    for i in range(3):
        for j in range(3):
            if j == 2:
                ending = '\n'
            else:
                ending = '|'
            if board[i][j] == 1:
                print('X', end=ending)
            elif board[i][j] == -1:
                print('O', end=ending)
            else:
                print(' ', end=ending)
        if i < 2:
            print("-----")
        else:
            print()


def valid(r, c):
    if r < 3 and r >= 0 and c < 3 and c >= 0:
        return True
    else:
        return False


def my_turn(s):   # go for max
    v = copy.deepcopy(s)
    r, c = map(int, input("row,col = ").split(","))
    while valid(r, c) and v.board[r][c] != 0:
        print("Choose an empty position!")
        r, c = map(int, input("row,col = ").split(","))
    v.board[r][c] = 1   # my action
    v.play = -1         # indicate that next play will be by the program
    return v


def program_turn(s):
    # Among states resulted from its one-action plays, return the one with minimum score possible
    # Complete the code to find such a min_state.
    min_state = None
    beta = float('inf')
    for v in successor(s):
        v_score = maxPlay(v, -float('inf'), beta)
        if v_score < beta:
            beta = v_score
            min_state = v
    return min_state


s = state([[0]*3 for i in range(3)])
playFirst = input("Start? (y/n) : ")
if playFirst in ['y', 'Y']:
    s.play = 1
else:
    s.play = -1

score = result(s.board)
while score == None:
    if s.play == 1:
        s = my_turn(s)
    else:
        s = program_turn(s)
    print_board(s.board)
    score = result(s.board)
if score < 0:
    print('O wins')
elif score > 0:
    print('X wins')
else:
    print('Tie!')
