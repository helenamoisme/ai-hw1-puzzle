from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[self.n*i : self.n*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        
        if self.blank_index < self.n:
            return None
        target = self.blank_index-self.n
        config = list(self.config)
        config[self.blank_index]=config[target]
        config[target]=0
        return PuzzleState(config, self.n, self, "Up", self.cost+1)
    
      
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        
         
        if self.blank_index >= self.n*(self.n - 1):
            return None
        target = self.blank_index+self.n
        config = list(self.config)
        config[self.blank_index]=config[target]
        config[target]=0
        return PuzzleState(config, self.n, self, "Down", self.cost+1)
    
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        
         
        if self.blank_index % self.n==0:
            return None
        target = self.blank_index-1
        config = list(self.config)
        config[self.blank_index]=config[target]
        config[target]=0
        return PuzzleState(config, self.n, self, "Left", self.cost+1)
    

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        
         
        if self.blank_index % self.n==self.n-1:
            return None
        target = self.blank_index+1
        config = list(self.config)
        config[self.blank_index]=config[target]
        config[target]=0
        return PuzzleState(config, self.n, self, "Right", self.cost+1)
    
      
    def expand(self):
        """ Generate the child nodes of this node """
        
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
def writeOutput(goal_state, nodes_expanded, max_search_depth, start_time):
    ### Student Code Goes here
    import resource
    path = []
    state = goal_state
    
    while state is not None and state.parent is not None:
        path.append(state.action)
        state = state.parent

    path.reverse()
    depth = len(path)
    if goal_state is None:
        depth = -1

    running_time = time.perf_counter() - start_time
    ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    if sys.platform == "darwin":
        ram = ram / (1024 * 1024)
    else:
        ram = ram / 1024

    with open("output.txt", "w") as f:
        f.write(f"path_to_goal: {path}\n")
        f.write(f"cost_of_path: {depth}\n")
        f.write(f"nodes_expanded: {nodes_expanded}\n")
        f.write(f"search_depth: {depth}\n")
        f.write(f"max_search_depth: {max_search_depth}\n")
        f.write(f"running_time: {running_time:.8f}\n")
        f.write(f"max_ram_usage: {ram:.8f}\n")
    

def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    start_time = time.perf_counter()
    frontier=Q.Queue()
    frontier.put(initial_state)
    discovered = set()
    
    discovered.add(tuple(initial_state.config))
    nodes_expanded=0
    max_search_depth=initial_state.cost
    while not frontier.empty():
        state=frontier.get()
        if test_goal(state):
            writeOutput(state, nodes_expanded, max_search_depth, start_time)
            return state
        nodes_expanded=nodes_expanded+1
        children = state.expand()
        for child in children:
            key = tuple(child.config)
            if key not in discovered:
                discovered.add(key)
                frontier.put(child)
                if child.cost > max_search_depth:
                    max_search_depth = child.cost
        state.children = []
    writeOutput(None, nodes_expanded, max_search_depth, start_time)
    return None
  
    

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    
    start_time = time.perf_counter()

    stack = [initial_state]
    seen = set()
    seen.add(tuple(initial_state.config))

    nodes_expanded = 0
    max_search_depth = 0

    while len(stack) > 0:
        state = stack.pop()

        if test_goal(state):
            writeOutput(state, nodes_expanded,
                        max_search_depth, start_time)
            return state

        nodes_expanded = nodes_expanded + 1

        children = state.expand()
        children.reverse()

        for child in children:
            board = tuple(child.config)

            if board not in seen:
                seen.add(board)
                stack.append(child)

                if child.cost > max_search_depth:
                    max_search_depth = child.cost

        state.children = []

    writeOutput(None, nodes_expanded, max_search_depth, start_time)
    return None

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
    
    start_time = time.perf_counter()

    queue = Q.PriorityQueue()
    order = 0
    score = calculate_total_cost(initial_state)
    queue.put((score, order, initial_state))

    best = {}
    best[tuple(initial_state.config)] = initial_state.cost

    visited = set()
    nodes_expanded = 0
    max_search_depth = 0

    while not queue.empty():
        item = queue.get()
        state = item[2]
        board = tuple(state.config)

        if board in visited:
            continue

        if state.cost != best[board]:
            continue

        if test_goal(state):
            writeOutput(state, nodes_expanded,
                        max_search_depth, start_time)
            return state

        visited.add(board)
        nodes_expanded = nodes_expanded + 1

        children = state.expand()

        for child in children:
            child_board = tuple(child.config)

            if child_board in visited:
                continue

            better = False

            if child_board not in best:
                better = True
            elif child.cost < best[child_board]:
                better = True

            if better:
                best[child_board] = child.cost
                order = order + 1
                score = calculate_total_cost(child)
                queue.put((score, order, child))

                if child.cost > max_search_depth:
                    max_search_depth = child.cost

        state.children = []

    writeOutput(None, nodes_expanded, max_search_depth, start_time)
    return None


def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    
    distance = 0

    for i in range(len(state.config)):
        number = state.config[i]

        if number != 0:
            distance = distance + calculate_manhattan_dist(
                i, number, state.n
            )

    return state.cost + distance


def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    ### STUDENT CODE GOES HERE ###
    
    if value == 0:
        return 0

    row = idx // n
    col = idx % n

    goal_row = value // n
    goal_col = value % n

    distance = abs(row - goal_row) + abs(col - goal_col)

    return distance


def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    ### STUDENT CODE GOES HERE ###
    
    for i in range(len(puzzle_state.config)):
        if puzzle_state.config[i] != i:
            return False

    return True


# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    if len(sys.argv) != 3:
        print("Please provide a search method and a board.")
        print("Example: python3 puzzle.py bfs 1,2,5,3,4,0,6,7,8")
        return

    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
