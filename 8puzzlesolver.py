#random imported to generate puzzle
import random
#numpy handles n-d arrays better than standard python
import numpy as np
#import puzzle class
from puzzle import Puzzle
#import queue wrappers
from QueueWrappers import Queue, Stack, PriorityQueue
#priority queue
#from queue import PriorityQueue
#8puzzle solver
#must implement and compare the following algorithms:
#DFS, UCS, BFS, A*

#goal puzzle
goal = np.array([[1,2,3],
                 [8,0,4],
                 [7,6,5]])
test = np.array([[0,1,3],
                 [8,2,4],
                 [7,6,5]])

#initializes the puzzle
def initPuzzle():
        #initial puzzle object:
        puzzleValues = np.zeros((3,3), dtype=int)
        #list of numbers to be used:
        openNumbers = [0,1,2,3,4,5,6,7,8]
        #for each tile in the puzzle:
        #get a random number from the open numbers list
        #remove that number from the list
        for i in range(0,3):
                for j in range(0,3):
                        value = random.choice(openNumbers)
                        puzzleValues[i][j] = value
                        openNumbers.remove(value)
        #return the puzzle
        puzzle = Puzzle(puzzleValues)
        return puzzle



def depthFirstSearch(puzzle):
        #create a stack
        stack = Stack()
        #create visited set
        visited = []
        #add root to stack
        stack.push(puzzle)
        #while stack is not empty
        while stack:
                print(len(stack))
                #pop the stack
                p = stack.pop()
                #if is goal return
                if np.array_equal(p.puzzle, goal):
                        print("node found!")
                        printPath(p)
                        return

                #if unvisited, add all child nodes to the stack

                if not isVisited(p, visited):
                        visited.append(p)
                        children = p.generateAdjacentNodes()
                        for c in children:
                                        c.parent = p
                                        stack.push(c)

                

def breadthFirstSearch(puzzle):
        #create queue
        queue = Queue()
        #create list of visited nodes
        visited = []
        #start at root node
        #label root as explored
        visited.append(puzzle)
        #add root to queue
        queue.push(puzzle)
        #while queue is not empty:
        
        while queue:
                #pop the queue
                p = queue.pop()
                #if is goal return
                if np.array_equal(p.puzzle, goal):
                        print("node found!")
                        print("path from goal:")
                        printPath(p)
                        return
                #else, for all adjacent nodes
                children = p.generateAdjacentNodes()
                for c in children:
                        #if not explored
                        #label as explored 
                        #add the parent
                        # and add to queue
                        if not isVisited(c, visited):
                                visited.append(c)
                                c.parent = p
                                queue.push(c)
        print("Node not found")



# UCS or Djikstra's for Large Graphs
#inserts nodes as they are discovered rather than the entire graph initially
#this means the algorithm can be performed on large or infinite graphs
#in this implementation the "cost" of a node is its depth
#however the implementation would work on a different cost function

def uniformCostSearch(puzzle):
        
        #create a priority queue and a visited list
        #add the puzzle to the priority queue
        # while queue not empty
        #pop the queue
        #add node to visited
        # if is goal, return
        # if node NOT visited or in queue, add to queue
        # elif node in queue, update cost
        depth = 0
        queue = PriorityQueue()
        queue.push(puzzle, depth)
        visited = []
        while queue:
                p = queue.pop()






#A* algorithm
#heuristic: nilsson's sequence score

#def aStar():
#simple helper function for determining if a puzzle is in a list of puzzles 
def isVisited(node, list):
        #iterate through the array
        #if a puzzle node matches, return true
        #return false after iteration
        for i in list:
                if np.array_equal(node.puzzle, i.puzzle):
                        return True
        return False

def buildPath(previous, current):
        path = Queue()
        path.push(current)
        while current in previous:
                current = previous[current]
                path.push(current)
        return path



def printPath(puzzle):
        if puzzle is not None:
                puzzle.print()
                printPath(puzzle.parent)


def main():
        puzzle1 = Puzzle(test)
        #puzzle1 = initPuzzle()
        print("Initial Puzzle:")
        puzzle1.print()
        uniformCostSearch(puzzle1)
        
        

if __name__=="__main__":
        main()


