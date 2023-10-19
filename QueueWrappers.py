#simple wrapper class for various queues
#this simplifies certain calls within algorithms
#and uses python's deque module, which is "list like" but supports fast insert and pop operations from either end
from collections import deque
from itertools import count

#heapq is used for the priority queue implementation
import heapq

#Simple FIFO queue wrapper
class Queue:
    #general class functions: constructor, length,and a function that allows the object to be iterable(allowing for loop traversal)
    def __init__(self):
        self.items = deque()

    def __len__(self):
        return len(self.items)
    
    def __iter__(self):
        while len(self) > 0:
            yield self.pop()
    #push and pop functions
    def push(self, item):
        self.items.append(item)
    def pop(self):
        return self.items.popleft()
    

#Simple LIFO stack wrapper
#extends queue
class Stack(Queue):
    def pop(self):
        return self.items.pop()
    
#Simple Priority Queue
class PriorityQueue:
    def __init__(self):
        self.entries = {}
        self.heap = []
        self.counter = count()

    def __len__(self):
        return len(self.heap)
    def __iter__(self):
        while len(self) > 0:
            return self.pop()
    #push and remove entry if needed
    def push(self,item, priority):
        if item in self.entries:
            self.remove(item)
        count = next(self.counter)
        entry = [priority, count, item]
        self.entries[item] = entry
        heapq.heappush(self.heap, entry)
    #mark entry as removed
    def remove(self,item):
        entry = self.entries.pop(item)
        entry[-1] = "REMOVED"
    #pop least priority non-removed entry
    def pop(self):
        while self.heap:
            priority,count,item = heapq.heappop(self.heap)
            if item is not "REMOVED":
                del self.entries[item]
                return item