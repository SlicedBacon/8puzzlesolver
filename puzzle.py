import random
import numpy as np

class Puzzle:

    def __init__(self):
        self.puzzle = np.zeros((3,3), dtype=int)
        self.parent = None
        self.depth = 0
        self.cost = 0
    def __init__(self, puzzle):
        self.puzzle = np.copy(puzzle)
        self.parent = None
        self.depth = 0
        self.cost = 0
    #helper print method          
    def print(self):
        print(self.puzzle)

    def getTilePos(self,value):
       it = np.nditer(self.puzzle, flags=['multi_index'])
       for x in it:
           if x == value:
               return it.multi_index
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
    

    