# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and child states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed child
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        childGameState = currentGameState.getPacmanNextState(action)
        newPos = childGameState.getPacmanPosition()
        newFood = childGameState.getFood()
        newGhostStates = childGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        # List of the positions of each dot
        foodList = newFood.asList()

        bonus = 0
        # Incentive to get closer to food
        for food in foodList:
            # The closer a dot is, the bigger the incentive
            distance = util.manhattanDistance(newPos, food)
            bonus += 5/(distance**2)

        # Deterrent to avoid unscared ghosts
        ghostPenalty = 0
        for ghost in newGhostStates:
            # If the ghost is at least a move away of getting back to normal
            # we can skip it, as it poses no threat to pacman
            if ghost.scaredTimer > 1:
                continue
            # Getting too close to a ghost results in a big penalty, that
            # overpowers the score and any food bonuses
            if util.manhattanDistance(ghost.getPosition(), newPos) < 3:
                ghostPenalty = 9999

        # Evaluation = score + bonus - ghostPenalty
        return childGameState.getScore() + bonus - ghostPenalty

def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.getNextState(agentIndex, action):
        Returns the child game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        def minimax(gameState, agentIndex, depth):
            # Minimax algorithm is a modified version of the pseudocode from
            # https://en.wikipedia.org/wiki/Minimax
            # Small changes have been made to accommodate multiple agents (MIN's ply).
            # maximizingPlayer parameter is not needed, due to the fact that Pacman
            # is always agent 0 (MAX) and the rest of the agents/ghosts are MIN

            # All legal moves of the current agent
            legalMoves = gameState.getLegalActions(agentIndex)

            # If final depth is reached or a goalState is reached 
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                # Return the value of the sequence of moves
                return self.evaluationFunction(gameState)
            
            # MAX -- Pacman is always agent 0
            if agentIndex == 0:
                value = -999999
                for action in legalMoves:
                    nextState = gameState.getNextState(agentIndex, action)
                    # agentIndex + 1 signifies MIN's ply
                    value = max(value, minimax(nextState, agentIndex + 1, depth))
                return value
            # MIN -- Rest of the agents / Ghosts
            else:
                # Go to the next agentIndex
                nextAgent = agentIndex + 1
                value = 999999

                # Once all agents have been checked, it's MAX's ply
                # and depth gets increased
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                    depth += 1
                
                for action in legalMoves:
                    nextState = gameState.getNextState(agentIndex, action)
                    value = min(value, minimax(nextState, nextAgent, depth))
                return value

        # Legal moves of Pacman (Pacman is always agent 0 - self.index is 0)
        legalMoves = gameState.getLegalActions(self.index)

        # Pacman is MAX
        startMax = -999999

        for action in legalMoves:
            nextState = gameState.getNextState(self.index, action)
            # Starting depth is 0
            value = minimax(nextState, self.index+1, 0)
            # Get the move with the highest value
            if value > startMax:
                startMax = value
                move = action

        # Return the best move
        return move


        util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def alphabeta(gameState, agentIndex, depth, a, b):
            # Alpha–beta pruning algorithm is a combination of the pseudocode from
            # https://en.wikipedia.org/wiki/Alpha-beta_pruning
            # and the max_value and min-value algorithms on Berkley's site.
            # Modifiacations have been made to accommodate multiple agents (MIN's ply).
            # maximizingPlayer parameter is not needed, due to the fact that Pacman
            # is always agent 0 (MAX) and the rest of the agents / ghosts are MIN

            # All legal moves of the current agent
            legalMoves = gameState.getLegalActions(agentIndex)

            # If final depth is reached or a goalState is reached 
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                # Return the value of the sequence of moves
                return self.evaluationFunction(gameState)
            
            # MAX -- Pacman is always agent 0
            if agentIndex == 0:
                value = -999999
                for action in legalMoves:
                    nextState = gameState.getNextState(agentIndex, action)
                    # agentIndex + 1 signifies MIN's ply
                    value = max(value, alphabeta(nextState, agentIndex + 1, depth, a, b))
                    if value > b:
                        return value
                    a = max(a,value)
                return value
            # MIN -- Rest of the agents / Ghosts
            else:
                # Go to the next agentIndex
                nextAgent = agentIndex + 1
                value = 999999

                # Once all agents have been checked, it's MAX's ply
                # and depth gets increased
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                    depth += 1
                
                for action in legalMoves:
                    nextState = gameState.getNextState(agentIndex, action)
                    value = min(value, alphabeta(nextState, nextAgent, depth, a, b))
                    if value < a:
                        return value
                    b = min(b,value)
                return value

        # Legal moves of Pacman (Pacman is always agent 0 - self.index is 0)
        legalMoves = gameState.getLegalActions(self.index)

        # Pacman is MAX
        startMax = -999999

        alpha = -999999
        beta = 999999
        for action in legalMoves:
            nextState = gameState.getNextState(self.index, action)
            # Starting depth is 0
            value = alphabeta(nextState, self.index+1, 0, alpha, beta)
            # Get the move with the highest value
            if value > startMax:
                startMax = value
                move = action
            if value > beta:
                return value
            alpha = max(alpha, value)

        # Return the best move
        return move
        util.raiseNotDefined()

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        def expectimax(gameState, agentIndex, depth):
            # Expectimax algorithm is a based on the above implementation of
            # minimax, modified to have chance nodes and not a MIN ply. The
            # algorithm used for the chance nodes is based on "def exp-value(state)"
            # from Berkley's FA18 - cs188 - lecture 7,
            # https://inst.eecs.berkeley.edu/~cs188/fa18/assets/slides/lec7/FA18_cs188_lecture7_expectimax_search_and_utilities_1pp.pdf
            # Slide 8


            # All legal moves of the current agent
            legalMoves = gameState.getLegalActions(agentIndex)

            # If final depth is reached or a goalState is reached 
            if depth == self.depth or gameState.isWin() or gameState.isLose():
                # Return the value of the sequence of moves
                return self.evaluationFunction(gameState)
            
            # MAX -- Pacman is always agent 0
            if agentIndex == 0:
                value = -999999
                for action in legalMoves:
                    nextState = gameState.getNextState(agentIndex, action)
                    # agentIndex + 1 signifies MIN's ply
                    value = max(value, expectimax(nextState, agentIndex + 1, depth))
                return value

            # Chance nodes -- Rest of the agents / Ghosts
            else:
                # Go to the next agentIndex
                nextAgent = agentIndex + 1
                value = 999999

                # Once all agents have been checked, it's MAX's ply
                # and depth gets increased
                if gameState.getNumAgents() == nextAgent:
                    nextAgent = 0
                    depth += 1

                expectedValue = 0

                # Equal probability for every move
                probability = 1/len(legalMoves)

                # For every legal move calculate it's value and update the expectedValue
                for action in legalMoves:
                    nextState = gameState.getNextState(agentIndex, action)
                    value = expectimax(nextState, nextAgent, depth)
                    expectedValue += value * probability
                return expectedValue

        # Legal moves of Pacman (Pacman is always agent 0 - self.index is 0)
        legalMoves = gameState.getLegalActions(self.index)

        # Pacman is MAX
        startMax = -999999

        for action in legalMoves:
            nextState = gameState.getNextState(self.index, action)
            # Starting depth is 0
            value = expectimax(nextState, self.index+1, 0)
            # Get the move with the highest value
            if value > startMax:
                startMax = value
                move = action

        # Return the best move
        return move
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    # Modified version of the evaluation function for Question 1.
    # Basic scoring according to the location of food (like Q1).
    # Actively seeks for scared ghosts, because they don't pose a threat and
    # they might block access to food.

    # Useful information you can extract from a GameState (pacman.py)
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    # List of the positions of each dot
    foodList = newFood.asList()

    bonus = 0
    # Incentive to get closer to food
    for food in foodList:
        # The closer a dot is, the bigger the incentive
        distance = util.manhattanDistance(newPos, food)
        bonus += 5/(distance**2)

    # Deterrent to avoid unscared ghosts
    ghostPenalty = 0
    for ghost in newGhostStates:
        # If the ghost is scared dont avoid it. It will
        # likely block access to food
        if ghost.scaredTimer > 1:
            # Bonus to follow the ghost
            ghostPenalty = -100
        else:
            # Getting too close to an unscared ghost results in a big penalty,
            # that overpowers the score and any food bonuses
            if util.manhattanDistance(ghost.getPosition(), newPos) < 1:
                ghostPenalty = 9999

    # Evaluation = score + bonus - ghostPenalty
    return currentGameState.getScore() + bonus - ghostPenalty
    util.raiseNotDefined()    

# Abbreviation
better = betterEvaluationFunction
