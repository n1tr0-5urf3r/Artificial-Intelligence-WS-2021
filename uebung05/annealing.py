# Authors: Lukas Probst, Fabian Ihle

import copy
import numpy as np

# np.random.seed(0)

""" E1: number of inversions """


def number_inversions(board):
    out = 0
    for i in range(len(board)):
        for j in range(len(board[0])):
            for k in range(i, len(board)):
                if k == i:
                    for m in range(j, len(board[0])):
                        if board[k][m] > 0 and board[k][m] < board[i][j]:
                            out += 1
                else:
                    for m in range(len(board[0])):
                        if board[k][m] > 0 and board[k][m] < board[i][j]:
                            out += 1
    return out


""" E2: number of misplaced tiles """


def number_misplaced(board):
    out = 0
    for k in range(len(board)):
        for j in range(len(board[0])):
            if board[k][j] > 0 and not board[k][j] == goal[k][j]:
                out += 1
    return out


""" E3: Manhattan distance """


def manhattan_distance(board):
    out = 0
    dimx = len(board[0])
    for k in range(len(board)):
        for j in range(len(board[0])):
            if not board[k][j] == 0:
                distance_x = np.abs((board[k][j] % dimx) - j)
                distance_y = np.abs(np.floor(board[k][j] / 3) - k)
                out += distance_x + distance_y
    return out


def energy(board, which_one):
    if which_one == 1:
        return number_inversions(board)
    elif which_one == 2:
        return number_misplaced(board)
    elif which_one == 3:
        return manhattan_distance(board)

# Assignment05: Q3(a)


def successor(board):
    """This function selects the successor state. For this, think of 
    copy.deepcopy(board), so you don't change the board which is given 
    as an argument."""

    def find_empty_tile(board):
        for idx, row in enumerate(board):
            if 0 in row:
                return idx

    # Select a random successor state. All actions are hardcoded
    c_board = copy.deepcopy(board)
    row_of_zero = find_empty_tile(c_board)
    col_of_zero = c_board[row_of_zero].index(0)
    if row_of_zero == 0:
        if col_of_zero == 0:
            possible_actions = 2
            rng = np.random.random_sample()
            if rng < 0.5:
                c_board[0][0] = c_board[0][1]
                c_board[0][1] = 0
            else:
                c_board[0][0] = c_board[1][0]
                c_board[1][0] = 0
        elif col_of_zero == 1:
            possible_actions = 3
            rng = np.random.random_sample()
            if rng < 1/possible_actions:
                c_board[0][1] = c_board[0][0]
                c_board[0][0] = 0
            elif rng < 2/possible_actions:
                c_board[0][1] = c_board[0][2]
                c_board[0][2] = 0
            else:
                c_board[0][1] = c_board[1][1]
                c_board[1][1] = 0
        else:
            possible_actions = 2
            rng = np.random.random_sample()
            if rng < 0.5:
                c_board[0][2] = c_board[0][1]
                c_board[0][1] = 0
            else:
                c_board[0][2] = c_board[1][2]
                c_board[1][2] = 0

    elif row_of_zero == 1:
        if col_of_zero == 0:
            possible_actions = 3
            rng = np.random.random_sample()
            if rng < 1/possible_actions:
                c_board[1][0] = c_board[0][0]
                c_board[0][0] = 0
            elif rng < 2/possible_actions:
                c_board[1][0] = c_board[2][0]
                c_board[2][0] = 0
            else:
                c_board[1][0] = c_board[1][1]
                c_board[1][1] = 0
        elif col_of_zero == 1:
            possible_actions = 4
            rng = np.random.random_sample()
            if rng < 1/possible_actions:
                c_board[1][1] = c_board[0][1]
                c_board[0][1] = 0
            elif rng < 2/possible_actions:
                c_board[1][1] = c_board[1][0]
                c_board[1][0] = 0
            elif rng < 3/possible_actions:
                c_board[1][1] = c_board[1][2]
                c_board[1][2] = 0
            else:
                c_board[1][1] = c_board[2][1]
                c_board[2][1] = 0
        else:
            possible_actions = 3
            rng = np.random.random_sample()
            if rng < 1/possible_actions:
                c_board[1][2] = c_board[0][2]
                c_board[0][2] = 0
            elif rng < 2/possible_actions:
                c_board[1][2] = c_board[2][2]
                c_board[2][2] = 0
            else:
                c_board[1][2] = c_board[1][1]
                c_board[1][1] = 0
    else:
        if col_of_zero == 0:
            possible_actions = 2
            rng = np.random.random_sample()
            if rng < 0.5:
                c_board[2][0] = c_board[1][0]
                c_board[1][0] = 0
            else:
                c_board[2][0] = c_board[2][1]
                c_board[2][1] = 0
        elif col_of_zero == 1:
            possible_actions = 3
            rng = np.random.random_sample()
            if rng < 1/possible_actions:
                c_board[2][1] = c_board[1][1]
                c_board[1][1] = 0
            elif rng < 2/possible_actions:
                c_board[2][1] = c_board[2][0]
                c_board[2][0] = 0
            else:
                c_board[2][1] = c_board[2][2]
                c_board[2][2] = 0
        else:
            possible_actions = 2
            rng = np.random.random_sample()
            if rng < 0.5:
                c_board[2][2] = c_board[1][2]
                c_board[1][2] = 0
            else:
                c_board[2][2] = c_board[2][1]
                c_board[2][1] = 0
    return c_board


def scheduler(step):
    """Scheduler should be a function that takes an integer step parameter."""
    t = 1/(np.log(np.log(np.log(step+1)+1)+1))
    return t


def simulated_annealing(schedule, board):
    """Implements the simulated annealing algorithm with the given schedule."""
    step = 1
    current = copy.deepcopy(board)
    while True:
        if current == [[0, 1, 2], [3, 4, 5], [6, 7, 8]]:
            return current, step
        temperature = scheduler(step)
        nxt = successor(current)
        delta_e = schedule(nxt) - schedule(current)
        if delta_e < 0:
            current = nxt
        else:
            # Need an extra minus sign to decrease the value for minimization problem
            prob = np.exp(-delta_e/temperature)
            rng = np.random.random_sample()
            if rng <= prob:
                current = nxt
        step += 1
    return current, step

############## Assignment05: Q3(b)


def compare_energies():
    """Execute the simulated annealing multiple times with the given schedule
       and average the results."""
    test1 = [[8, 1, 7], [5, 4, 2], [0, 6, 3]]

    # Removed the np.random.seed(0) as this is always generating the same pseudorandom numbers
    s = 0
    for i in range(20):
        g, s_i = simulated_annealing(number_inversions, test1)
        s += s_i
    e1_avg = s/20
    s = 0
    for i in range(20):
        g, s_i = simulated_annealing(number_misplaced, test1)
        s += s_i
    e2_avg = s/20
    s = 0
    for i in range(20):
        g, s_i = simulated_annealing(manhattan_distance, test1)
        s += s_i
    e3_avg = s/20
    return e1_avg, e2_avg, e3_avg


    #(57972.9, 183167.6, 72492.4)
""" 8-puzzle problem """
goal = [[0, 1, 2], [3, 4, 5], [6, 7, 8]]
# Solvable
print(simulated_annealing(number_inversions,
                          [[8, 1, 7], [5, 4, 2], [0, 6, 3]]))
print(simulated_annealing(number_inversions,
                          [[0, 1, 2], [3, 5, 4], [7, 6, 8]]))

print(compare_energies())

# Not Solvable
print(simulated_annealing(number_inversions,
                          [[0, 2, 1], [4, 3, 5], [7, 6, 8]]))
