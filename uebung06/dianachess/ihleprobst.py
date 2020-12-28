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

    def __init__(self, delay=0, threshold=5):
        self.delay = delay
        self.TIME_THRESHOLD = threshold

    def evaluateGame(self, board, player_wins, enemy_wins):
        # print("Evaluation of board started.")

        SCORE = {"p": 10,
                 "r": 50,
                 "b": 50,
                 "n": 50,
                 "win": 1000,
                 "check": 20}

        color = board.player_turn
        score = 0

        # TODO define better opening

        # print("Check winning")
        t1 = time.time()
        if player_wins:
            return SCORE["win"]
        elif enemy_wins:
            return -SCORE["win"]
        t2 = time.time()
        # print("Checking winning in evaluation: ", t2-t1)

        # print("Is in Check")
        t1 = time.time()
        if board.is_in_check(color):
            score -= SCORE["check"]

        if board.is_in_check(board.get_enemy(color)):
            score += SCORE["check"]

        t2 = time.time()
        # print("Checking Is in Check in evaluation: ", t2-t1)

        # print("Calc score")
        t1 = time.time()
        for coord in board.keys():
            if (board[coord] is not None):
                figure = board[coord]
                fig_color = board[coord].color

                figurescore = SCORE[figure.abbriviation] if figure.abbriviation in SCORE else 0

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

        board = gui.chessboard

        search_depth = 2
        maxscore = -math.inf

        bestmoves = []

        # print("First, valid moves are generated.")
        moves = board.generate_valid_moves(board.player_turn)
        random.shuffle(moves)

        if len(moves) > 0:
            # always have one move to to
            board.update_move(moves[0])

            # print("We will test ", len(moves), " main moves.")
            for m in moves:
                board_copy = deepcopy(board)
                board_copy._do_move(m[0], m[1])

                board_copy.player_turn = board_copy.get_enemy(board_copy.player_turn)

                # print("We test main move: ", m, " and the board looks like this:")
                # board_copy.pprint()
                # print("Main move test start.")
                score = self.min_func(board, board_copy, search_depth, -math.inf, math.inf)
                # print("Main move test end.")

                # TODO check for time left

                if score > maxscore:
                    maxscore = score
                    bestmoves.clear()
                    bestmoves.append(m)
                    board.update_move(m)
                elif score == maxscore:
                    bestmoves.append(m)

            bestmove = bestmoves[random.randint(0, len(bestmoves) - 1)]
            board.update_move(bestmove)
            gui.perform_move()

        # DO NOT REMOVE
        board.engine_is_selecting = False

    def min_func(self, original_board, board, depth, alpha, beta):

        color = board.player_turn

        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins

        if ((depth <= 0) or game_ends or (original_board.get_time_left() < self.TIME_THRESHOLD)):
            return self.evaluateGame(board, player_wins, enemy_wins)

        moves = board.generate_valid_moves(board.player_turn)

        minscore = math.inf

        for m in moves:
            board_copy = deepcopy(board)
            board_copy._do_move(m[0], m[1])

            board_copy.player_turn = board_copy.get_enemy(board_copy.player_turn)
            minscore = min(minscore, self.max_func(original_board, board_copy, depth - 1, alpha, beta))

            if minscore <= alpha:
                return minscore
            beta = min(beta, minscore)

        return minscore

    def max_func(self, original_board, board, depth, alpha, beta):

        color = board.player_turn

        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins

        if ((depth <= 0) or game_ends or (original_board.get_time_left() < self.TIME_THRESHOLD)):
            return self.evaluateGame(board, player_wins, enemy_wins)

        moves = board.generate_valid_moves(board.player_turn)
        random.shuffle(moves)

        maxscore = -math.inf

        for m in moves:
            board_copy = deepcopy(board)
            board_copy._do_move(m[0], m[1])

            board_copy.player_turn = board_copy.get_enemy(board_copy.player_turn)

            maxscore = max(maxscore, self.min_func(original_board, board_copy, depth - 1, alpha, beta))

            if maxscore >= beta:
                return maxscore
            alpha = max(alpha, maxscore)

        return maxscore