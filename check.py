import argparse
import copy
import sys
import time

cache = {} # you can use this to implement state caching

class State:
    # This class is used to represent a state.
    # board : a list of lists that represents the 8*8 board
    def __init__(self, board):
        self.next = None
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
def check_hw(val):
    if 0 <= val < 8:
        return val
    else:
        return -1

# check if the piece is able to crown to a king
def check_to_king(y):
    if y == 7 or y == 0:
        return True
    else:
        return False

"""
JUMPS
"""
def jump_king(state, x, y, opp_pieces, multi):
    up = check_hw(y - 2)
    down = check_hw(y + 2)
    right = check_hw(x + 2)
    left = check_hw(x - 2)

    moves = []
    new_state = None

    if (up!= -1 and right != -1) and state.board[y - 1][x + 1] in opp_pieces and state.board[up][right] == '.':
        new_state = jump_ur(state, x, y, right, up)
        new_state.display()
        moves.extend(jump_king(new_state, right, up, opp_pieces, True))

    if (up!= -1 and left != -1) and state.board[y - 1][x - 1] in opp_pieces and state.board[up][left] == '.':
        new_state = jump_ul(state, x, y, left, up)
        new_state.display()
        moves.extend(jump_king(new_state, left, up, opp_pieces, True))

    if (down!= -1 and right != -1) and state.board[y + 1][x + 1] in opp_pieces and state.board[down][right] == '.':
        new_state = jump_dr(state, x, y, right, down)
        new_state.display()
        moves.extend(jump_king(new_state, right, down, opp_pieces, True))

    if (down!= -1 and left != -1) and state.board[y + 1][x - 1] in opp_pieces and state.board[down][left] == '.':
        new_state = jump_dl(state, x, y, left, down)
        new_state.display()
        moves.extend(jump_king(new_state, left, down, opp_pieces, True))

    if new_state is None:
        if multi:
            print("MULTI: ")
            state.display()
            return [state]

    return moves

def jump_red(state, x, y, opp_pieces, multi):
    up = check_hw(y - 2)
    right = check_hw(x + 2)
    left = check_hw(x - 2)

    moves = []
    new_state = None

    if (up!= -1 and right != -1) and state.board[y - 1][x + 1] in opp_pieces and state.board[up][right] == '.':
        new_state = jump_ur(state, x, y, right, up)
        new_state.display()
        moves.extend(jump_red(new_state, right, up, opp_pieces, True))

    if (up!= -1 and left != -1) and state.board[y - 1][x - 1] in opp_pieces and state.board[up][left] == '.':
        new_state = jump_ul(state, x, y, left, up)
        new_state.display()
        moves.extend(jump_red(new_state, left, up, opp_pieces, True))

    if new_state is None:
        if multi:
            return [state]

    return moves


def jump_black(state, x, y, opp_pieces, multi):
    down = check_hw(y + 2)
    right = check_hw(x + 2)
    left = check_hw(x - 2)

    moves = []
    new_state = None

    if (down!= -1 and right != -1) and state.board[y + 1][x + 1] in opp_pieces and state.board[down][right] == '.':
        new_state = jump_dr(state, x, y, right, down)
        new_state.display()
        moves.extend(jump_black(new_state, right, down, opp_pieces, True))

    if (down!= -1 and left != -1) and state.board[y + 1][x - 1] in opp_pieces and state.board[down][left] == '.':
        new_state = jump_dl(state, x, y, left, down)
        new_state.display()
        moves.extend(jump_black(new_state, left, down, opp_pieces, True))

    if new_state is None:
        if multi:
            return [state]

    return moves


def jump_ur(state, x, y, new_x, new_y):
    new_board = copy_board(state)
    new_board[new_y][new_x] = state.board[y][x]
    new_board[y - 1][x + 1] = '.'
    new_board[y][x] = '.'
    return State(new_board)

def jump_ul(state, x, y, new_x, new_y):
    new_board = copy_board(state)
    new_board[new_y][new_x] = state.board[y][x]
    new_board[y - 1][x - 1] = '.'
    new_board[y][x] = '.'
    return State(new_board)

def jump_dr(state, x, y, new_x, new_y):
    new_board = copy_board(state)
    new_board[new_y][new_x] = state.board[y][x]
    new_board[y + 1][x + 1] = '.'
    new_board[y][x] = '.'
    return State(new_board)

def jump_dl(state, x, y, new_x, new_y):
    new_board = copy_board(state)
    new_board[new_y][new_x] = state.board[y][x]
    new_board[y + 1][x - 1] = '.'
    new_board[y][x] = '.'
    return State(new_board)

"""
SINGLE MOVES
"""
# single move top right
def single_ur(state, x, y):
    up = check_hw(y - 1)
    right = check_hw(x + 1)

    new_state = None
    # if up, right valid
    if up != -1 and right != -1:
        # check if the spot is empty
        if state.board[up][right] == '.':
            # move piece to new spot
            new_board = copy_board(state)
            new_board[up][right]  = state.board[y][x]
            new_board[y][x] = '.'
            new_state = State(new_board)
            new_state.display()
    return new_state

# single move top left
def single_ul(state, x, y):
    up = check_hw(y - 1)
    left = check_hw(x - 1)

    new_state = None

    if up != -1 and left != -1:
        if state.board[up][left] == '.':
            new_board = copy_board(state)
            new_board[up][left]  = state.board[y][x]
            new_board[y][x] = '.'
            new_state = State(new_board)
            new_state.display()
    return new_state

# single move bottom right
def single_dr(state, x, y):
    down = check_hw(y + 1)
    right = check_hw(x + 1)

    new_state = None

    if down != -1 and right != -1:
        if state.board[down][right] == '.':
            new_board = copy_board(state)
            new_board[down][right]  = state.board[y][x]
            new_board[y][x] = '.'
            new_state = State(new_board)
            new_state.display()
    return new_state

# single move bottom left
def single_dl(state, x, y):
    down = check_hw(y + 1)
    left = check_hw(x - 1)

    new_state = None

    if down != -1 and left != -1:
        if state.board[down][left] == '.':
            new_board = copy_board(state)
            new_board[down][left]  = state.board[y][x]
            new_board[y][x] = '.'
            new_state = State(new_board)
            new_state.display()
    return new_state

# add all the single moves given in parameter in list
def add_move(states):
    moves = []
    if states[0] != None:
        moves.append(states[0])
    if states[1] != None:
        moves.append(states[1])
    if len(states) > 2:
        if states[2] != None:
            moves.append(states[2])
        if states[3] != None:
            moves.append(states[3])
    return moves

# single move a king piece
def single_king(state, x, y):
    state1 = single_ur(state, x, y)
    state2 = single_ul(state, x, y)
    state3 = single_dr(state, x, y)
    state4 = single_dl(state, x, y)

    moves = add_move([state1, state2, state3, state4])

    return moves

# single move a red normal piece
def single_red(state, x, y):
    # red normal piece moves up
    state1 = single_ur(state, x, y)
    state2 = single_ul(state, x, y)

    moves = add_move([state1, state2])

    return moves

# single move a black normal piece
def single_black(state, x, y):
    # black normal piece moves down
    state1 = single_dr(state, x, y)
    state2 = single_dl(state, x, y)

    moves = add_move([state1, state2])

    return moves


"""
get successor
"""
def get_succ(state, curr_turn):
    jumps = []
    single = []
    succ = []

    # opposite player's pieces
    opp = get_opp_char(curr_turn)

    for j in range(state.height):
        for i in range(state.width):
            if state.board[j][i] == curr_turn:
                # first try to jump
                # if jump is not possible, single move
                # if jump is possible, ignore single moves
                if curr_turn == 'r':
                    print("jumps")
                    red = jump_red(state, i, j, opp, False)
                    jumps.extend(red)
                    if red == [] or jumps == []:
                        print("single")
                        red = single_red(state, i, j)
                        single.extend(red)

                else:
                    print("jumps")
                    black = jump_black(state, i, j, opp, False)
                    jumps.extend(black)
                    if black == [] or jumps == []:
                        print("single")
                        black = single_black(state, i, j)
                        single.extend(black)
            elif state.board[j][i] == curr_turn.upper():
                # first try to jump
                # if jump is not possible, single move
                # if jump is possible, ignore single moves
                print("jumps")
                king = jump_king(state, i, j, opp, False)
                jumps.extend(king)
                if king == [] or jumps == []:
                    print("single")
                    king = single_king(state, i, j)
                    single.extend(king)

    succ.extend(jumps)
    succ.extend(single)

    return succ


"""
evaluation factors
"""
# get the number of normal and king pieces per player
def get_factor_pieces(state):
    # index 0 = normal, index 1 = king
    red = [0, 0]
    black = [0, 0]
    for j in range(state.height):
        for i in range(state.width):
            if state.board[j][i] == 'r':
                red[0] += 1
            elif state.board[j][i] == 'R':
                red[1] += 1
            elif state.board[j][i] == 'b':
                black[0] += 1
            elif state.board[j][i] == 'B':
                black[1] += 1

    return red, black

# get the score of normal piece of each player getting crowned to king depending on the distance to top/bottom of board
def get_factor_crown(state):
    red = 0
    black = 0

    for j in range(state.height):
        for i in range(state.width):
            if state.board[j][i] == 'r':
                # distance from the top of the board
                dist = j - 0
                red += (7 - dist)
            elif state.board[j][i] == 'b':
                dist = 7 - j
                black += (7 - dist)
    return red, black

# return the weight associated with the given coord (x, y)
def get_weight(coord, weight):
    if coord in weight[0.5]:
        return 0.5
    elif coord in weight[0.4]:
        return 0.4
    elif coord in weight[0.3]:
        return 0.3
    else:
        return 0.2

# get the score representing the closeness of each piece per player to the center of the board
def get_factor_center(state):
    red = 0
    black = 0

    weight = {
        0.5: [(3, 3), (3, 4), (4, 3), (4, 4)],
        0.4: [(2, 2), (3, 2), (4, 2), (5, 2), (2, 3), (5, 3),
              (2, 4), (5, 4), (2, 5), (3, 5), (4, 5), (5, 5)],
        0.3: [(1, 1), (2, 1), (3, 1), (4, 1), (5, 1), (6, 1),
              (1, 2), (6, 2), (1, 3), (6, 3), (1, 4), (6, 4), (1, 5), (6, 5),
              (1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 6)]
    }

    for j in range(state.height):
        for i in range(state.width):
            if state.board[j][i] in ['r', 'R']:
                red += get_weight((i, j), weight)
            elif state.board[j][i] in ['b', 'B']:
                black += get_weight((i, j), weight)
    return red, black

"""
utility/evaluation 
"""
# get utility of terminal state
def utility(depth, curr_turn, succ, red_num, black_num):
    # if succ == [] => current turn player lose
    if succ == []:
        if curr_turn == 'r':
            return -500000 + depth
        else:
            return 500000 - depth
    # if only red_num == 0 => red lose
    if red_num == 0 and black_num != 0:
        return -500000 + depth
    # if only black_num == 0 => black lose
    if red_num != 0 and black_num == 0:
        return 500000 - depth
    # if none of the above => draw
    if red_num == black_num:
        return 0

# get acutal/estimate utility
def eval(state, curr_turn, depth, succ, red_num, black_num):
    # if terminal => when one of the pieces = 0 or succ of current == []
    if succ == [] or black_num == 0 or red_num == 0:
        return utility(depth, curr_turn, succ, red_num, black_num)
    # if not terminal => estimate utility
    # get the factors and add them up
    # factors: num of normal vs kings, num of pieces close to kinging, location of each player's pieces, depth(?)
    estimate = 0
    red, black = get_factor_pieces(state)

    # nnum of normal and kings
    # normal = 2, king = 4
    normal_score = red[0] - black[0]
    estimate += normal_score
    king_score = 4 * (red[1] - black[1])
    estimate += king_score

    # distance of normal pieces from crowning
    red_k, black_k = get_factor_crown(state)
    crown_score = red_k - black_k
    estimate += crown_score

    # distance of pieces from the center
    red_c, black_c = get_factor_center(state)
    center_score = red_c - black_c
    estimate += center_score

    print(f"estimate: {estimate}")
    # depth
    if curr_turn == 'r':
        estimate += depth
    else:
        estimate -= depth
    return estimate


"""
alpha beta pruning 
"""
# get the number of pieces each player have
def get_num_pieces(state):
    red_num = 0
    black_num = 0
    for j in range(state.height):
        for i in range(state.width):
            if state.board[j][i] in ['r', 'R']:
                red_num += 1
            elif state.board[j][i] in ['b', 'B']:
                black_num += 1
    return red_num, black_num

# alpha-beta algorithm
def alphabeta(state, alpha, beta, depth, curr_turn):
    best_move = None
    print(f"TURN: {curr_turn}")
    state.display()
    print()
    # get the successors of the current state
    successors = get_succ(state, curr_turn)
    # get number of pieces each player has on the board
    red_num, black_num = get_num_pieces(state)

    # if the depth limit is reached/no possible moves/one of the players do not have any pieces
    if depth == 0 or successors == [] or red_num == 0 or black_num == 0:
        # evalulate the utility
        return best_move, eval(state, curr_turn, depth, successors, red_num, black_num)

    # if the current player is the max player
    if curr_turn == 'r':
        val = float('-inf')

    # if the current player is the min player
    else:
        val = float('inf')

    # go through each possible successor
    for succ in successors:
        # look through the successors of the succ
        next_move, next_val = alphabeta(succ, alpha, beta, depth - 1, get_next_turn(curr_turn))
        print("NEXT")
        if next_move is not None:
            next_move.display()
            print(next_val)
            print()
        # if the current player is the max player
        if curr_turn == 'r':
            if val <= next_val:
                state.next = succ
                best_move, val = succ, next_val
            if val > beta:
                break
            alpha = max(alpha, val)

        # if the current player is the min player
        else:
            if val >= next_val:
                state.next = succ
                best_move, val = succ, next_val
            if val < alpha:
                break
            beta = min(beta, val)

    return best_move, val


def print_result(state):
    curr = state

    while curr is not None:
        curr.display()
        curr = curr.next


if __name__ == '__main__':

    # parser = argparse.ArgumentParser()
    # parser.add_argument(
    #     "--inputfile",
    #     type=str,
    #     required=True,
    #     help="The input file that contains the puzzles."
    # )
    # parser.add_argument(
    #     "--outputfile",
    #     type=str,
    #     required=True,
    #     help="The output file that contains the solution."
    # )
    # args = parser.parse_args()

    initial_board = read_from_file("checkers5.txt")
    state = State(initial_board)
    turn = 'r'
    ctr = 0

    # sys.stdout = open(args.outputfile, 'w')

    # sys.stdout = sys.__stdout__

    with open("puzzle5_sol.txt", 'w') as sys.stdout:
        result, val = alphabeta(state, -1, 1, 9, turn)
        if result:
            print("RESULT")
            state.display()
            print_result(result)

