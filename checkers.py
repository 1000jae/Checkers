import argparse
import sys
from state import State

# gets the opponent's pieces
def get_opp(player):
    if player == 'b' or player == 'B':
        return ['r', 'R']
    else:
        return ['b', 'B']

# gets the player to make move next
def get_next(curr):
    if curr == 'r':
        return 'b'
    else:
        return 'r'

# reads the input file and creates the initial board
def get_initial_board(filename):
    file = open(filename)
    board = []
    for l in file.readlines():
        row = []
        for i in l.strip():
            row.append(i)
        board.append(row)
    return board


def copy_board(state):
    """
    Return a copy of the board of the given state
    """
    copy_board = []
    # make empty board
    for j in range(state.h):
        row = []
        for i in range(state.w):
            row.append('.')
        copy_board.append(row)

    # fill in the empty board with the same pieces as the given state
    for j in range(state.h):
        for i in range(state.w):
            if state.board[j][i] == 'r':
                copy_board[j][i] = 'r'
            elif state.board[j][i] == 'R':
                copy_board[j][i] = 'R'
            elif state.board[j][i] == 'b':
                copy_board[j][i] = 'b'
            elif state.board[j][i] == 'B':
                copy_board[j][i] = 'B'
    return copy_board


def check_hw(val):
    """
    Check if the given value is valid for a location on the board
    Returns the value if it is valid, else -1
    """
    # if the value given is less than 8 and greater than or equal to 0
    if 0 <= val < 8:
        return val
    else:
        return -1


def change_normal_to_king(state):
    """
    Crowns the normal pieces that can become king
    """
    # go through each space at the top and bottom of the board
    for i in range(state.w):
        # if there is normal red piece at the top, crown it to king
        if state.board[0][i] == 'r':
            state.board[0][i] = 'R'
        # if there is normal black piece at the bottom, crown it to king
        elif state.board[7][i] == 'b':
            state.board[7][i] == 'B'


"""
JUMPS
"""


def jump_ur(state, x, y, new_x, new_y):
    """
    Jump the piece at (x, y) to the top right
    """
    # copy the given board
    new_board = copy_board(state)
    # make the jump move on the copied board
    new_board[new_y][new_x] = state.board[y][x]
    new_board[y - 1][x + 1] = '.'
    new_board[y][x] = '.'
    # return a new state with the new board
    return State(new_board)


def jump_ul(state, x, y, new_x, new_y):
    """
    Jump the piece at (x, y) to the top left
    """
    # copy given board
    new_board = copy_board(state)
    # make the jump move on the copied board
    new_board[new_y][new_x] = state.board[y][x]
    new_board[y - 1][x - 1] = '.'
    new_board[y][x] = '.'
    # return a new state with the new board
    return State(new_board)


def jump_dr(state, x, y, new_x, new_y):
    """
    Jump the piece at (x, y) to the bottom right
    """
    new_board = copy_board(state)
    # make the jump move on the copied board
    new_board[new_y][new_x] = state.board[y][x]
    new_board[y + 1][x + 1] = '.'
    new_board[y][x] = '.'
    # return a new state with the new board
    return State(new_board)


def jump_dl(state, x, y, new_x, new_y):
    """
    Jump the piece at (x, y) to the bottom left
    """
    new_board = copy_board(state)
    # make the jump move on the copied board
    new_board[new_y][new_x] = state.board[y][x]
    new_board[y + 1][x - 1] = '.'
    new_board[y][x] = '.'
    # return a new state with the new board
    return State(new_board)


def jump_king(state, x, y, opp_pieces, multi):
    """
    Try jumping the king piece
    Return the states the jumps makes
    """

    up = check_hw(y - 2)
    down = check_hw(y + 2)
    right = check_hw(x + 2)
    left = check_hw(x - 2)

    moves = []
    new_state = None

    # if the piece can jump to the top right
    if (up != -1 and right != -1) and state.board[y - 1][
        x + 1] in opp_pieces and state.board[up][right] == '.':
        new_state = jump_ur(state, x, y, right, up)

        # check if the piece can jump more
        moves.extend(jump_king(new_state, right, up, opp_pieces, True))

    # if the piece can jump to the top left
    if (up != -1 and left != -1) and state.board[y - 1][x - 1] in opp_pieces and \
            state.board[up][left] == '.':
        new_state = jump_ul(state, x, y, left, up)

        # check if the piece can jump more
        moves.extend(jump_king(new_state, left, up, opp_pieces, True))

    # if the piece can jump to the bottom right
    if (down != -1 and right != -1) and state.board[y + 1][
        x + 1] in opp_pieces and state.board[down][right] == '.':
        new_state = jump_dr(state, x, y, right, down)

        # check if the piece can jump more
        moves.extend(jump_king(new_state, right, down, opp_pieces, True))

    # if the piece can jump to the bottom left
    if (down != -1 and left != -1) and state.board[y + 1][
        x - 1] in opp_pieces and state.board[down][left] == '.':
        new_state = jump_dl(state, x, y, left, down)

        # check if the piece can jump more
        moves.extend(jump_king(new_state, left, down, opp_pieces, True))

    # if the piece cannot be jumped
    if new_state is None:
        # if piece is being checked if it can be jumped multiple times
        if multi:
            # return the current state
            return [state]

    return moves


def jump_red(state, x, y, opp_pieces, multi):
    """
    Try jumping the normal red piece
    Return the states the jumps makes
    NOTE: red pieces move towards the top of the board
    """

    up = check_hw(y - 2)
    right = check_hw(x + 2)
    left = check_hw(x - 2)

    moves = []
    new_state = None

    # if the piece can jump to the top right
    if (up != -1 and right != -1) and state.board[y - 1][
        x + 1] in opp_pieces and state.board[up][right] == '.':
        new_state = jump_ur(state, x, y, right, up)
        # check if any piece needs to be changed to king
        change_normal_to_king(new_state)

        # check if the piece can jump more
        moves.extend(jump_red(new_state, right, up, opp_pieces, True))

    # if the piece can jump to the top left
    if (up != -1 and left != -1) and state.board[y - 1][x - 1] in opp_pieces and \
            state.board[up][left] == '.':
        new_state = jump_ul(state, x, y, left, up)
        # check if any piece needs to be changed to king
        change_normal_to_king(new_state)

        # check if the piece can jump more
        moves.extend(jump_red(new_state, left, up, opp_pieces, True))

    # if the piece cannot be jumped
    if new_state is None:
        # if piece is being checked if it can be jumped multiple times
        if multi:
            # return the current state
            return [state]

    return moves


def jump_black(state, x, y, opp_pieces, multi):
    """
    Try jumping a normal black piece
    Return the states the jump makes
    NOTE: black pieces move towards the bottom of the board
    """

    down = check_hw(y + 2)
    right = check_hw(x + 2)
    left = check_hw(x - 2)

    moves = []
    new_state = None

    # if the piece can jump to the bottom right
    if (down != -1 and right != -1) and state.board[y + 1][
        x + 1] in opp_pieces and state.board[down][right] == '.':
        new_state = jump_dr(state, x, y, right, down)
        # check if any piece needs to be changed to king
        change_normal_to_king(new_state)

        # check if the piece can jump more
        moves.extend(jump_black(new_state, right, down, opp_pieces, True))

    # if the piece can jump to the bottom left
    if (down != -1 and left != -1) and state.board[y + 1][
        x - 1] in opp_pieces and state.board[down][left] == '.':
        new_state = jump_dl(state, x, y, left, down)
        # check if any piece needs to be changed to king
        change_normal_to_king(new_state)

        # check if the piece can jump more
        moves.extend(jump_black(new_state, left, down, opp_pieces, True))

    # if the piece cannot be jumped
    if new_state is None:
        # if piece is being checked if it can be jumped multiple times
        if multi:
            # return the current state
            return [state]

    return moves


"""
SINGLE MOVES
"""


def single_ur(state, x, y):
    """
    Try to make a single move to top right of the piece given
    """
    up = check_hw(y - 1)
    right = check_hw(x + 1)

    new_state = None

    # if the piece can make a single move to top right
    if up != -1 and right != -1 and state.board[up][right] == '.':
        new_board = copy_board(state)
        # make move in the copied board and make new state with the copied board
        new_board[up][right] = state.board[y][x]
        new_board[y][x] = '.'
        new_state = State(new_board)

    return new_state


def single_ul(state, x, y):
    """
    Try to make a single move to top left of the piece given
    """
    up = check_hw(y - 1)
    left = check_hw(x - 1)

    new_state = None

    if up != -1 and left != -1 and state.board[up][left] == '.':
        new_board = copy_board(state)
        # make move in the copied board and make new state with the copied board
        new_board[up][left] = state.board[y][x]
        new_board[y][x] = '.'
        new_state = State(new_board)

    return new_state


def single_dr(state, x, y):
    """
    Try to make a single move to bottom right of the piece given
    """
    down = check_hw(y + 1)
    right = check_hw(x + 1)

    new_state = None

    if down != -1 and right != -1 and state.board[down][right] == '.':
        new_board = copy_board(state)
        # make move in the copied board and make new state with the copied board
        new_board[down][right] = state.board[y][x]
        new_board[y][x] = '.'
        new_state = State(new_board)

    return new_state


def single_dl(state, x, y):
    """
    Try to make a single move to bottom left of the piece given
    """
    down = check_hw(y + 1)
    left = check_hw(x - 1)

    new_state = None

    if down != -1 and left != -1 and state.board[down][left] == '.':
        new_board = copy_board(state)
        # make move in the copied board and make new state with the copied board
        new_board[down][left] = state.board[y][x]
        new_board[y][x] = '.'
        new_state = State(new_board)

    return new_state


def add_king(states):
    """
    Return a list of all the possible single moves the king piece can make
    """
    moves = []
    if states[0] is not None:
        moves.append(states[0])
    if states[1] is not None:
        moves.append(states[1])
    if states[2] is not None:
        moves.append(states[2])
    if states[3] is not None:
        moves.append(states[3])
    return moves


def add_normal(states):
    """
    Return a list of all the possible single moves the normal piece can make
    """
    moves = []
    if states[0] is not None:
        # check if any piece needs to be changed to king
        change_normal_to_king(states[0])
        moves.append(states[0])
    if states[1] is not None:
        # check if any piece needs to be changed to king
        change_normal_to_king(states[1])
        moves.append(states[1])
    return moves


def single_king(state, x, y):
    """
    Get all states that a single move of the king piece creates
    """
    # try to make a move in all directions
    state1 = single_ur(state, x, y)
    state2 = single_ul(state, x, y)
    state3 = single_dr(state, x, y)
    state4 = single_dl(state, x, y)

    # get list of possible moves
    moves = add_king([state1, state2, state3, state4])

    return moves


def single_red(state, x, y):
    """
    Get all states that a single move of the normal red piece creates
    NOTE: red pieces move toward the top of the board
    """
    # try to move piece in both directions
    state1 = single_ur(state, x, y)
    state2 = single_ul(state, x, y)

    # get list of all possible moves
    moves = add_normal([state1, state2])

    return moves


def single_black(state, x, y):
    """
    Get all states that a single move of the normal black piece creates
    NOTE: black pieces move toward the bottom of the board
    """
    # try to move piece in both directions
    state1 = single_dr(state, x, y)
    state2 = single_dl(state, x, y)

    # get list of all possible moves
    moves = add_normal([state1, state2])

    return moves


"""
UTILITY/EVALUATION
"""


def utility(depth, curr_turn, succ, red_num, black_num):
    """
    Return the utility of a terminal state
    """
    # if current player cannot make any moves, current turn player lose
    if succ == []:
        if curr_turn == 'r':
            return -500000 + depth
        else:
            return 500000 - depth
    # if no red pieces only,  red lose
    if red_num == 0 and black_num != 0:
        return -500000 + depth
    # if no black pieces only, black lose
    if red_num != 0 and black_num == 0:
        return 500000 - depth
    # else, draw
    return 0


def get_factor_pieces(state):
    """
    Calculate the number of king and normal pieces each player has on the board
    """
    # index 0 = normal, index 1 = king
    red = [0, 0]
    black = [0, 0]
    for j in range(state.h):
        for i in range(state.w):
            if state.board[j][i] == 'r':
                red[0] += 1
            elif state.board[j][i] == 'R':
                red[1] += 1
            elif state.board[j][i] == 'b':
                black[0] += 1
            elif state.board[j][i] == 'B':
                black[1] += 1

    return red, black


def eval(state):
    """
    Return an estimate utility for the state given
    """
    estimate = 0
    # get number of kings and normal pieces each player has
    red, black = get_factor_pieces(state)

    # w: normal = 1, king = 4
    normal_score = (red[0] - black[0])
    estimate += normal_score
    king_score = 4 * (red[1] - black[1])
    estimate += king_score

    return estimate


"""
alpha beta pruning 
"""


def get_succ(state, curr_turn):
    """
    Return a list of all the successor states the given state creates
    when moving curr_turn pieces
    """
    jumps = []
    single = []

    # opposite player's pieces
    opp = get_opp(curr_turn)

    for j in range(state.h):
        for i in range(state.w):
            # if the piece is a normal piece
            if state.board[j][i] == curr_turn:
                # if the current player is red
                if curr_turn == 'r':
                    # try jumping first
                    jumps.extend(jump_red(state, i, j, opp, False))
                    # if a jump cannot be done for any of the player's pieces
                    if jumps == []:
                        # try making single move
                        single.extend(single_red(state, i, j))
                # if the current player is black
                else:
                    jumps.extend(jump_black(state, i, j, opp, False))
                    if jumps == []:
                        single.extend(single_black(state, i, j))

            # if the piece is a king
            elif state.board[j][i] == curr_turn.upper():
                jumps.extend(jump_king(state, i, j, opp, False))
                if jumps == []:
                    single.extend(single_king(state, i, j))

    # # if there are no jump moves made, make single moves
    if jumps == []:
        return single
    # else make jump moves only
    else:
        return jumps


def get_num_pieces(state):
    """
    Return the number of pieces each player have
    """
    red_num = 0
    black_num = 0
    for j in range(state.h):
        for i in range(state.w):
            if state.board[j][i] in ['r', 'R']:
                red_num += 1
            elif state.board[j][i] in ['b', 'B']:
                black_num += 1
    return red_num, black_num


def alphabeta(state, alpha, beta, depth, curr_turn):
    """
    Alpha-Beta Pruning Algorithm
    """
    best_move = None
    # get the successors of the current state
    successors = get_succ(state, curr_turn)
    # get number of pieces each player has on the board
    red_num, black_num = get_num_pieces(state)

    # if the player cannot make any moves or
    # one of the player does not have any pieces on board
    if successors == [] or black_num == 0 or red_num == 0:
        # get exact utility
        return best_move, utility(depth, curr_turn, successors, red_num,
                                  black_num)

    # if the depth limit is reached
    if depth == 0:
        # get estimate of the utility
        return best_move, eval(state)

    # if the current player is the max player
    if curr_turn == 'r':
        val = float('-inf')

    # if the current player is the min player
    else:
        val = float('inf')

    # go through each possible successor
    for succ in successors:
        # look through the successors of the current successor
        next_move, next_val = alphabeta(succ, alpha, beta, depth - 1,
                                        get_next(curr_turn))

        # if the current player is the max player
        if curr_turn == 'r':
            if val < next_val:
                # assign the current successor as the next move
                state.next = succ
                best_move, val = succ, next_val
            if val >= beta:
                return best_move, val
            alpha = max(alpha, val)

        # if the current player is the min player
        else:
            if val > next_val:
                # assign the current successor as the next move
                state.next = succ
                best_move, val = succ, next_val
            if val <= alpha:
                return best_move, val
            beta = min(beta, val)

    return best_move, val


def print_result(state):
    """
    Print the resulting sequence of states
    """
    curr = state

    while curr is not None:
        curr.display()
        curr = curr.next


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

    # get initial board state
    initial_board = get_initial_board(args.inputfile)
    state = State(initial_board)

    # output the results in another file
    with open(args.outputfile, 'w') as sys.stdout:
        state.display()
        result, val = alphabeta(state, float('-inf'), float('inf'), 10, 'r')
        if result:
            print_result(result)
