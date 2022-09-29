from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q


#### SKELETON CODE ####
## The Class that Represents the Puzzle
# how to arrange all different puzzle states
# do i put puzzle states in a queue, list, another class?


class Frontier(object):
    # each node == puzzle state
    # keep a mirror of the queue as a set for checking
    #make it O(1)

    def __init__(self, switch):
        if switch == "queue":
            self.q = Q.Queue()
            self.qset = set()

        if switch == "stack":
            self.stack = []
        pass

    def put(self, node):
        self.qset.add(tuple(node.config))
        return self.q.put(node)

    def empty(self):
        return self.q.empty()

    def get(self):
        node = self.q.get()
        self.qset.remove(tuple(node.config))
        return node

    def search(self, node):
        if tuple(node.config) in self.qset:
            return True
        else:
            return False



class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """

    # frontier - all different configs of puzzlestate. pick data structure: A*-queue
    # constructor
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n * n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n * n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        # self so they do not get discarded on the stack after init goes out of scope
        self.n = n
        self.cost = cost
        self.parent = parent
        self.action = action
        self.config = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3 * i: 3 * (i + 1)])

    def move_up(self):
        """
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        #(self, config, n, parent=None, action="Initial", cost=0):
        new_state = PuzzleState(self.config[:], self.n, self, self.action, self.cost)
        if new_state.blank_index > self.n:
            new_state.config[new_state.blank_index], new_state.config[new_state.blank_index - self.n] = new_state.config[
                                                                                                       new_state.blank_index - self.n], \
                                                                                                   new_state.config[
                                                                                                       new_state.blank_index]
        else:
            return None
        return new_state
        pass

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        new_state = PuzzleState(self.config[:], self.n, self, self.action, self.cost)
        if new_state.blank_index < (len(self.config) - self.n):
            new_state.config[new_state.blank_index], new_state.config[new_state.blank_index + self.n] = new_state.config[
                                                                                                       new_state.blank_index + self.n], \
                                                                                                   new_state.config[
                                                                                                       new_state.blank_index]

        return new_state
        pass

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        new_state = PuzzleState(self.config[:], self.n, self, self.action, self.cost)
        if (new_state.blank_index % self.n) != 0 and new_state.blank_index > 0:
            new_state.config[new_state.blank_index], new_state.config[new_state.blank_index - 1] = new_state.config[
                                                                                                       new_state.blank_index - 1], \
                                                                                                   new_state.config[
                                                                                                       new_state.blank_index]
        return new_state
        pass


    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        # [0, 1, 2
        #  3, 4, 5
        #  6, 7, 8]

        new_state = PuzzleState(self.config[:], self.n, self, self.action, self.cost)
        if (new_state.blank_index % self.n) != 1 and new_state.blank_index < self.n:
            new_state.config[new_state.blank_index], new_state.config[new_state.blank_index + 1] = new_state.config[
                                                                                                       new_state.blank_index + 1], \
                                                                                                   new_state.config[
                                                                                                       new_state.blank_index]
        return new_state
        pass


    def expand(self):
        """ Generate the child nodes of this node """
        # dont touch

        # Node has already been expanded
        if len(self.children) != 0:
            return self.children

        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children


# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput():
    ### Student Code Goes here
    pass


#WORKS
def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    # use explicit queue
    frontier = Frontier("queue")
    frontier.put(initial_state)
    #print(frontier.get().config)
    explored = set()

    while not frontier.empty():
        state = frontier.get()
        #print(state.config)
        explored.add(tuple(state.config))
        #print(tuple(state.config))

        #print(test_goal(state))
        if test_goal(state):
            print(state.config)
            return state

        for neighbor in state.expand():
            #print(neighbor.config)
            if not frontier.search(neighbor) and neighbor not in explored:
                frontier.put(neighbor)

    return -1
    pass


def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    # queue holds puzzle states
    pass


def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    pass


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    pass


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    pass


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    new_list = sorted(puzzle_state.config)
    #print(sorted(puzzle_state.config))
    if (puzzle_state.config == new_list):
        return True
    else:
        return False
    pass


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size = int(math.sqrt(len(begin_state)))
    hard_state = PuzzleState(begin_state, board_size)
    start_time = time.time()

    if search_mode == "bfs":
        bfs_search(hard_state)
    # elif search_mode == "dfs": dfs_search(hard_state)
    # elif search_mode == "ast": A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time - start_time))


if __name__ == '__main__':
    main()
