class State:
    """
    Represents a state 8x8 checkers board.
    The class was given by the instructor as source code for this assignment.
    """
    def __init__(self, board):
        # board: a list of lists that represents a 8x8 checkers board
        # w: integer value representing the width of the board
        # h: integer value representing the height of the board
        # next: a pointer to the next board state
        self.next = None
        self.board = board
        self.w = 8
        self.h = 8

    # displays the board of the state
    def display(self):
        for i in self.board:
            print(''.join(i))
        print()
