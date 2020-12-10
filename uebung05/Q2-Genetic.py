#!/usr/bin/env python
# coding: utf-8
# Authors: Lukas Probst, Fabian Ihle


import random
import numpy as np


np.random.seed(2020)  # for the results reproducibility

# ## a)
# Implement a function `initializePopulation()` which takes the number of individuals in a population and the size of the board (number of queens), and returns a randomly generated population. Each value should be in the range $[0, n]$


def initialize_population(population_size, num_queens):
    """

    Args:
        population_size: number of samples to generate
        num_queens:  (board size)

    Returns:
        a list of generated population with each element having
        `num_queens` items
    """
    population = []
    for p in range(0, population_size):
        individual = []
        for i in range(1, num_queens+1):
            q = random.randint(1, num_queens)
            individual.append(q)
        population.append(individual)
    return population


population = initialize_population(4, 5)
print(population)


# ## b)
# Implement a function `findConflicts(individual)` which returns the number of attacking pairs of queens (or #conflicts) for the given input individual (or a population sample / board state).
def find_conflicts(individual):
    """
    Args:
        individual: (board state): a list of size `num_queens` containing each queen position

    Returns:
        Total number of conflicts with the current placement of queens
    """
    conflicts = 0
    for idx, i in enumerate(individual):
        # Same row to the left
        for k in range(idx):
            if individual[k] == i:
                conflicts += 1

        # Check upper diagonal on left side
        for k, j in zip(range(idx-1, -1, -1),
                        range(i-1, 0, -1)):
            if individual[k] == j:
                conflicts += 1

        # Check lower diagonal on left side
        for k, j in zip(range(idx-1, -1, -1),
                        range(i+1, len(individual)+1, 1)):
            if individual[k] == j:
                conflicts += 1

    return conflicts


# testing find_conflicts
find_conflicts([1, 1, 1, 1])
find_conflicts([1, 2, 3, 4])
find_conflicts([1, 1, 1, 1, 1, 1, 1, 1])
find_conflicts([1, 2, 3, 4, 5, 6, 7, 8])
find_conflicts([2, 4, 7, 4, 8, 5, 5, 2])


# ## c)
# Implement a function `randomSelect(population, lamda)` which chooses a parent from the population based on the fitness value. You should use the fitness function $f = exp^{-\lambda x}$ (where $x$
# is number of conflicts and $\lambda$ is a decaying factor) and Roulette-Wheel selection for parents, i.e. probability of selection of a parent is $p_i = f_i / \sum_{j} f_j$ .
#
# To Solve this part, complete following three functions
#  - `fitness_function`
#  - `selection_probability`
#  - `randomSelect`


def fitness_function(individual, lamda):
    """

    Args:
        individual: current state of the board (a list)
        lamda: lambda value.

    Returns:
        fitness of current state of board, i.e. fitness of current individual
    """
    x = find_conflicts(individual)
    return np.exp(-lamda*x)


# Testing of fitness function for 4-queens
fitness_function([1, 1, 1, 1], 0.1)
fitness_function([2, 4, 1, 3], 0.1)


def selection_probability(fitness_population):
    """

    Args:
        fitness_population: a list of fitness values for each individual of population

    Returns:
        probability of each individual being chosen, i.e. p_i = f_i / \sum_{j} f_j
    """
    p = []
    for f_i in fitness_population:
        p_i = f_i / sum(fitness_population)
        p.append(p_i)
    return p


# Calling
selection_probability([0.4, 0.2, 0.5])

# In[65]:


def random_select(population, lamda):
    """
     Randomly chooses the parent from the population using the fitness function
     steps:
     i- compute fitness of each individual using fitness_function
     ii- compute selection probability using selection_probability function
     iii- select invididual according to probability using np.random.choice function

    Args:
        population: given the list of population generated using initialize population
        lamda: for the exponential distribution

    Returns:
        selected individual (state of the board)
    """
    fitness_population = []
    for i in population:
        f_i = fitness_function(i, lamda)
        fitness_population.append(f_i)
    pList = selection_probability(fitness_population)
    rnd_indices = np.random.choice(len(population), p=pList)
    choice = population[rnd_indices]
    return choice


random_select(population, 0.2)


# ## d)
# Implement a function `crossover(parent1, parent2)` which reproduces an offspring by combining parts of each parent at a randomly chosen crossover point.


def cross_over(parent1, parent2):
    """
    generate an offspring by combining parts of each parents
    hint: generate a random index and use it to select slices from both parents
    Args:
        parent1:
        parent2:

    Returns:
        a new individual
    """
    rnd_idx = np.random.choice(len(parent1))
    child = parent1[:rnd_idx] + parent2[rnd_idx:]
    return child


cross_over([1, 2, 3, 4, 2], [2, 3, 1, 2, 5])

# ## e)
# Implement a function `mutate(individual)` which assigns a random position between 1 and $n$ to each queen with the probability of $1/n$


def mutate(individual):
    """
    mutate a given individual sample, i.e. for each queen change its position with probability 1/n
    i.e. generate a random number using random.random and if it is less than 1/n assign
    the queen a random position other-wise leave it. 
    Args:
        individual:

    Returns:
    a mutated child

    """
    for idx, q in enumerate(individual):
        rng = random.random()
        if rng < 1 / (len(individual)):
            pos = random.randint(1, len(individual))
            individual[idx] = pos
    return individual


mutate([1, 3, 2, 5, 4])


# ## f)
# Using the functions in previous parts, implement the complete genetic algorithm (as explained in book and slides). Test your algorithm for varying number of queens and varying decay factor $\lambda$.


def genetic_algorithm(population, lamda):
    """
    Generate the solution using genetic algorithm for input population and lambda
    Your solution should generate at most 1000 generations, if no solution found
    it should return False
    Args:
        population: a list of individuals
        lamda:

    Returns:
        If solution is found it returns the solution and generation count,
        Otherwise: returns false

    """
    maxGenerations = 1000
    generations_count = 0
    while generations_count <= maxGenerations:
        new_population = []
        generations_count += 1
        for i in range(0, len(population)):
            x = random_select(population, lamda)
            y = random_select(population, lamda)
            child = cross_over(x, y)
            child = mutate(child)
        new_population.append(child)
        population = new_population
        # Test for result
        for p in population:
            f_i = fitness_function(p, lamda)
            if f_i == 1:
                return True, p, generations_count
    return False, None, maxGenerations


# First Test of Board of Size 4:
population_size = 16
population = initialize_population(population_size, 4)
genetic_algorithm(population, 0.2)


# Test for Different Queen Sizes
population_size = 16
num_queens_list = [3, 4, 5, 6, 7, 8, 9]
lamda_list = [0.1, 0.2, 0.5, 1, 2]
for num_queens in num_queens_list:
    population = initialize_population(population_size, num_queens)
    for lamda in lamda_list:
        found, solution, generations_count = genetic_algorithm(
            population, lamda)
        if found:
            print('\nNumber of Queens:', num_queens,
                  '\nlamda:', lamda, '\nSolution:', solution)
            print('Number of generations:', generations_count,
                  '\nNumber of individuals', generations_count*population_size)
        else:
            print('\nNumber of Queens:', num_queens,
                  '\nlamda:', lamda, '\nSolution:', solution)
            print('Solution not found in the specified limit of generations')
