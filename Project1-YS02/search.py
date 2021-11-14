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
    #   function DEPTH-FIRST-SEARCH(problem) returns a solution or failure

    # node ← a node with STATE=problem.INITIAL-STATE, PATH-COST=0
    node = (problem.getStartState(), 0, False, False)
    # if problem.GOAL-TESt(node.STATE) then return SOLUTION(node)
    if problem.isGoalState(node[0]) == True:
            return []
    # frontier ← a FIFO queue with node as the only element
    frontier = util.Stack()
    frontier.push(node)
    # explored ← an empty set
    explored = set()
    # loop do
    while True:
        # if EMPTY?(frontier) then return failure
        if frontier.isEmpty() == True:
            return False
        # node ← POP(frontier)
        node = frontier.pop()
        # add node.STATE to explored
        explored.add(node[0])

        # if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
        if problem.isGoalState(node[0]):
            solution = []
            currentNode = node
            # While there is a parent node to go to, insert the actions to go there
            # and update the currentNode to the currentNode's parent
            while currentNode[3]:
                solution.insert(0, currentNode[2])
                currentNode = currentNode[3]

            return solution

        # for each action in problem.ACTIONS(node.STATE) do
        for expandedNode in problem.expand(node[0]):
            # child ← CHILD-NODE(problem, node, action)
            # child stores the child to the current state, the stepCost,
            # the action to get there and the parent node of the child
            child = (expandedNode[0], expandedNode[2], expandedNode[1], node)
            # if child.STATE is not in explored or frontier then
            if child[0] not in explored:
                # frontier ← INSERT(child, frontier)
                    frontier.push(child)
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    #   function BREADTH-FIRST-SEARCH(problem) returns a solution or failure

    # node ← a node with STATE=problem.INITIAL-STATE, PATH-COST=0
    node = (problem.getStartState(), 0, False, False)
    # if problem.GOAL-TESt(node.STATE) then return SOLUTION(node)
    if problem.isGoalState(node[0]) == True:
            return []
    # frontier ← a FIFO queue with node as the only element
    frontier = util.Queue()
    frontier.push(node)
    # explored ← an empty set
    explored = set()
    # loop do
    while True:
        # if EMPTY?(frontier) then return failure
        if frontier.isEmpty() == True:
            return False
        # node ← POP(frontier)
        node = frontier.pop()
        # add node.STATE to explored
        explored.add(node[0])

        # if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
        if problem.isGoalState(node[0]):
            solution = []
            currentNode = node
            # While there is a parent node to go to, insert the actions to go there
            # and update the currentNode to the currentNode's parent
            while currentNode[3]:
                solution.insert(0, currentNode[2])
                currentNode = currentNode[3]

            return solution

        # for each action in problem.ACTIONS(node.STATE) do
        for expandedNode in problem.expand(node[0]):
            # child ← CHILD-NODE(problem, node, action)
            # child stores the child to the current state, the stepCost,
            # the action to get there and the parent node of the child
            child = (expandedNode[0], expandedNode[2], expandedNode[1], node)
            # if child.STATE is not in explored or frontier then
            if child[0] not in explored:
                if(child[0]) not in (node[0] for node in frontier.list):
                # frontier ← INSERT(child, frontier)
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
    #   function A-STAR-SEARCH(problem) returns a solution or failure

    # node ← a node with STATE=problem.INITIAL-STATE, PATH-COST=0
    node = (problem.getStartState(), 0, False, False)
    # if problem.GOAL-TESt(node.STATE) then return SOLUTION(node)
    if problem.isGoalState(node[0]) == True:
            return []
    # frontier ← a FIFO queue with node as the only element
    frontier = util.PriorityQueue()
    frontier.push(node, 0)
    # explored ← an empty set
    explored = set()
    # loop do
    while True:
        # if EMPTY?(frontier) then return failure
        if frontier.isEmpty() == True:
            return False
        # node ← POP(frontier)
        node = frontier.pop()
        # add node.STATE to explored
        if node in explored:
            continue
        explored.add(node[0])

        # if problem.GOAL-TEST(child.STATE) then return SOLUTION(child)
        if problem.isGoalState(node[0]):
            solution = []
            currentNode = node
            # While there is a parent node to go to, insert the actions to go there
            # and update the currentNode to the currentNode's parent
            while currentNode[3]:
                solution.insert(0, currentNode[2])
                currentNode = currentNode[3]

            return solution

        # for each action in problem.ACTIONS(node.STATE) do
        for expandedNode in problem.expand(node[0]):
            # child ← CHILD-NODE(problem, node, action)
            # child stores the child to the current state, the stepCost,
            # the action to get there and the parent node of the child
            child = (expandedNode[0], expandedNode[2], expandedNode[1], node)
            sequence = []
            currentNode = node
            # While there is a parent node to go to, insert the actions to go there
            # and update the currentNode to the currentNode's parent
            while currentNode[3]:
                sequence.insert(0, currentNode[2])
                currentNode = currentNode[3]
            # print(action, "==")
            costOfSequence = problem.getCostOfActionSequence(sequence)
            # if child.STATE is not in explored or frontier then
            if child[0] not in explored:
                # if(child[0]) not in (node[0] for node in frontier.heap):
                # frontier ← INSERT(child, frontier)
                    frontier.push(child, costOfSequence + heuristic(expandedNode[0], problem))
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
