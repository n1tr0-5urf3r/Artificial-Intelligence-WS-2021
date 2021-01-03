import random
import math
from copy import deepcopy, copy
import time

"""   

- Generally, coordinates/positions are 'A3', 'B3',...
- board[coord] returns the piece at coord
- Try to always have a move to do (just take a random one at the beginning with update_move)

- IMPORTANT: ALWAYS USE COPIES OF THE GAME BOARD VIA DEEPCOPY() IF YOU WANT TO MANIPULATE THE BOARD,
             THIS IS SHOWN IN MR. NOVICE
             
- You can get the board from the gui via gui.chessboard

- DO NOT CHANGE OR ADD THE PARAMS OF THE GENERATE FUNCTION OR ITS NAME!



        -------------------- Useful methods  ---------------------------------------

-------------------- Board methods:

# converts coordinates in the form '(x,y)' (tuple) to 'A4' (string)
def letter_notation(self,coord)

# converts coordinates in the from 'A4' (string) to '(x,y)' (tuple)
def number_notation(self, coord):

# looks through the whole board to check for the king, outputs pos of king like this 'A5' (string)
def get_king_position(self, color):

# get the enemy, color is "white" or "black"
def get_enemy(self, color):

# manually check from the king if other pieces can attack it
# output is boolean
def is_in_check(self, color, debug=False):

def is_in_checkmate(self, color):

# returns a list of all valid moves in the format [('A1','A4'),..], left: from, right: to
def generate_valid_moves(self, color):

# returns a list of all possible moves in the format [('A1','A4'),..], left: from, right: to
def all_possible_moves(self, color):

# checks for limit turn count and checkmate, returns boolean (won/not won)
def check_winning_condition(self,color,end_game=False,print_result=False,gui = None):

# filter out invalid moves for moves of a color, returns list of valid moves
def is_in_check_after_move_filter(self,moves):

# returns boolean (still in check after p1->p2)
def is_in_check_after_move(self, p1, p2):

# time left for choosing move (in seconds)
def get_time_left(self):

# executes move without checking
# !   You have to manually change to the next player 
# with board.player_turn=board.get_enemy(board.player_turn) after this !
def _do_move(self, p1, p2):

# Pretty print board
def pprint(self):

# update the move that will be done (has to be a tuple (from, to))
def update_move(self,move):


---------------GUI methods

# performs the selected move (should ideally be at the end of generate function)
def perform_move(self):


--------------- Piece methods


# returns the landing positions, if the piece were at pos
# ! only landing positions !
def possble_moves(pos)

"""


# After perform_move(), make sure that the agent does not continue searching for moves!

class MrCustom:

    def __init__(self, delay=0, threshold=2):
        self.delay = delay
        self.TIME_THRESHOLD = threshold
        self.color = None
        self.firstRun = True

    def evaluateGame(self, board, player_wins, enemy_wins):
        # print("Evaluation of board started.")

        SCORE_WIN = 1000

        SCORE_PAWN = 10
        SCORE_ROOK = 50
        SCORE_BISHOP = 30
        SCORE_KNIGHT = 30

        SCORE_CHECK = 5

        field_value = [[1, 1, 1, 1, 1, 1],
                       [1, 1, 1.1, 1.1, 1, 1],
                       [1, 1.2, 1.25, 1.25, 1.2, 1],
                       [1, 1.2, 1.25, 1.25, 1.2, 1],
                       [1, 1, 1.1, 1.1, 1, 1],
                       [1, 1, 1, 1, 1, 1]]

        # As we can not enter color as parameter to __init__ function, as MrNovice does, we set it here.
        # Somehow we always have to set the opposite color of player_turn
        color = self.color
        score = 0

        # print("Check winning")
        t1 = time.time()
        if player_wins:
            return SCORE_WIN
        elif enemy_wins:
            return -SCORE_WIN
        t2 = time.time()
        # print("Checking winning in evaluation: ", t2-t1)

        # print("Is in Check")
        t1 = time.time()
        if board.is_in_check(color):
            score -= SCORE_CHECK

        if board.is_in_check(board.get_enemy(color)):
            score += SCORE_CHECK

        t2 = time.time()
        # print("Checking Is in Check in evaluation: ", t2-t1)

        # print("Calc score")
        t1 = time.time()
        for coord in board.keys():
            if (board[coord] is not None):
                figure = board[coord]
                fig_color = board[coord].color

                figurescore = 0
                fig_name = (figure.abbriviation).lower()
                if fig_name == 'p':
                    figurescore = SCORE_PAWN
                elif fig_name=='r':
                    figurescore = SCORE_ROOK
                elif fig_name=='b':
                    figurescore = SCORE_BISHOP
                elif fig_name=='n':
                    figurescore = SCORE_KNIGHT
                row, col = board.number_notation(coord)

                # figurescore = figurescore * field_value[row][col]

                if fig_color == color:
                    score += figurescore
                else:
                    score -= figurescore

        t2 = time.time()
        # print("Checking Score Calc in evaluation: ", t2-t1)

        # print("Evaluation of board ended.")
        return score

    def generate_next_move(self, gui):

        # print("Next move will now be generated:")
        # This is needed to globally set player color as we dont get that via parameter
        if self.firstRun:
            self.color = gui.chessboard.player_turn
            self.firstRun = False

        search_depth = 3

        bestmove = self.alpha_beta_search(gui, search_depth)
        gui.chessboard.update_move(bestmove)
        gui.perform_move()
        gui.chessboard.engine_is_selecting = False

    def alpha_beta_search(self, gui, search_depth):
        board = deepcopy(gui.chessboard)

        v, move = self.max_value(gui.chessboard, board, search_depth, -math.inf, math.inf, None)
        return move

    def max_value(self, original_board, board, depth, alpha, beta, move_that_lead_here):
        color = self.color
        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins

        if ((depth <= 0) or game_ends or (original_board.get_time_left() < self.TIME_THRESHOLD)):
            return self.evaluateGame(board, player_wins, enemy_wins), move_that_lead_here

        moves = board.generate_valid_moves(board.player_turn)

        v = -math.inf
        best_move = None
        sorted_moves = self.preorder_moves(moves, board, True)

        for m in sorted_moves:
            # COPY
            _from_fig = board[m[0]]
            _to_fig = board[m[1]]
            player, move_number = board.get_current_state()

            # PERFORM
            board._do_move(m[0], m[1])
            board.switch_players()

            new_v, new_move = self.min_value(original_board, board, depth - 1, alpha, beta, m)
            new_v = 0.99 * new_v
            if new_v > v:
                v = new_v
                best_move = m

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            if v >= beta:
                return v, best_move
            alpha = max(alpha, v)

        return v, best_move

    def min_value(self, original_board, board, depth, alpha, beta, move_that_lead_here):
        color = self.color
        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins

        if ((depth <= 0) or game_ends or (original_board.get_time_left() < self.TIME_THRESHOLD)):
            return self.evaluateGame(board, player_wins, enemy_wins), move_that_lead_here

        moves = board.generate_valid_moves(board.player_turn)

        v = math.inf
        best_move = None
        sorted_moves = self.preorder_moves(moves, board, True)

        for m in sorted_moves:
            # COPY
            _from_fig = board[m[0]]
            _to_fig = board[m[1]]
            player, move_number = board.get_current_state()

            # PERFORM
            board._do_move(m[0], m[1])
            board.switch_players()

            new_v, new_move = self.max_value(original_board, board, depth - 1, alpha, beta, m)
            new_v = 0.99 * new_v

            if new_v < v:
                v = new_v
                best_move = m

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            if v <= alpha:
                return v, best_move
            beta = min(beta, v)

        return v, best_move


    def preorder_moves(self, moves, board, min_or_max):
        """
        Returns a preordered list of moves
        :param moves: List of moves
        :param board: The current state
        :param min_or_max: True if List should be ordered with least value first
        """

        order = ["k", "r", "b", "n", "p", None]
        debugStr = "Defend " if min_or_max else "Attack "
        if min_or_max:
            order.reverse()
        m_values = []
        for m in moves:
            # Kill the highest valued target: king, rook, bishop, knight and pawn
            source = board[m[0]].abbriviation.lower()
            target = board[m[1]].abbriviation.lower() if board[m[1]] else None
            # todo remove last element from tuple
            m_values.append((m[0], m[1], order.index(target),
                             str(order[order.index(source)]) + " " + debugStr + str(order[order.index(target)])))

        sorted_moves = sorted(m_values, key=lambda tup: tup[2])
        return sorted_moves
