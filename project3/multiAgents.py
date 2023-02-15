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
        # Collect legal moves and successor states
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

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        score = 0
        #print(newGhostStates)
        x, y = currentGameState.getPacmanPosition()
        nextx, nexty = newPos

        if newFood[nextx][nexty] == True:
            score += 1000                                                   #if Pacman eats food with the next move increase score by many cause that's really good!

        newDistances = []
        oldDistances = []

        foodList = newFood.asList()
        for food in foodList:                                                               #calculate distances between Pacman and food dots
            newDistances.append(abs(food[0] - nextx) + abs(food[1] - nexty))                
            oldDistances.append(abs(food[0] - x) + abs(food[1] - y))

        if len(oldDistances) > 0:                                                           #check difference between new and current distances between Pacman and foods
            if min(oldDistances) > min(newDistances):
                score += 50                                                                 #if pacman gets closer to closest food give him points
            else:
                score -= 5                                                                  #else take points
        

        for ghost in newGhostStates:
            ghostx, ghosty = ghost.getPosition()                                            #ghosts make a move
            newDist = abs(ghostx - nextx) + abs(ghosty - nexty)
            oldDist = abs(ghostx - x) + abs(ghosty - y)                                     
            if newDist == 0:                                                                #for that move if new position of Pacman is on the ghosts' positions then decrease score
                score = -500                                                                
            #here I have 2 distances. First, newDist is distance between new Pacman's position and new ghosts' positions
            #oldDist is distance between current Pacman's position and new ghosts' position
                                                                            
            #check difference between new Pacman's position and new ghosts' position 
            if newDist > oldDist:                                                           #if distance gets bigger then that means Pacman is getting away from ghosts and that's good so give him a few points
                score += 5
            elif newDist == oldDist:                                                        #if it's the same then just give him 1 (cause that's not good but it's also not bad!)
                score += 1
            

        
        return score

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

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, 0, 0)[1]                  #returns the action via maxValue cause we want the moves for Pacman, who's MAX in this occasion
        util.raiseNotDefined()

    def minimaxDecision(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():           #check if we reached end state (win, lose, max depth)
            return self.evaluationFunction(gameState)
        if agentIndex == 0:                                                                                     #check if it's Pacman else it's ghosts
            return self.maxValue(gameState, agentIndex, depth)[0]
        else:
            return self.minValue(gameState, agentIndex, depth)[0]


    def maxValue(self, gameState, agentIndex, depth):
        v = (-float("inf"), "none")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)                                
            nextIndex = agentIndex + 1                                                                      #next agent is needed
            successorValue = (self.minimaxDecision(successorState, nextIndex, depth + 1), action)           #get the value of child nodes 
            v = max(v, successorValue)

        return v

    def minValue(self, gameState, agentIndex, depth):
        v = (float("inf"), "none")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            nextIndex = agentIndex + 1
            if nextIndex == gameState.getNumAgents():                                                       #because we have multiple ghosts I increase index by 1 to check next ghost until we reach maximum number of
                nextIndex = 0                                                                               #agents, we see that by checking if the value of index reaches the value of getNumAgents and if it's true I 
                                                                                                            #change the value of index to zero so we can check about Pacman again
            successorValue = (self.minimaxDecision(successorState, nextIndex, depth + 1), action)
            v = min(v, successorValue)

        return v

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        return self.maxValue(gameState, 0, 0, -float("inf"), float("inf"))[1]
        util.raiseNotDefined()

    def alphaBetaDecision(self, gameState, agentIndex, depth, a, b):
        if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():           
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth, a, b)[0]
        else:
            return self.minValue(gameState, agentIndex, depth, a, b)[0]


    def maxValue(self, gameState, agentIndex, depth, a, b):
        v = (-float("inf"), "none")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)                                
            nextIndex = agentIndex + 1                                                                      
            successorValue = (self.alphaBetaDecision(successorState, nextIndex, depth + 1, a, b), action)          
            v = max(v, successorValue)
            if v[0] > b:                                                                               #if value is bigger than best value for MIN (beta) then return cause we don't need to look deeper
                return v
            a = max(a, v[0])                                                                            #check if new value of v is greater than alpha, if that's true set alpha equal to that value, else do nothing
        return v

    def minValue(self, gameState, agentIndex, depth, a, b):
        v = (float("inf"), "none")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)
            nextIndex = agentIndex + 1
            if nextIndex == gameState.getNumAgents():                                                       
                nextIndex = 0                                                                               
   
            successorValue = (self.alphaBetaDecision(successorState, nextIndex, depth + 1, a, b), action)
            v = min(v, successorValue)
            if v[0] < a:                                                                               #if value is less than best value for MAX (alpha) then return cause we don't have to look deeper
                return v
            b = min(b, v[0])                                                                            #check if new value of v is less than beta, if that's true set beta equal to that value, else do nothing
        return v

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
        return self.maxValue(gameState, 0, 0)[1]
        util.raiseNotDefined()

    def expectimaxDecision(self, gameState, agentIndex, depth):
        if gameState.isWin() or gameState.isLose() or depth == self.depth * gameState.getNumAgents():
            return self.evaluationFunction(gameState)
        if agentIndex == 0:
            return self.maxValue(gameState, agentIndex, depth)[0]
        else:
            return self.expectedValue(gameState, agentIndex, depth)[0]

    def maxValue(self, gameState, agentIndex, depth):
        v = (-float("inf"), "none")
        legalActions = gameState.getLegalActions(agentIndex)
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)                                
            nextIndex = agentIndex + 1
            successorValue = (self.expectimaxDecision(successorState, nextIndex, depth + 1), action) 
            v = max(v, successorValue)

        return v

    def expectedValue(self, gameState, agentIndex, depth):
        chance = 0
        legalActions = gameState.getLegalActions(agentIndex)
        length = len(legalActions)
        probability = 1.0 / length                                                                          # we assume that all actions have the same probability to occur
        for action in legalActions:
            successorState = gameState.generateSuccessor(agentIndex, action)                         
            nextIndex = agentIndex + 1
            if nextIndex == gameState.getNumAgents():
                nextIndex = 0
            successorValue = (self.expectimaxDecision(successorState, nextIndex, depth + 1), action) 
            chance += probability * successorValue[0]                                       #according to the algorithm, chance value of each node is the sum of values of their child nodes multiplied by probability

                                    #since these nodes are chance nodes we don't care about what exact action ghosts take (ghosts move randomly) but only for the average chance value of all those actions, 
        return (chance, action)     # so I return the last action that was randomly checked

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"

    score = 0                                                           #my evaluation score (NOT THE ACTUAL SCORE OF PACMAN GAME)
    ghostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    capsules = currentGameState.getCapsules()
    x, y = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    foodList = newFood.asList()

    if currentGameState.isWin():                                        #if current state is win state that's really really good
        return 100000
    elif currentGameState.isLose():                                     #if current state is lose state that's pretty bad
        return -100000

    score += 10 * currentGameState.getScore()                           #the current score of the game is the best criteria telling us how we're going, so of course the better the score the better for Pacman 

    capsuleMultiplier = -20                                             #capsules are important for eating ghosts. Pacman must prioritize them, so the more capsules remaining, the worse a game state is
    score += capsuleMultiplier * len(capsules)

    foodsMultiplier = -10                                               #for Pacman to win the game, he must eat all the dots, so the more food dots remaining, the worse a game state is

    closestFoodMultiplier = -5                                          #Pacman must prefer closest food dots cause it's easier and faster to eat, so the closer the food is, the better for Pacman

    closestScaredGhostMultiplier = -15                                  #Pacman must hunt scared ghost so he can eat them and get points

    #capsules must be first priority cause they help pacman eat ghosts and get many points and also avoid death, therefore scared ghosts are second priority. After those, the next important thing
    #for Pacman is to eat food dots so he can win, therefore the number of dots remaining come third in priority. Last but not least are the closest foods, Pacman should prefer them but not prioritize them
    #cause sometimes it may be a worse option to take that action. Hence, the priority order is: Capsules > Closest Scared Ghost > Remaining food dots > Closest remaining food dot. Normal ghosts are very important
    #too but we don't need to put them in order cause there are many occasions, like if they are too far away they don't bother Pacman, even if they get closer to Pacman it's not a problem cause Pacman will still 
    #be moving to a direction which is better for him in other ways. So at most times Pacman will avoid normal ghosts due to other factors. But if those ghosts come too close that's too dangerous. More details below.


    foodDistances = []
    foodCount = 0                                                       #counter for how many foods remain
    for food in foodList:
        foodCount += 1                                                  #increase counter by 1
        foodDistances.append(abs(food[0] - x) + abs(food[1] - y))       #calculate distances between Pacman and food dots
    
    
    
    score += foodsMultiplier * foodCount                                #the more food remaining the more points will be substracted from the evaluation score

    closestFood = min(foodDistances)
    
    
    score += closestFoodMultiplier * closestFood                        #the furthest the closest food is the more points will be substracted from the evaluation score

    normalGhosts = []
    scaredGhosts = []
    normalGhostDistances = []
    scaredGhostDistances = []
    for ghost in ghostStates:
        ghostx, ghosty = ghost.getPosition()
        if newScaredTimes == 0:
            normalGhosts.append(ghost)
            normalGhostDistances.append(abs(int(ghostx) - x) + abs(int(ghosty) - y))        #calculate distances between Pacman and normal ghosts
        else:
            scaredGhosts.append(ghost)
            scaredGhostDistances.append(abs(int(ghostx) - x) + abs(int(ghosty) - y))        #calculate distances between Pacman and scared ghosts


    closestScaredGhost = 0
    if len(scaredGhostDistances) != 0:
        closestScaredGhost = min(scaredGhostDistances)

    score += closestScaredGhostMultiplier * closestScaredGhost             #the furthest the scared ghost is the more points will be substracted from the evaluation score (REMEMBER! PACMAN SHOULD CHASE THOSE GHOSTS)


    closestNormalGhost = 0
    if len(normalGhostDistances) != 0:
        closestNormalGhost = min(normalGhostDistances)                              #Pacman must avoid normal ghosts cause they're gonna eat him, the closest normal ghost is the most important

    if closestNormalGhost < 2:                                                      #so I do a check for the closest one, if that ghost is too close it's really bad
        score -= 100000                                                             #and I remove many many points cause Pacman must avoid it immediately
    
    if closestFood < closestNormalGhost:                                    #if the closest food is closer to Pacman than the closest ghost is, that's good and Pacman must prefer to try and go to eat that dot
        score += 1
        if foodCount == 1:
            score += 1

    score += closestNormalGhost                                             #add also to the evaluation score the distance of the closest normal ghost so that the further it is the better the state is 

    return score
    util.raiseNotDefined()
# Abbreviation
better = betterEvaluationFunction
