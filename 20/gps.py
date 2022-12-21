from __future__ import annotations
import sys

numbers = [int(l) for l in open(sys.argv[1]).read().split('\n')]

class Node:
    
    def __init__(self, steps, prev) -> None:
        self.steps = steps
        self.prev = prev
        self.next = None
        self.visited = False
    
    def __repr__(self) -> str:
        return str(self.steps)
    
    def walkForward(self):
        return self.next
    
    def walkBack(self):
        return self.prev
    
    def remove(self):
        self.prev.next = self.next
        self.next.prev = self.prev
        #print('Removed', self, self.prev.next, self.next.prev)

        self.next = None
        self.prev = None
        return self
    
    def insertAfter(self, node):
        node.prev = self
        node.next = self.next
        self.next.prev = node
        self.next = node




def printList(head: Node):
    curNode = head
    lst = []
    #print('Printing list, head = ', head)
    while True:
        lst.append(curNode.steps)
        assert len(lst) <= len(numbers)
        curNode = curNode.walkForward()
        #print('Walking forward, new node: ', curNode)
        if curNode == head:
            #print('Back at head', curNode)
            break

    print(' '.join(map(str, lst)))
    
def listLen(head):
    curNode = head
    numNodes = 0
    #print('Printing list, head = ', head)
    while True:
        numNodes += 1
        curNode = curNode.walkForward()
        #print('Walking forward, new node: ', curNode)
        if curNode == head:
            #print('Back at head', curNode)
            break

    return numNodes

numLen = len(numbers)
def mix(allNodes):
    for curNode in allNodes:
        # print('\n=====\n')
        #print('Visiting', curNode, listLen(curNode))
        # printList(curNode.prev)
    
        
        # Not visited, move the amount of steps defined in it
        numSteps = abs(curNode.steps) % (numLen - 1)
        
        
        if numSteps != 0:
            oldPrev, oldNext = curNode.prev, curNode.next
            curNode.remove()
            targetNode = None
            
            if curNode.steps < 0:
                targetNode = oldPrev
                for i in range(numSteps):
                    targetNode = targetNode.walkBack()
                    
            if curNode.steps > 0:
                targetNode = oldNext
                for i in range(numSteps - 1):
                    targetNode = targetNode.walkForward()
            
            #print(curNode, 'moves between', targetNode, 'and', targetNode.next)

            #print('After remove')
            #printList(targetNode)
            targetNode.insertAfter(curNode)
            #print('After insert')
            #printList(head)
        #else:
            #print('Doing nothing, steps = 0', curNode.prev, curNode.next)
    

prev = None
head = Node(numbers[0], None)

prev = head

# Keeps the original order of the nodes
allNodes = [head]

for n in numbers[1:]:
    node = Node(n, prev)
    prev.next = node
    prev = node
    allNodes.append(node)

head.prev = prev
prev.next = head

for n in allNodes:
    n.steps = 811589153 * n.steps

for _ in range(10):
    mix(allNodes)

zero = [n for n in allNodes if n.steps == 0]
curNode = zero[0]
total = 0
for i in range(1, 3001):
    curNode = curNode.walkForward()
    if i % 1000 == 0:
        total += curNode.steps

print(total)

    
    
    
    