# # Assignment 06 - LRTA
# ## Initialization
# Authors: Fabian Ihle, Lukas Probst

import time
import copy


class DefineNode:
    def __init__(self, name, neighbours=[], dist_neighbours=[], parent=None, h=None, H=None):
        self.neighbours = neighbours  # A list containing all the neighbor city objects
        self.dist_neighbours = dist_neighbours  # The distance to each neighbor of the city (same order as self.neighbours)
        self.parent = parent  # The parent of this city (For keeping track of the path)
        self.name = name  # The name of this city
        self.h = h  # The heuristic h(n)
        self.H = H  # H(n) the H table cost of this node
        assert len(self.dist_neighbours) == len(self.neighbours)

    def g(self, node):
        idx = self.neighbours.index(node)
        dist = self.dist_neighbours[idx]
        return dist


def initialize_all_nodes():
    node = {}
    node['A1'] = DefineNode(name='A1', h=6, H=6)
    node['A2'] = DefineNode(name='A2', h=6, H=6)
    node['A3'] = DefineNode(name='A3', h=1, H=1)
    node['A4'] = DefineNode(name='A4', h=3, H=3)
    node['A5'] = DefineNode(name='A5', h=3, H=3)
    node['B1'] = DefineNode(name='B1', h=5, H=5)
    node['B2'] = DefineNode(name='B2', h=1, H=1)
    node['B3'] = DefineNode(name='B3', h=1, H=1)
    node['B4'] = DefineNode(name='B4', h=4, H=4)
    node['B5'] = DefineNode(name='B5', h=2, H=2)
    node['C1'] = DefineNode(name='C1', h=6, H=6)
    node['C2'] = DefineNode(name='C2', h=5, H=5)
    node['C3'] = DefineNode(name='C3', h=4, H=4)
    node['C4'] = DefineNode(name='C4', h=3, H=3)
    node['C5'] = DefineNode(name='C5', h=2, H=2)
    node['D1'] = DefineNode(name='D1', h=5, H=5)
    node['D2'] = DefineNode(name='D2', h=4, H=4)
    node['D3'] = DefineNode(name='D3', h=3, H=3)
    node['D4'] = DefineNode(name='D4', h=2, H=2)
    node['D5'] = DefineNode(name='D5', h=1, H=1)
    node['E1'] = DefineNode(name='E1', h=4, H=4)
    node['E2'] = DefineNode(name='E2', h=3, H=3)
    node['E3'] = DefineNode(name='E3', h=2, H=2)
    node['E4'] = DefineNode(name='E4', h=1, H=1)
    node['E5'] = DefineNode(name='E5', h=0, H=0)
    node['A1'].neighbours = [node['A2'], node['B1']]
    node['A1'].dist_neighbours = [1, 1]
    node['A2'].neighbours = [node['A1'], node['B2'], node['A3']]
    node['A2'].dist_neighbours = [1, 1, 1]
    node['A3'].neighbours = [node['A2'], node['B3'], node['A4']]
    node['A3'].dist_neighbours = [1, 1, 1]
    node['A4'].neighbours = [node['A3'], node['B4'], node['A5']]
    node['A4'].dist_neighbours = [1, 1, 1]
    node['A5'].neighbours = [node['A4'], node['B5']]
    node['A5'].dist_neighbours = [1, 1]
    node['B1'].neighbours = [node['A1'], node['B2'], node['C1']]
    node['B1'].dist_neighbours = [1, 1, 1]
    node['B2'].neighbours = [node['B1'], node['A2'], node['B3'], node['C2']]
    node['B2'].dist_neighbours = [1, 1, 1, 1]
    node['B3'].neighbours = [node['B2'], node['A3'], node['B4'], node['C3']]
    node['B3'].dist_neighbours = [1, 1, 1, 1]
    node['B4'].neighbours = [node['B3'], node['A4'], node['B5'], node['C4']]
    node['B4'].dist_neighbours = [1, 1, 1, 1]
    node['B5'].neighbours = [node['B4'], node['A5'], node['C5']]
    node['B5'].dist_neighbours = [1, 1, 1]
    node['C1'].neighbours = [node['B1'], node['C2'], node['D1']]
    node['C1'].dist_neighbours = [1, 1, 1]
    node['C2'].neighbours = [node['C1'], node['B2'], node['C3'], node['D2']]
    node['C2'].dist_neighbours = [1, 1, 1, 1]
    node['C3'].neighbours = [node['C2'], node['B3'], node['C4'], node['D3']]
    node['C3'].dist_neighbours = [1, 1, 1, 1]
    node['C4'].neighbours = [node['C3'], node['B4'], node['C5'], node['D4']]
    node['C4'].dist_neighbours = [1, 1, 1, 1]
    node['C5'].neighbours = [node['C4'], node['B5'], node['D5']]
    node['C5'].dist_neighbours = [1, 1, 1]
    node['D1'].neighbours = [node['C1'], node['D2'], node['E1']]
    node['D1'].dist_neighbours = [1, 1, 1]
    node['D2'].neighbours = [node['D1'], node['C2'], node['D3'], node['E2']]
    node['D2'].dist_neighbours = [1, 1, 1, 1]
    node['D3'].neighbours = [node['D2'], node['C3'], node['D4'], node['E3']]
    node['D3'].dist_neighbours = [1, 1, 1, 1]
    node['D4'].neighbours = [node['D3'], node['C4'], node['D5'], node['E4']]
    node['D4'].dist_neighbours = [1, 1, 1, 1]
    node['D5'].neighbours = [node['D4'], node['C5'], node['E5']]
    node['D5'].dist_neighbours = [1, 1, 1]
    node['E1'].neighbours = [node['D1'], node['E2']]
    node['E1'].dist_neighbours = [1, 1]
    node['E2'].neighbours = [node['E1'], node['D2'], node['E3']]
    node['E2'].dist_neighbours = [1, 1, 1]
    node['E3'].neighbours = [node['E2'], node['D3'], node['E4']]
    node['E3'].dist_neighbours = [1, 1, 1]
    node['E4'].neighbours = [node['E3'], node['D4'], node['E5']]
    node['E4'].dist_neighbours = [1, 1, 1]
    node['E5'].neighbours = [node['E4'], node['D5']]
    node['E5'].dist_neighbours = [1, 1]
    return node


nodes = initialize_all_nodes()


def check_consistency(node):
    inconsistency = []
    h_n = node.h
    for idx, neighbor in enumerate(node.neighbours):
        c_n = node.dist_neighbours[idx]
        h_n_prime = neighbor.h
        if h_n > c_n + h_n_prime:
            inconsistency.append(neighbor)
    return inconsistency

for node in nodes.values():
    inconsistency = check_consistency(node)
    if inconsistency:
        print('There is an incosistency from the node:', node.name, 'to the neighbours:',
              [i.name for i in inconsistency])


def lrta_cost(previous_state, state):
    if not state:
        return previous_state.h
    else:
        return previous_state.g(state) + state.H

def lrta_agent(state=None, goal=None, previous_state=None):
    if state == goal:
        return True
    
    if previous_state:
        min_cost = float('inf')
        for idx, n in enumerate(previous_state.neighbours):
            if n.H + previous_state.dist_neighbours[idx] < min_cost:
                min_cost = lrta_cost(previous_state, n)
                a = n
        previous_state.H = min_cost
    # s' = state
    # actions(s') = state.neighbours 
    min_cost = float('inf')
    a = None
    for idx, n in enumerate(state.neighbours):
        if n.H + state.dist_neighbours[idx] < min_cost:
            min_cost = lrta_cost(state, n)
            a = n
    return a

def lrta_graphsearch(start_node, goal_node):
    ctr = 0
    path = []
    previous_state = None
    current_state = start_node
    while (True):
        path.append(current_state.name)
        next_node = lrta_agent(current_state, goal_node, previous_state)
        if next_node is True:
            return path, ctr
        ctr += 1
        previous_state = current_state
        current_state = next_node

nodes = initialize_all_nodes()
start_node = nodes['A1']
goal_node = nodes['E5']
path, steps = lrta_graphsearch(start_node, goal_node)
print('\nThe path from', start_node.name, 'to', goal_node.name, 'is:\n', path)
print('Total number of steps taken:', steps)

# d) Look at the steps made by the agent during the algorithm. Do they form an optimal path? If not, explain why.
# The path is not optimal. The optimal path would be 'A1-B1-B2-B3-B4-B5-C5-D5-E5' as we found out with the A* Algorithm in assignment07. 
# This happens due to the fact, that lrta* does not take the cumulated path cost into consideration and only looks at the next possible actions from its current state on.
