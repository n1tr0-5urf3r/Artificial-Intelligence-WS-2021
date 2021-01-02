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
        self.color = None
        self.firstRun = True

    def evaluateGame(self, board, player_wins, enemy_wins):
        # print("Evaluation of board started.")

        SCORE = {"p": 1,
                 "r": 5.5,
                 "b": 3.3,
                 "n": 3.2,
                 "win": 1000,
                 "check": 10}

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

        # TODO define default action when no time left

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

                figurescore = SCORE[(figure.abbriviation).lower()] if (figure.abbriviation).lower() in SCORE else 0
                row, col = board.number_notation(coord)

                figurescore = figurescore * field_value[row][col]

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

        board = deepcopy(gui.chessboard)

        search_depth = 2
        maxscore = -math.inf

        bestmoves = []

        # print("First, valid moves are generated.")
        moves = board.generate_valid_moves(board.player_turn)
        sorted_moves = self.preorder_moves(moves, board, False)
        # print(sorted_moves)

        if len(moves) > 0:
            # always have one move to to
            gui.chessboard.update_move(sorted_moves[0])

            # print("We will test ", len(moves), " main moves.")
            for m in sorted_moves:

                # COPY
                _from_fig = board[m[0]]
                _to_fig = board[m[1]]
                player, move_number = board.get_current_state()

                # PERFORM
                #print("{} doing move {} {}".format(self.color, m[0], m[1]))
                board._do_move(m[0], m[1])
                board.switch_players()

                # print("We test main move: ", m, " and the board looks like this:")
                # board_copy.pprint()
                # print("Main move test start.")

                # board.board_states.append(board.to_string())

                score = self.min_func(gui.chessboard, board, search_depth, -math.inf, math.inf)

                """
                print("\n\n----------------------\n\n")
                print("Main move " + "(" +m[0] + ", " + m[1] + ")" + " with score " + str(score) + " test end.\n\n")
                for state in board.board_states:
                    print(state)
                print("\n\n----------------------\n\n")
                board.board_states.pop()
                """

                # RESET
                board[m[0]] = _from_fig
                board[m[1]] = _to_fig
                board.player_turn = player
                board.fullmove_number = move_number

                if score > maxscore:
                    maxscore = score
                    bestmoves.clear()
                    bestmoves.append(m)
                    gui.chessboard.update_move(m)
                elif score == maxscore:
                    bestmoves.append(m)

            bestmove = bestmoves[random.randint(0, len(bestmoves) - 1)]
            gui.chessboard.update_move(bestmove)
            gui.perform_move()
        gui.chessboard.engine_is_selecting = False

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

    def min_func(self, original_board, board, depth, alpha, beta):

        color = self.color
        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins

        if ((depth <= 0) or game_ends or (original_board.get_time_left() < self.TIME_THRESHOLD)):
            return self.evaluateGame(board, player_wins, enemy_wins)

        moves = board.generate_valid_moves(board.player_turn)

        minscore = math.inf

        sorted_moves = self.preorder_moves(moves, board, True)
        # print(sorted_moves)
        for m in sorted_moves:
            # COPY
            _from_fig = board[m[0]]
            _to_fig = board[m[1]]
            player, move_number = board.get_current_state()
           # print("{} doing move {} {} MIN".format(self.color, m[0], m[1]))

            # PERFORM
            board._do_move(m[0], m[1])
            board.switch_players()

            # board.board_states.append(board.to_string())

            minscore = min(minscore, self.max_func(original_board, board, depth - 1, alpha, beta))

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            if minscore <= alpha:
                return minscore
            beta = min(beta, minscore)

        return minscore

    def max_func(self, original_board, board, depth, alpha, beta):

        color = self.color

        player_wins = board.check_winning_condition(color)
        enemy_wins = board.check_winning_condition(board.get_enemy(color))
        game_ends = player_wins or enemy_wins

        if ((depth <= 0) or game_ends or (original_board.get_time_left() < self.TIME_THRESHOLD)):
            return self.evaluateGame(board, player_wins, enemy_wins)

        moves = board.generate_valid_moves(board.player_turn)

        maxscore = -math.inf

        sorted_moves = self.preorder_moves(moves, board, False)
        # print(sorted_moves)

        for m in sorted_moves:
            # COPY
            _from_fig = board[m[0]]
            _to_fig = board[m[1]]
            player, move_number = board.get_current_state()

           # print("{} doing move {} {} MAX".format(self.color, m[0], m[1]))

            # PERFORM
            board._do_move(m[0], m[1])
            board.switch_players()

            # board.board_states.append(board.to_string())

            maxscore = max(maxscore, self.min_func(original_board, board, depth - 1, alpha, beta))

            """
            print("\n\n----------------------\n\n")
            print("Score for this move sequence is: ", score)
            for state in board.board_states:
                print(state)
            print("\n\n----------------------\n\n")
            board.board_states.pop()
            """

            # RESET
            board[m[0]] = _from_fig
            board[m[1]] = _to_fig
            board.player_turn = player
            board.fullmove_number = move_number

            if maxscore >= beta:
                return maxscore
            alpha = max(alpha, maxscore)

        return maxscore
