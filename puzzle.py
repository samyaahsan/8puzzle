from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import heapq


#### SKELETON CODE ####
## The Class that Represents the Puzzle
# how to arrange all different puzzle states
# do i put puzzle states in a queue, list, another class?


class Frontier(object):
    # each node == puzzle state
    # keep a mirror of the queue as a set for checking
    # make it O(1)

    def __init__(self, switch):
        if switch == "queue":
            self.q = Q.Queue()
            self.qset = set()
        elif switch == "stack":
            self.stack = []
            self.sset = set()
        elif switch == "heap":
            self.heap = []
            self.hset = set()
        pass

    #queue methods
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

    #stack methods
    def stack_empty(self):
        return len(self.stack) == 0

    def push(self, node):
        self.sset.add(tuple(node.config))
        return self.stack.append(node)

    def pop(self):
        return self.stack.pop()

    def stack_search(self, node):
        if tuple(node.config) in self.sset:
            return True
        else:
            return False

    def heap_push(self, priority, node):
        #add the new thing to the queue with two different priorities,
        #heap -- list of tuples
        self.hset.add(tuple(node.config))
        heapq.heappush(self.heap, (priority, node))


    def heap_search(self, node):
        if tuple(node.config) in self.hset:
            return True
        else:
            return False

    def delete_min(self):
        deleted = heapq.heappop(self.heap)
        #print(deleted)
        #returns a tuple {node, cost}
        remove = list(deleted)[1]
        #print(remove.config)
        self.hset.remove(tuple(remove.config))
        return remove

    #won't work
    def remove_duplicate(self, node):
        for item in self.heap:
            if item[1].config == node.config:
                self.heap.remove(item)
                self.hset.remove(tuple(node.config))

    def heap_empty(self):
        return len(self.heap) == 0

    def get_element(self, node):
        for state in self.heap:
            if state[1].config == node.config:
                return state[1]





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

    def __lt__(self, other):
        if self.cost < other.cost:
            return True
        elif self.action == "Up":
            if other.action == "Up":
                return False
            elif other.action == "Down":
                return False
            elif other.action == "Left":
                return False
            elif other.action == "Right":
                return False

        elif self.action == "Down":
            if other.action == "Up":
                return True
            elif other.action == "Down":
                return False
            elif other.action == "Left":
                return True
            elif other.action == "Right":
                return True

        elif self.action == "Left":
            if other.action == "Up":
                return True
            elif other.action == "Down":
                return True
            elif other.action == "Left":
                return True
            elif other.action == "Right":
                return False

        elif self.action == "Right":
            if other.action == "Up":
                return True
            elif other.action == "Down":
                return True
            elif other.action == "Left":
                return True
            elif other.action == "Right":
                return True


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
        new_state = PuzzleState(self.config[:], self.n, self, self.action, self.cost + 1)
        if new_state.blank_index > self.n:
            new_state.config[new_state.blank_index], new_state.config[new_state.blank_index - self.n] = new_state.config[
                                                                                                       new_state.blank_index - self.n], \
                                                                                                   new_state.config[
                                                                                                       new_state.blank_index]
            new_state.action = "Up"
        else:
            return None

        return new_state
        pass

    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        new_state = PuzzleState(self.config[:], self.n, self, self.action, self.cost+1)
        if new_state.blank_index < (len(self.config) - self.n):
            new_state.config[new_state.blank_index], new_state.config[new_state.blank_index + self.n] = new_state.config[
                                                                                                       new_state.blank_index + self.n], \
                                                                                                   new_state.config[
                                                                                                       new_state.blank_index]
            new_state.action = "Down"
        else:
            return None

        return new_state
        pass

    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        new_state = PuzzleState(self.config[:], self.n, self, self.action, self.cost+1)
        if (new_state.blank_index % self.n) != 0 and new_state.blank_index > 0:
            new_state.config[new_state.blank_index], new_state.config[new_state.blank_index - 1] = new_state.config[
                                                                                                       new_state.blank_index - 1], \
                                                                                                   new_state.config[
                                                                                                       new_state.blank_index]
            new_state.action = "Left"
        else:
            return None
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

        new_state = PuzzleState(self.config[:], self.n, self, self.action, self.cost+1)
        if (new_state.blank_index % self.n) != self.n - 1:  # and new_state.blank_index < self.n:
            new_state.config[new_state.blank_index], new_state.config[new_state.blank_index + 1] = new_state.config[
                                                                                                       new_state.blank_index + 1], \
                                                                                                   new_state.config[
                                                                                                       new_state.blank_index]
            new_state.action = "Right"
        else:
            return None
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
    #path to goal: done

    pass


#WORKS
def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    # use explicit queue
    frontier = Frontier("queue")
    frontier.put(initial_state)
    explored = set()
    moves = []

    while not frontier.empty():
        # print(explored)
        state = frontier.get()
        #print(state.config)
        explored.add(tuple(state.config))
        #print(tuple(state.config))

        #print(test_goal(state))
        if test_goal(state):
            #print(state.config)
            while state.parent:
                moves.append(state.action)
                state = state.parent
            print(moves[::-1])
            return True

        for neighbor in state.expand():
            #print(neighbor.config)
            if tuple(neighbor.config) not in explored and not frontier.search(neighbor):
            #if tuple(neighbor.config) not in explored:
                frontier.put(neighbor)

    return False
    # pass


def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    # queue holds puzzle states
    #when expand, reverse the list
    frontier = Frontier("stack")
    frontier.push(initial_state)
    #print(frontier.pop().config)
    explored = set()
    moves = []

    while not frontier.stack_empty():
        state = frontier.pop()
        #print(state.config)
        explored.add(tuple(state.config))

        if test_goal(state):
            while state.parent:
                #print(state.config)
                moves.append(state.action)
                state = state.parent
            print(moves[::-1])
            return True

        for neighbor in state.expand()[::-1]:
            if not frontier.stack_search(neighbor) and neighbor not in explored:
                frontier.push(neighbor)

    return False
    pass


def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    frontier = Frontier("heap")
    cost = calculate_total_cost(initial_state)
    frontier.heap_push(cost, initial_state)
    explored = set()

    while not frontier.heap_empty():
        state = frontier.delete_min()
        explored.add(tuple(state.config))
        moves = []

        if test_goal(state):
            tc = state.cost
            while state.parent:
                #print(state.config)
                moves.append(state.action)
                state = state.parent
            print(moves[::-1])
            print(tc)
            return True


        for neighbor in state.expand():
            #tuple(neighbor.config) not in explored
            if neighbor not in explored and not frontier.heap_search(neighbor):
                cost = calculate_total_cost(neighbor)
                frontier.heap_push(cost, neighbor)

            elif frontier.heap_search(neighbor):
                #check if lower cost, then replace it
                #get the cost of the state that is in the frontier
                if calculate_total_cost(frontier.get_element(neighbor)) > calculate_total_cost(neighbor):
                    #remove it from the heap
                    frontier.remove_duplicate(neighbor)

                    #add
                    frontier.heap_push(calculate_total_cost(neighbor), neighbor)
                    #print(calculate_total_cost(neighbor))


    return False
    pass


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    # cost = initial_state.cost + manhattan_cost

    TC = 0
    for tile in state.config:
        if tile != 0:
            TC = TC + calculate_manhattan_dist(tile, state.config[tile], state.n)
    return TC + state.cost
    pass


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    #M = abs(x1 - y1) + abs(x2 - y2)
    #how to determine how far a tile is from where it is supposed to be?
    # iterate through rows, columns
    # do it from index, then do it for goal
    #     subtract magniutdes to find it
    # row 0, 1, 2
    # col 0, 1, 2
    # to find where it should be
    # /3 = row numbers
    # %3 = row numbers

    start_row = int(idx / 3)
    start_col = idx % 3

    goal_row = int(value / 3)
    goal_col = value % 3

    distance = abs(start_row - goal_row) + abs(start_col - goal_col)
    return distance


    pass


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    copy = puzzle_state.config.copy()
    #print(copy)

    new_list = sorted(copy)
    #print(sorted(puzzle_state.config))
    if (puzzle_state.config == new_list):
        print(puzzle_state.config)
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
        print(bfs_search(PuzzleState([6,1,8,4,0,2,7,3,5], 3)))
    elif search_mode == "dfs":
        print(dfs_search(hard_state))
    elif search_mode == "ast": A_star_search(hard_state)
    else:
        print("Enter valid command arguments !")

    end_time = time.time()
    print("Program completed in %.3f second(s)" % (end_time - start_time))


if __name__ == '__main__':
    main()