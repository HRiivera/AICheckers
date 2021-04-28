from Game import Game
import copy
from collections import namedtuple

GameState = namedtuple('GameState', 'to_move, utility, board, moves')


class CheckersGame(Game):

    def __init__(self):
        # Initial board state, E means empty, R means red piece, B means black piece
        board = [["E", "R", "E", "R", "E", "R", "E", "R"],
                 ["R", "E", "R", "E", "R", "E", "R", "E"],
                 ["E", "R", "E", "R", "E", "R", "E", "R"],
                 ["E", "E", "E", "E", "E", "E", "E", "E"],
                 ["E", "E", "E", "E", "E", "E", "E", "E"],
                 ["B", "E", "B", "E", "B", "E", "B", "E"],
                 ["E", "B", "E", "B", "E", "B", "E", "B"],
                 ["B", "E", "B", "E", "B", "E", "B", "E"]]

        self.initial = GameState(to_move="B", utility=0, board=board, moves=self.get_all_moves(board, "B"))

    def actions(self, state):
        player = state.to_move
        moves = state.moves

        if len(moves) == 1:  # Not too sure about this
            return moves

        legal_moves = []
        for move in moves:
            board = copy.deepcopy(state.board)
            if self.is_legal_move(board, move[0], move[1], player):
                legal_moves.append(move)
        return legal_moves

    def result(self, state, move):
        board = copy.deepcopy(state.board)
        player = state.to_move
        self.move_checker(board=board, start=move[0], dest=move[1])
        player = ("R" if player == "B" else "B")
        return GameState(to_move=player, utility=self.compute_utility(state.board, move, player),
                         board=board, moves=self.get_all_moves(board, player))

    def utility(self, state, player):
        """Returns 1 if Red wins, -1 if Black wins or 0 if otherwise"""
        return state.utility if player == 'R' else -state.utility

    def terminal_test(self, state):
        """A state is terminal if one player wins."""
        return state.utility != 0

    def compute_utility(self, board, move, player):
        """Returns 1 if Red wins move, -1 if Black 
        wins move or 0 if otherwise"""
        r_Alive = 0
        b_Alive = 0
        for line in range(8):
            for col in range(8):
                if board[line][col] == "R":
                    r_Alive += 1
                elif board[line][col] == "B":
                    b_Alive += 1
        if r_Alive > b_Alive:
            if b_Alive == 0:
                return 1
            else: return 0
        elif r_Alive == 0:
            return -1

    def get_all_moves(self, board, player):
        """Returns all possible moves"""
        result = []
        for startx in range(8):
            for starty in range(8):
                for destx in range(8):
                    for desty in range(8):
                        if self.is_legal_move(board, [startx, starty], [destx, desty], player):
                            result.append([[startx, starty], [destx, desty]])
        return result
                            

    def is_legal_move(self, board, start, dest, player):

        start_x, start_y = start[0], start[1]
        dest_x, dest_y = dest[0], dest[1]

        piece = board[start_y][start_x]
        dist = abs(start_x - dest_x)

        # Checks if it's the player's piece
        if piece[0] != player[0]:
            return False
        # Checks if destination isn't empty
        if board[dest_y][dest_x] != "E":
            return False
        # Checks if destination is within bounds
        if dest_x < 0 or dest_x > 7 or dest_y < 0 or dest_y > 7:
            return False

        # All the conditions to see if a move is possible. Probably a way to make it shorter but oh well
        if piece == "B" and dist == 1:
            return dest_y == start_y - 1 and dest_x in [start_x - 1, start_x + 1]
        elif piece == "B" and dist == 2:
            if dest_y == start_y - 2 and dest_x == start_x - 2 and board[start_y - 1][start_x - 1] in ["R", "RK"]:
                return True
            elif dest_y == start_y - 2 and dest_x == start_x + 2 and board[start_y - 1][start_x + 1] in ["R", "RK"]:
                return True
            else:
                return False
        elif piece == "BK" and dist == 1:
            return dest_y in [start_y - 1, start_y + 1] and dest_x in [start_x - 1, start_x + 1]
        elif piece == "BK" and dist == 2:
            if dest_y == start_y - 2 and dest_x == start_x - 2 and board[start_y - 1][start_x - 1] in ["R", "RK"] or \
                    dest_y == start_y + 2 and dest_x == start_x - 2 and board[start_y + 1][start_x - 1] in ["R", "RK"]:
                return True
            elif dest_y == start_y - 2 and dest_x == start_x + 2 and board[start_y - 1][start_x + 1] in ["R", "RK"] or \
                    dest_y == start_y + 2 and dest_x == start_x + 2 and board[start_y + 1][start_x + 1] in ["R", "RK"]:
                return True
            else:
                return False

        elif piece == "R" and dist == 1:
            return dest_y == start_y + 1 and dest_x in [start_x - 1, start_x + 1]
        elif piece == "R" and dist == 2:
            if dest_y == start_y + 2 and dest_x == start_x - 2 and board[start_y + 1][start_x - 1] in ["B", "BK"]:
                return True
            elif dest_y == start_y + 2 and dest_x == start_x + 2 and board[start_y + 1][start_x + 1] in ["B", "BK"]:
                return True
            else:
                return False
        elif piece == "RK" and dist == 1:
            return dest_y in [start_y - 1, start_y + 1] and dest_x in [start_x - 1, start_x + 1]
        elif piece == "RK" and dist == 2:
            if dest_y == start_y - 2 and dest_x == start_x - 2 and board[start_y - 1][start_x - 1] in ["B", "BK"] or \
                    dest_y == start_y + 2 and dest_x == start_x - 2 and board[start_y + 1][start_x - 1] in ["B", "BK"]:
                return True
            elif dest_y == start_y - 2 and dest_x == start_x + 2 and board[start_y - 1][start_x + 1] in ["B", "BK"] or \
                    dest_y == start_y + 2 and dest_x == start_x + 2 and board[start_y + 1][start_x + 1] in ["B", "BK"]:
                return True
            else:
                return False

        return False

    def move_checker(self, board, start, dest):

        start_x, start_y = start[0], start[1]
        dest_x, dest_y = dest[0], dest[1]

        piece = board[start_y][start_x]
        dist = abs(start_x - dest_x)

        board[start_y][start_x] = "E"

        if dist == 1:
            board[dest_y][dest_x] = piece
        elif dist == 2:
            board[dest_y][dest_x] = piece
            board[(start_y+dest_y)//2][(start_x+dest_x)//2] = "E"
        if piece == "B" and dest_y == 0:
            board[dest_y][dest_x] = "BK"
        elif piece == "R" and dest_y == 7:
            board[dest_y][dest_x] = "RK"

    def display(self, state):
        for i in range(len(state.board)):
            print(state.board[i])