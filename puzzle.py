#puzzle class wraps a puzzle and has various helper methods
#assigned to it
import random
import numpy as np

class Puzzle:
    #important class methods
    def __init__(self):
        self.puzzle = np.zeros((3,3), dtype=int)
        self.successors = {}
    def __init__(self, puzzle):
        self.puzzle = np.copy(puzzle)
        self.successors = {}
    #eq and hash functions that define the comparison and hashability of the object
    def __eq__(self, other):
        return np.array_equal(self.puzzle, other.puzzle)
    def __hash__(self):
        return hash(str(self.puzzle))
    #str value of the object for printing
    def __str__(self):
        return str(self.puzzle)
    #creates a dictionary of successor values for each position
    def createSuccessors(self):
        #top row
        self.successors[self.puzzle[0][0]] = self.puzzle[0][1]
        self.successors[self.puzzle[0][1]] = self.puzzle[0][2]
        #right side
        self.successors[self.puzzle[0][2]] = self.puzzle[1][2]
        self.successors[self.puzzle[1][2]] = self.puzzle[2][2]
        #bottom row
        self.successors[self.puzzle[2][2]] = self.puzzle[2][1]
        self.successors[self.puzzle[2][1]] = self.puzzle[2][0]
        #left side
        self.successors[self.puzzle[2][0]] = self.puzzle[1][0]
        self.successors[self.puzzle[1][0]] = self.puzzle[0][0]

    #determines nilsson score in relation to a given goal puzzle
    #h(n) = P(n) +3S(n)
    #P(n) is manhattan distance of each tile from proper position
    #S(n) is a sequence score given by: a tile in the center scores 1. Every other tile(except 0) that has a wrong clockwise
    #successor scores 2
    #add these scores together to get S(n)
    def getNilssonScore(self, goal):
        #create successors
        self.createSuccessors()
        total = 0
        #if a tile is in the center score 1
        if self.getTilePos(0) != (0,0):
            total += 1
        #for eachtile:
        #if successor is not valid than add 2
        for x in range(1,9):
            if self.successors.get(x) is not goal.successors.get(x):
                total += 2
        #multiply total by 3
        total *=3
        #add manhattan distance and return
        total += self.totalManhattanDistance(goal)
        return total

    #total manhattan distance compared to a goal
    def totalManhattanDistance(self, goal):
        total = 0
        for x in range(9):
            pos1 = goal.getTilePos(x)
            pos2 = self.getTilePos(x)
            total += self.tileManhattanDistance(pos1, pos2)
        return total
    def tileManhattanDistance(self, pos1, pos2):
        return (abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1]))

    #get tile position
    def getTilePos(self,value):
       it = np.nditer(self.puzzle, flags=['multi_index'])
       for x in it:
           if x == value:
               return it.multi_index
    #generate adjacent nodes
    def generateAdjacentNodes(self):
        adjacentPuzzles = []
        #get position of blank tile
        position = self.getTilePos(0)
        #print("My position is:", position)
        #evaluate and swap all available directions
        #generate a new puzzle based on the swap
        #add that puzzle to the list
        #if can left-move left
        if position[1] > 0:
            #print("can left")
            newPos = (position[0], position[1] - 1)
            newPuzzle = Puzzle(self.puzzle)
            newPuzzle.positionSwap(position, newPos)
            adjacentPuzzles.append(newPuzzle)
        
        #if can right- move right
        if position[1] < 2:
            #print("can right")
            #swap the tiles


            newPos = (position[0], position[1] + 1)
            
            newPuzzle = Puzzle(self.puzzle)
            newPuzzle.positionSwap(position, newPos)
            adjacentPuzzles.append(newPuzzle)

        #if can up- move up
        if position[0] > 0:
            #print("can up")
            #swap the tiles
            newPos = (position[0] - 1, position[1])
            newPuzzle = Puzzle(self.puzzle)
            newPuzzle.positionSwap(position, newPos)
            adjacentPuzzles.append(newPuzzle)
        
        #if can down- move down
        if position[0] < 2:
            #print("can down")
            newPos = (position[0] + 1, position[1])
            
            newPuzzle = Puzzle(self.puzzle)
            newPuzzle.positionSwap(position, newPos)
            adjacentPuzzles.append(newPuzzle)
        return adjacentPuzzles

    #positional swap method
    def positionSwap(self, pos1, pos2):
        #print("pos 1")
        #print(pos1)
        #print("pos 2:")
        #print(pos2)
        val1 = self.puzzle[pos1]
        #print("val1:")
        #print(val1)
        val2 = self.puzzle[pos2]
        #print("val2:")
        #print(val2)
        #print(val2)
        self.puzzle[pos1] = val2
        self.puzzle[pos2] = val1
    

    