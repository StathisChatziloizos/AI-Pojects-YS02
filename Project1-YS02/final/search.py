# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from typing import Sequence
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def expand(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (child,
        action, stepCost), where 'child' is a child to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that child.
        """
        util.raiseNotDefined()

    def getActions(self, state):
        """
          state: Search state

        For a given state, this should return a list of possible actions.
        """
        util.raiseNotDefined()

    def getActionCost(self, state, action, next_state):
        """
          state: Search state
          action: action taken at state.
          next_state: next Search state after taking action.

        For a given state, this should return the cost of the (s, a, s') transition.
        """
        util.raiseNotDefined()

    def getNextState(self, state, action):
        """
          state: Search state
          action: action taken at state

        For a given state, this should return the next state after taking action from state.
        """
        util.raiseNotDefined()

    def getCostOfActionSequence(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]


def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    """
    "*** YOUR CODE HERE ***"
    # DFS algorithm and naming convention taken from class's notes.
    # graph_search.pdf, page 27 - slightly modified for DFS

    #   function DEPTH-FIRST-SEARCH(problem) returns a solution or failure

    # node stores the starting state, an empty list of actions, 0 cost and no parent node
    node = (problem.getStartState(), [], 0, False)

    # If node is the goal state, then an empty sequence of moves gets returned
    if problem.isGoalState(node[0]) == True:
            return []

    # Frontier - Stack for DFS
    frontier = util.Stack()

    # Push node to the frontier
    frontier.push(node)

    # explored is an empty set
    explored = set()

    # loop do
    while True:
        # if EMPTY?(frontier) then return failure
        if frontier.isEmpty() == True:
            return False

        # node POP(frontier)
        node = frontier.pop()

        # if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
        if problem.isGoalState(node[0]):
            solution = []
            currentNode = node
            # While there is a parent node to go to, insert the actions to go there
            # and update the currentNode to the currentNode's parent
            while currentNode[3]:
                solution.insert(0, currentNode[1])
                currentNode = currentNode[3]

            # Returns the sequence of moves to get to the Goal State
            return solution

        # for each expanded node
        for expandedNode in problem.expand(node[0]):

            # child - CHILD-NODE(state, action, stepCost, parentNode)
            child = (expandedNode[0], expandedNode[1], expandedNode[2], node)

            # If child hasn't yet been explored, add it to the explored set
            if child[0] not in explored:
                    explored.add(node[0])

                    # frontier - INSERT(child, frontier)
                    frontier.push(child)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    # BFS algorithm and naming convention taken from class's notes.
    # graph_search.pdf, page 27
    
    #BREADTH-FIRST-SEARCH(problem) returns a solution or failure

    # node stores the starting state, an empty list of actions, 0 cost and no parent node
    node = (problem.getStartState(), [], 0, False)
    
    # If node is the goal state, then an empty sequence of moves gets returned
    if problem.isGoalState(node[0]) == True:
            return []
    
    # Frontier - Queue for BFS 
    frontier = util.Queue()

    # Push node to the frontier
    frontier.push(node)

    # explored is an empty set
    explored = set()

    # loop do
    while True:
        # if EMPTY?(frontier) then return failure
        if frontier.isEmpty() == True:
            return False

        # node - POP(frontier)
        node = frontier.pop()

        # if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
        if problem.isGoalState(node[0]):
            solution = []
            currentNode = node
            # While there is a parent node to go to, insert the actions to go there
            # and update the currentNode to the currentNode's parent
            while currentNode[3]:
                solution.insert(0, currentNode[1])
                currentNode = currentNode[3]

            # Returns the sequence of moves to get to the Goal State
            return solution

        # for each expanded node
        for expandedNode in problem.expand(node[0]):

            # child - CHILD-NODE(state, action, stepCost, parentNode)
            child = (expandedNode[0], expandedNode[1], expandedNode[2], node)

            # If child hasn't yet been explored, add it to the explored set
            if child[0] not in explored:
                explored.add(node[0])

                # If child.STATE is not in the frontier queue
                if child[0] not in (node[0] for node in frontier.list):
                # frontier - INSERT(child, frontier)
                    frontier.push(child)
    

    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    # A* algorithm and naming convention taken from class's notes.
    # graph_search.pdf, page 27 - slightly modified for A*

    # A-STAR-SEARCH(problem) returns a solution or failure

    # node stores the starting state, an empty list of actions, 0 cost and no parent node
    node = (problem.getStartState(), [], 0, False)

    # If node is the goal state, then an empty sequence of moves gets returned
    if problem.isGoalState(node[0]):
        return []

    # Frontier - Priority Queue for BFS
    # Priority is based on the combinded cost of the step and the heuristic
    frontier = util.PriorityQueue()

    # Push node to the frontier - 0 cost for the starting state
    frontier.push(node, 0)

    # explored is an empty set
    explored = set()

    # loop do
    while True:
        # if EMPTY?(frontier) then return failure
        if frontier.isEmpty() == True:
            return False

        # node - POP(frontier)   
        node = frontier.pop()

        # if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
        if problem.isGoalState(node[0]):
            # node[1] stores the sequence of moves to get to the goal state
            return node[1]

        # If node hasn't yet been explored, add it to the explored set
        if node[0] not in explored:
            explored.add(node[0])

            # for each expanded node
            for expandedNode in problem.expand(node[0]):

                # Sequence stores the sequence of actions to get to Node
                # Plus the action to get to the newly expanded node from Node
                sequence = node[1] + [expandedNode[1]]

                # totalCost stores the total cost to get to Node plus the
                # cost to get to the newly expanded node from Node
                totalCost = node[2] + expandedNode[2]

                # child - CHILD-NODE(state, sequence, totalCost, parentNode)
                # child stores the current state, the sequence of actions to get to
                # the newly expanded node, the total cost and the parent node of the child
                child = (expandedNode[0], sequence, totalCost, node)

                # frontier - INSERT(child, frontier)
                # child is given priority based on the combined totalCost to get to the child
                # and the result of the heuristic of the child
                frontier.push(child, totalCost + heuristic(expandedNode[0], problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
