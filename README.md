# Checkers

Goal: Find the best result for the red players using Alpha-Beta Pruning.


Pieces
- "R" or "B": king pieces
- "r" or "b": single pieces

Rules
1. Red starts at the bottom three rows and Balck starts at top three rows. 
2. Movements: simple move or jump
    - Simple Move: move piece one square diagonally to adjacent unoccupied space. King pieces can move in all different directions. Single pieces can only move forward. 
    - Jump: move piece diagonally adjacent to an opponent's piece to an empty square immediately beyond it in the same direction. King pieces can move in all different directions. Single pieces can only move forward. A jumped piece is "captured" an removed from the board. 
3. Jumping is mandatory. Jumping is prioritized over Simple moves. 
4. Multiple Jumps are done if possible. 
5. If a piece reaches the other end of the board, the piece becomes a King piece.
6. Player wins if the they capture all of the opponent's pieces or if the opponent is not able to make any legal moves. 


Input: each input is a state of an 8x8 board (64 characters). 
- ".": empty space
- "b" or "r": single piece
- "B" or "R": king piece


Output: all of the moves it takes for the red player to win. 


Command
    python3 checkers.py --inputfile inputs/<input file> --outputfile outputs/<output file>
