#random imported to generate puzzle
import random
#numpy handles n-d arrays better than standard python
import numpy as np
#import puzzle class
from puzzle import Puzzle
#import queue wrappers
from QueueWrappers import Queue, Stack, PriorityQueue
#import time for timing
import time
#8puzzle solver
#must implement and compare the following algorithms:
#DFS, UCS, BFS, A* with Nilssson's score

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


#simple dfs implementation
def depthFirstSearch(puzzle, goal):

        #create a stack
        stack = Stack()
        #create visited set
        visited = set()
        #dict of previous nodes
        previous = {}
        #add root to stack
        stack.push(puzzle)
        #while stack is not empty
        while stack:
                #pop the stack
                p = stack.pop()
                #if goal return
                if p == goal:
                        print("node found!")
                        return len(visited)

                #add p to visited
                #then generate adjacent nodes
                #and for each unvisited child
                #add that child to the stack
                visited.add(p)
                children = p.generateAdjacentNodes()
                for c in children:
                        if c not in visited:
                                previous[c] = p
                                stack.push(c)
        print("Node not found")
        return len(visited)

                
#simple bfs implementation
def breadthFirstSearch(puzzle, goal):

        #create queue
        queue = Queue()
        #create set of visited nodes
        visited = set()
        #dict of previous nodes
        previous = {}
        #start at root node
        #label root as explored
        visited.add(puzzle)
        #add root to queue
        queue.push(puzzle)
        #while queue is not empty:
        
        while queue:
                #pop the queue
                p = queue.pop()
                #if goal return
                if p == goal:
                        print("node found!")
                        return len(visited)
                #else, for all adjacent nodes
                children = p.generateAdjacentNodes()
                for c in children:
                        #if not explored
                        #label as explored 
                        #add the parent
                        # and add to queue
                        if c not in visited:
                                visited.add(c)
                                previous[c] = p
                                queue.push(c)
        print("Node not found")
        return len(visited)



# UCS or Dijkstra's for Large Graphs
#inserts nodes as they are discovered rather than the entire graph initially
#this means the algorithm can be performed on large or infinite graphs
#in this implementation the "cost" of a node is its depth
#however the implementation would work on a different cost function
#this means UCS can be modified for A*
def uniformCostSearch(puzzle, goal):
        
        #create a priority queue and a visited list
        #add the puzzle to the priority queue
        # while queue not empty
        #pop the queue
        # if is goal, return, else
        #add node to visited
        #for each child
        # if node NOT visited or in queue, add to queue
        # elif node in queue, update cost

        queue = PriorityQueue()
        queue.push(puzzle, 0)
        visited = set()
        previous = {}
        #this dictionary tracks the costs of a given node g(n)
        costs = {}
        #add the initpuzzle to costs
        costs[puzzle] = 0

        #main search loop
        while queue:
                p = queue.pop()
                #if goal return
                if p == goal:
                        print("node found!")
                        return len(visited)
                #else add to visited and generate children
                visited.add(p)
                children = p.generateAdjacentNodes()
                #set node cost to depth
                #the depth of the node is simply the depth of the parent + 1
                for c in children:
                        cost = costs[p] + 1
                        if c not in visited and c not in costs:
                                costs[c] = cost
                                queue.push(c, cost)
                                previous[c] = p
                        #update cost if needed
                        elif c in costs and costs.get(c) > cost:
                                costs[c] = cost
                                previous[c] = p
                                queue.push(c, cost)
        print("Node not found")
        return len(visited)







#A* algorithm
#heuristic: nilsson's sequence score
#This is effectively a modified Dijkstra's for Infinite Graphs, AKA Uniform Cost Search
#depth is still used for the g(n)
#and nilsson's sequence score is used for the h(n)
#f(n) is a combination of g(n) and h(n)
#we use two dictionaries to track f(n) and g(n)
#g(n) is the depth of the node and h(n) is the nilsson score applied to a node
def astar(puzzle, goal):
        #create queue and push
        queue = PriorityQueue()
        #initial depth is 0 so just calculate nilsson score
        initFcost = puzzle.getNilssonScore(goal)
        queue.push(puzzle, initFcost)
        visited = set()
        #previous dictionary to track node neighbors
        previous = {}
        #this dictionary tracks the costs of a given node f(n)
        gCosts = {}
        fCosts = {}
        #add puzzle to gcosts and fcosts
        gCosts[puzzle] = 0
        fCosts[puzzle] = initFcost


        #main search loop
        while queue:
                #print(len(queue))
                p = queue.pop()
                #if goal return
                if p == goal:
                        print("node found!")
                        return len(visited)
                #else add to visited and generate children
                visited.add(p)
                children = p.generateAdjacentNodes()
                for c in children:
                        #calculate node cost
                        gCost = gCosts[p] + 1
                        hCost = c.getNilssonScore(goal)
                        fCost = gCost + hCost
                        #check if node not visited and not in queue. a node in fcosts but not visited is in the queue
                        if c not in visited and c not in fCosts:
                                #add node to gCosts and fCosts
                                #and push to queue
                                fCosts[c] = fCost
                                gCosts[c] = gCost
                                queue.push(c, fCost)
                                previous[c] = p
                        #update cost if needed
                        elif c in fCosts and fCosts.get(c) > fCost:
                                fCosts[c] = fCost
                                gCosts[c] = gCost
                                previous[c] = p
                                queue.push(c, fCost)
        print("Node not found")
        return len(visited)

#best first search implementation
#effectively a modified UCS method where the node cost is h(n)
#h(n) in this implementation is the node's nilsson score
#because h(n) is always the same for a node, tracking the cost is not needed
def bestFirstSearch(puzzle, goal):
        
        queue = PriorityQueue()
        initcost = puzzle.getNilssonScore(goal)
        queue.push(puzzle, initcost)
        visited = set()
        previous = {}

        #main search loop
        while queue:
                p = queue.pop()
                #if goal return
                if p == goal:
                        print("node found!")
                        return len(visited)
                #else add to visited and generate children
                visited.add(p)
                children = p.generateAdjacentNodes()
                for c in children:
                        #set node cost
                        cost = c.getNilssonScore(goal)
                        #if unvisited add to queue
                        if c not in visited:
                                queue.push(c, cost)
                                previous[c] = p
        print("Node not found")
        return len(visited)


#returns a path to the current node using a dictionary of previous nodes
def buildPath(previous, current):
        path = Stack()
        path.push(current)
        while current in previous:
                current = previous[current]
                path.push(current)
        return path

#helper function determines if a function is solvable
#if the number of swaps needed to solve a puzzle is even, then the puzzle is solvable
#2 tiles form a swap if the order is incorrect for the goal state. The blank space is not counted in swap pairs
def isSolvable(puzzle):
        #map of the goal values to a standard 8-puzzle
        #this is hardcoded and would need to be changed to support different goal states
        valueMap = {
                0:0,
                1:1,
                2:2,
                3:3,
                8:4,
                4:5,
                7:6,
                6:7,
                5:8
        }
        

        #iterate through array, and map values

        #flatten and convert to list
        plist = puzzle.flatten().tolist()
        #iterate and map values
        puzzle = np.array(list(map(valueMap.get, plist)))



        #check if solvable
        iters = 0
        for i in range(9):
                for j in range(i+1, 9):
                        if puzzle[j] != 0 and puzzle[i]!= 0 and puzzle[i] > puzzle[j]:
                                iters+=1
        return(iters % 2 == 0)
                        

def main():
        #perform BFS, DFS, UCS, AStar, best-first search x times
        #and find: the average completion time per algorithm, and average nodes traversed

        #goal puzzle
        goalValues = np.array([[1,2,3],[8,0,4],[7,6,5]])
        goal = Puzzle(goalValues)
        goal.createSuccessors()

        #puzzle list
        puzzles = []

        bfsAverageTime = 0
        dfsAverageTime = 0
        ucsAverageTime = 0
        astarAverageTime = 0
        bestFirstAverageTime = 0

        bfsAverageNodes = 0
        dfsAverageNodes = 0
        ucsAverageNodes = 0
        astarAverageNodes = 0
        bestFirstAverageNodes = 0

        #limit to the run
        runLimit = 20
        #perform runs
        for x in range(runLimit):
                puzzle = initPuzzle()
                while not isSolvable(puzzle.puzzle):
                        puzzle = initPuzzle()
                puzzles.append(puzzle)
        for x in range(runLimit):

                print(f"iteration: {x+1}")
                puzzle = puzzles[x]
                print(puzzle)

                #bfs run
                tic = time.perf_counter()
                nodeCount = breadthFirstSearch(puzzle, goal)
                toc = time.perf_counter()
                print(f"Breadth First Search Completed in: {toc-tic:0.4f} seconds")
                print(f"nodes visited: {nodeCount}")
                bfsAverageTime += (toc-tic)
                bfsAverageNodes += nodeCount

                #dfs run
                tic = time.perf_counter()
                nodeCount = depthFirstSearch(puzzle, goal)
                toc = time.perf_counter()
                print(f"Depth First Search Completed in: {toc-tic:0.4f} seconds")
                print(f"nodes visited: {nodeCount}")
                dfsAverageTime += (toc-tic)
                dfsAverageNodes += nodeCount

                #ucs run
                tic = time.perf_counter()
                nodeCount = uniformCostSearch(puzzle, goal)
                toc = time.perf_counter()
                print(f"Uniform Cost Search Completed in: {toc-tic:0.4f} seconds")
                print(f"nodes visited: {nodeCount}")
                ucsAverageTime += (toc-tic)
                ucsAverageNodes += nodeCount

                #A* run
                tic = time.perf_counter()
                nodeCount = astar(puzzle, goal)
                toc = time.perf_counter()
                print(f"A* Search Completed in: {toc-tic:0.4f} seconds")
                print(f"nodes visited: {nodeCount}")
                astarAverageTime += (toc-tic)
                astarAverageNodes += nodeCount

                #best first run
                tic = time.perf_counter()
                nodeCount = bestFirstSearch(puzzle, goal)
                toc = time.perf_counter()
                print(f"Best-First Search Completed in: {toc-tic:0.4f} seconds")
                print(f"nodes visited: {nodeCount}")
                bestFirstAverageTime += (toc-tic)
                bestFirstAverageNodes += nodeCount
        
        #calculate and display averages:
        bfsAverageTime /= runLimit
        bfsAverageNodes /= runLimit
        dfsAverageTime /= runLimit
        dfsAverageNodes /= runLimit
        ucsAverageTime /= runLimit
        ucsAverageNodes /= runLimit
        astarAverageTime /= runLimit
        astarAverageNodes /= runLimit
        bestFirstAverageTime /= runLimit
        bestFirstAverageNodes /= runLimit
        
        print(f"Total runs:{runLimit}")

        print(f"Average BFS search time: {bfsAverageTime:0.4f} seconds")
        print(f"Average BFS nodes visited: {bfsAverageNodes}")

        print(f"Average DFS search time: {dfsAverageTime:0.4f} seconds")
        print(f"Average DFS nodes visited: {dfsAverageNodes}")

        print(f"Average UCS search time: {ucsAverageTime:0.4f} seconds")
        print(f"Average UCS nodes visited: {ucsAverageNodes}")

        print(f"Average A* search time: {astarAverageTime:0.4f} seconds")
        print(f"Average A* nodes visited: {astarAverageNodes}")

        print(f"Average best-first search time: {bestFirstAverageTime:0.4f} seconds")
        print(f"Average best-first nodes visited: {bestFirstAverageNodes}")
     
#NEED: Timer, nodes traversed, find averages for 10 puzzles for each search
if __name__=="__main__":
        main()


