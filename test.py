import argparse
import copy
import sys
import time

cache = {} # you can use this to implement state caching

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):
        self.parent = None
        self.board = board
        self.width = 8
        self.height = 8
        

    # function to display the board
    def display(self):
        for i in self.board:
            for j in i:
                print(j, end="")
            print("")
        print("")


# get the opponent players
def get_opp_char(player):
    if player in ['b', 'B']:
        return ['r', 'R']
    else:
        return ['b', 'B']

# return which player is next
def get_next_turn(curr_turn):
    if curr_turn == 'r':
        return 'b'
    else:
        return 'r'

# read file 
def read_from_file(filename):

    f = open(filename)
    lines = f.readlines()
    board = [[str(x) for x in l.rstrip()] for l in lines]
    f.close()

    return board

def copy_board(state):
    copy = []
    for j in range(state.height):
        row = []
        for i in range(state.width):
            row.append('.')
        copy.append(row)
    
    for j in range(state.height):
        for i in range(state.width):
            if state.board[j][i] == 'r':
                copy[j][i] = 'r'
            elif state.board[j][i] == 'R':
                copy[j][i] = 'R'
            elif state.board[j][i] == 'b':
                copy[j][i] = 'b'
            elif state.board[j][i] == 'B':
                copy[j][i] = 'B'
    return copy

# check if the value is valid height or width
def check_hw(val, dim):
    if 0 <= val < dim:
        return val
    else:
        return -1
    
# check if the piece is able to crown to a king
def check_to_king(y):
    if y == 7 or y == 0:
        return True
    else:
        return False

# jump the piece to the new position and remove the captured piece
def create_jump_board(state, x, y, new_x, new_y, dir1, dir2):
    to_king = False

    new_board = copy_board(state)
    if check_to_king(new_y) and new_board[y][x] not in ['R', 'B']:
        to_king = True
    if to_king:
        new_board[new_y][new_x] = new_board[y][x].upper()
    else:
        new_board[new_y][new_x] = new_board[y][x]
    new_board[y][x] = '.'
    new_board[y + dir1][x + dir2] = '.'
    return State(new_board)

# jump a king piece
def jump_king(state, x, y, opp_pieces, multi):
    up = check_hw(y - 2, state.height)
    down = check_hw(y + 2, state.height)
    right = check_hw(x + 2, state.width)
    left = check_hw(x - 2, state.width)

    moves = []

    if (up!= -1 and right != -1) and state.board[y - 1][x + 1] in opp_pieces and state.board[up][right] == '.':
        new_state = create_jump_board(state, x, y, right, up, -1, 1)
        new_state.display()
        moves.extend(jump_king(new_state, right, up, opp_pieces, True))

    if (up!= -1 and left != -1) and state.board[y - 1][x - 1] in opp_pieces and state.board[up][left] == '.':
        new_state = create_jump_board(state, x, y, left, up, -1, -1)
        new_state.display()
        moves.extend(jump_king(new_state, left, up, opp_pieces, True))

    if (down!= -1 and right != -1) and state.board[y + 1][x + 1] in opp_pieces and state.board[down][right] == '.':
        new_state = create_jump_board(state, x, y, right, down, 1, 1)
        new_state.display()
        moves.extend(jump_king(new_state, right, down, opp_pieces, True))

    if (down!= -1 and left != -1) and state.board[y + 1][x - 1] in opp_pieces and state.board[down][left] == '.':
        new_state = create_jump_board(state, x, y, left, down, 1, -1)
        new_state.display()
        moves.extend(jump_king(new_state, left, down, opp_pieces, True))
    
    else:
        if multi:
            moves.extend([state])
    
    return moves


def jump_normal(state, x, y, opp_pieces, curr_turn, multi):
    right = check_hw(x + 2, state.width)
    left = check_hw(x - 2, state.width)
    moves = []
    
    if curr_turn == 'r':
        up = check_hw(y - 2, state.height)
        if (up!= -1 and right != -1) and state.board[y - 1][x + 1] in opp_pieces and state.board[up][right] == '.':
            new_state = create_jump_board(state, x, y, right, up, -1, 1)
            new_state.display()
            # print(new_state == True)
            if check_to_king(up):
                moves.append(new_state)
                return moves
            moves.extend(jump_normal(new_state, right, up, opp_pieces, curr_turn, True))

        if (up!= -1 and left != -1) and state.board[y - 1][x - 1] in opp_pieces and state.board[up][left] == '.':
            new_state = create_jump_board(state, x, y, left, up, -1, -1)
            new_state.display()
            # print(new_state == True)
            if check_to_king(up):
                moves.append(new_state)
                return moves
            moves.extend(jump_normal(new_state, left, up, opp_pieces, curr_turn, True))
        
        else:
            if multi:
                moves.extend([state])            
    
    else:
        down = check_hw(y + 2, state.height)
        if (down!= -1 and right != -1) and state.board[y + 1][x + 1] in opp_pieces and state.board[down][right] == '.':
            new_state = create_jump_board(state, x, y, right, down, 1, 1)
            new_state.display()
            if check_to_king(down):
                moves.append(new_state)
                return moves
            moves.extend(jump_normal(new_state, right, down, opp_pieces, curr_turn, True))

        if (down!= -1 and left != -1) and state.board[y + 1][x - 1] in opp_pieces and state.board[down][left] == '.':
            new_state = create_jump_board(state, x, y, left, down, 1, -1)
            new_state.display()
            if check_to_king(down):
                moves.append(new_state)
                return moves
            moves.extend(jump_normal(new_state, left, down, opp_pieces, curr_turn, True))

        else:
            if multi:
                moves.extend([state])
        
    return moves


# helper function to generate all possible jump sequences
def get_jumps(state, x, y, opp_pieces, curr_turn, isKing):
    # print("jumps!\n")
    moves = []

    if isKing:
        moves.extend(jump_king(state, x, y, opp_pieces, False))
    else:
        moves.extend(jump_normal(state, x, y, opp_pieces, curr_turn, False))

    return moves

# make simple move to new position
def create_simple_board(state, new_x, new_y, x, y):
    to_king = False
    new_board = copy_board(state)
    # print("COPY\n")
    if check_to_king(new_y) and new_board[y][x] not in ['R', 'B']:
        to_king = True
    if to_king:
        new_board[new_y][new_x] = new_board[y][x].upper()
    else:
        new_board[new_y][new_x] = new_board[y][x]
    new_board[y][x] = '.'
    n = State(new_board)
    # n.display()
    return n

# simple move a king
def simple_move_king(state, x, y):
    up = check_hw(y - 1, state.height)
    down = check_hw(y + 1, state.height)
    right = check_hw(x + 1, state.width)
    left = check_hw(x - 1, state.width)

    moves = []

    if up!= -1:
        if right != -1 and state.board[up][right] == '.':
            new_state = create_simple_board(state, right, up, x, y)
            new_state.display()
            moves.append(new_state)
        if left != -1 and state.board[up][left] == '.':
            new_state = create_simple_board(state, left, up, x, y)
            new_state.display()
            moves.append(new_state)
        
    if down != -1:
        if right != -1 and state.board[down][right] == '.':
            new_state = create_simple_board(state, right, down, x, y)
            new_state.display()
            moves.append(new_state)
        if left != -1 and state.board[down][left] == '.':
            new_state = create_simple_board(state, left, down, x, y)
            new_state.display()
            moves.append(new_state)
    
    return moves  

# simple move a normal piece
def simple_move_normal(state, x, y, curr_turn):
    up = check_hw(y - 1, state.height)
    down = check_hw(y + 1, state.height)
    right = check_hw(x + 1, state.width)
    left = check_hw(x - 1, state.width)

    moves = []

    if curr_turn == 'r':
        if up != -1:
            if right != -1 and state.board[up][right] == '.':
                new_state = create_simple_board(state, right, up, x, y)
                new_state.display()
                # print(f"up right: h = {up}, w = {right}\n")
                # new_state.display()
                moves.append(new_state)
            if left != -1 and state.board[up][left] == '.':
                new_state = create_simple_board(state, left, up, x, y)
                new_state.display()
                # print(f"up right: h = {up}, w = {left}\n")
                # new_state.display()
                moves.append(new_state)
    
    else:
        if down != -1:
            if right != -1 and state.board[down][right] == '.':
                print(f"height = {down} width = {right}\n")
                new_state = create_simple_board(state, right, down, x, y)
                new_state.display()
                moves.append(new_state)
            if left != -1 and state.board[down][left] == '.':
                print(f"height = {down} width = {left}\n")
                new_state = create_simple_board(state, left, down, x, y)
                new_state.display()
                moves.append(new_state)
    
    print("num_simple_normal moves = ")
    print(len(moves))
    print("")
    return moves


def get_simple_moves(state, x, y, curr_turn, isKing):
    moves = []

    if isKing:
        moves.extend(simple_move_king(state, x, y))
    else:
        moves.extend(simple_move_normal(state, x, y, curr_turn))

    return moves

# def get_moves(x, y, state, opp_pieces, curr_turn, isKing):
#     moves = []

#     moves = get_jumps(state, x, y, opp_pieces, curr_turn, isKing)
#     if moves == []:
#         print("simple\n")
#         moves.extend(get_simple_moves(state, x, y, curr_turn, isKing))
#     return moves


# generate successor
def get_succ(state, curr_turn):
    # returns list of all successor states
    succ = []
    pieces = []
    player_piece = []
    jump = False

    # possible pieces of current player
    if curr_turn == 'r':
        player_piece = ['r', 'R']
    else:
        player_piece = ['b', 'B']

    # get opponent's possible pieces
    opp_piece = get_opp_char(curr_turn)

    # get a list of all the current player's pieces index on the board 
    for j in range(state.height):
        for i in range(state.width):
            if state.board[j][i] in player_piece:
                pieces.append((j, i))
                print(f"height = {j} width = {i}\n")
    
    # two types of moves: simple moves and jumps
    for j, i in pieces:
        # the current piece looking at
        curr = state.board[j][i]
        print("get succ CURRENT BOARD")
        print(f"curr_piece = {curr}")
        # if the piece is a king
        if curr == player_piece[1]:
            # look both up and down
            succ.extend(get_jumps(state, i, j, opp_piece, curr_turn, True))
            if succ != []:
                jump == True
            if not jump:
                succ.extend(get_simple_moves(state, i, j, curr_turn, True))
        # if the piece is normal
        else:
            # can move only forward
            succ.extend(get_jumps(state, i, j, opp_piece, curr_turn, False))
            if succ != []:
                jump == True
            print(f"Jumping: {jump}")
            if not jump:
                succ.extend(get_simple_moves(state, i, j, curr_turn, False))

    return succ

def get_center_score(state, x, y, score):
    if state.board[y][x] in ['r', 'R']:
        return score
    else:
        return -1 * score

def check_center(state):
    """
    0,7 = 0.1
    1,6 = 0.2
    2,5 = 0.3
    3,4 not center = 0.4
    3,4 center = 0.5
    """
    score = 0
    away = [(0, 7), (1, 6), (2, 5)]
    center_squares = [(3, 3), (3, 4), (4, 3), (4, 4)]

    for j in range(state.height):
        for i in range(state.width):
            if j in away[0]:
                score += get_center_score(state, i, j, 1)
            elif j in away[1]:
                score += get_center_score(state, i, j, 2)
            elif j in away[2]:
                score += get_center_score(state, i, j, 3)
            else:
                if (j, i) in center_squares:
                    score += get_center_score(state, i, j, 5)
                else:
                    score += get_center_score(state, i, j, 4)
    
    return score

# def check_crown_king(state):
#     crown_r = 0
#     crown_b = 0

#     for i in range(state.width):
#          # check the top of the board for any red pieces
#         if state.board[0][i] in ['r', 'R']:
#             crown_r += 1
#          # check the bottom of the board for any black pieces
#         if state.board[7][i] in ['b', 'B']:
#             crown_b += 1

#     return crown_r, crown_b

def get_num_pieces(state):
    red = 0
    red_king = 0
    black = 0
    black_king = 0

    for j in range(state.height):
        for i in range(state.width):
            if state.board[j][i] == 'r':
                red += 1
            elif state.board[j][i] == 'R':
                red_king += 1
            elif state.board[j][i] == 'b':
                black += 1
            elif state.board[j][i] == 'B':
                black_king += 1

    return red, black, red_king, black_king

"""
actual utility
"""
def utility(depth, num_pieces, moves, curr_turn):
    # computes a player's utility of a terminal state
    # utility a very high number for the winning player 
    # in a state where the game has ended, 
    # and incorporating the depth that the winning position occurs at into the utility.
    # num_red, num_black = get_num_pieces(state)

    num_red = num_pieces[0] + num_pieces[2]
    num_black = num_pieces[1] + num_pieces[3]

    # if red wins
    if (num_black == 0 and num_red > 0) or (curr_turn == 'b' and moves == []):
        return 5000 + depth
    # if draw
    if num_black == num_red:
        return 0
    # if black wins
    if num_red == 0 and num_black > 0 or (curr_turn == 'r' and moves == []):
        return -5000 + depth
    

# evaluation function: estimate utility
def eval(state, depth, curr_turn, moves, num_pieces):
    """
    weights:
        normal piece = 4
        king = 10
        center = 5
        crowning king = 2
    """
    # crown_r, crown_b = check_crown_king(state)
    center_score = check_center(state)

    # if terminal
    if moves == [] or (num_pieces[1] + num_pieces[3]) == 0 or (num_pieces[0] + num_pieces[2]) == 0:
        return utility(depth, num_pieces, moves, curr_turn)
    # non terminal
    else:
        print("eval board")
        state.display()
        
        # estimate
        normal_piece = 1 * (num_pieces[0] - num_pieces[1])
        king_piece = 2 * (num_pieces[2] - num_pieces[2])
        # crown_score = 2 * (crown_r - crown_b)
        total = normal_piece + king_piece + center_score
        print(total)
        return total


# alpha beta pruning
def ab_pruning(state, alpha, beta, depth, curr_turn, max_player):
    # return best move for player (the position)
    # and MAX's value for pos
    print("CURRENT STATE")
    state.display()
    best_move = state
    val = 0
    opp_num = 0
    curr_num = 0
    print(f"curr_turn = {curr_turn}")
    poss_succ = get_succ(state, curr_turn)
    print("----------------------------------")
    num_pieces = get_num_pieces(state)
    # print("POSS_SUCC\n")
    # for i in poss_succ:
    #     i.display()
    #     print("")
    # if the current pos == terminal (no child) => return best, utility(pos)
    # if player(pos) == MAX => value -= -inf
    # if player(pos) == MIN => value = inf
    if curr_turn == max_player:
        val = -5000
        opp_num = (num_pieces[1] + num_pieces[3])
        curr_num = (num_pieces[0] + num_pieces[2])
        print(f"black num = {opp_num}")
    else:
        val = 5000
        opp_num = (num_pieces[0] + num_pieces[2])
        curr_num = (num_pieces[1] + num_pieces[3])

    if depth == 0 or poss_succ == [] or opp_num == 0 or curr_num == 0:
        return best_move, eval(state, depth, curr_turn, poss_succ,num_pieces)
        

    for succ in poss_succ:
        # print(curr_turn)
        # print("succ")
        # succ.display()
        next_move, next_val = ab_pruning(succ, alpha, beta, depth - 1, get_next_turn(curr_turn), max_player)
        # print("next")
        # next_move.display()
        # print(f"val = {val}, beta = {beta}")
        if curr_turn == max_player:
            if val <= next_val:
                val, best_move = next_val, next_move
            if val > beta:
                return best_move, val
            alpha = max(alpha, val)
        
        else:
            if val >= next_val:
                val, best_move = next_val, next_move
            if val < alpha:
                return best_move, val
            beta = min(beta, val)
        print("BEST")
        best_move.display()   
    return best_move, val

def print_result(state):
    curr = state
    states = []
    while curr is not None:
        states.append(curr)
        curr = curr.parent
    
    while len(states) != 1:
        states.pop().display()
        print("")
    states.pop().display()

    
if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--inputfile",
        type=str,
        required=True,
        help="The input file that contains the puzzles."
    )
    parser.add_argument(
        "--outputfile",
        type=str,
        required=True,
        help="The output file that contains the solution."
    )
    args = parser.parse_args()

    initial_board = read_from_file(args.inputfile)
    state = State(initial_board)
    turn = 'r'
    ctr = 0

    with open(args.outputfile, 'w') as sys.stdout:
        result = ab_pruning(state, -1, 1, 4, turn, turn)
        print("final\n")
        print(result[0].display())
        # if result:
            # print_result(result[0])
            
    # sys.stdout = open(args.outputfile, 'w')

    # sys.stdout = sys.__stdout__

