from __future__ import annotations
from collections import defaultdict
import sys

grid = [[c for c in l] for l in open(sys.argv[1]).read().split('\n')]

directions = ['N', 'S', 'W', 'E']

mv = {
    'N': [(-1, -1), (-1, 0), (-1, 1)],
    'S': [(1, -1), (1, 0), (1, 1)],
    'W': [(-1, -1), (0, -1), (1, -1)],
    'E': [(-1, 1), (0, 1), (1, 1)]
}

allMoves = list(set([m for _, moves in mv.items() for m in moves]))

def add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def boundingBox(G):
    min_x = 10e9
    max_x = -10e9
    min_y = 10e9
    max_y = -10e9
    
    for (y, x) in G:
        min_x = min(min_x, x)
        min_y = min(min_y, y)
        max_x = max(max_x, x)
        max_y = max(max_y, y)
    return ((min_y, max_y), (min_x, max_x))

def printGrid(G):
    ((min_y, max_y), (min_x, max_x)) = boundingBox(G)
    
    for y in range(min_y, max_y+1):
        for x in range(min_x, max_x+1):
            if (y, x) in G:
                print('#', end='')
            else:
                print('.', end='')
        print('')

class Elf:
    
    def __init__(self, position):
        self.position = position
        
    def __repr__(self):
        return str(self.position)
    
    def propose(self, G, round):
        noNeighbors = True
        for m in allMoves:
            pos = add(self.position, m)
            if pos in G:
                noNeighbors = False
                break
        
        if noNeighbors:
            return None, None
        
        for offset in range(4):
            dirIdx = (round + offset) % 4
            direction = directions[dirIdx]
            
            neighbors = mv[direction]
            canMove = True
            for n in neighbors:
                pos = add(self.position, n)
                if pos in G:
                    canMove = False
                    break
            
            if canMove:
                # The straight step into the direction is always at the second position
                # of the movement table
                return add(self.position, neighbors[1]), direction
        return None, None
            
                
        
elves = []

# Is always updated with the elf positions
G = set()

for r, line in enumerate(grid):
    for c, cell in enumerate(line):
        if cell == '#':
            elves.append(Elf((r, c)))
            G.add((r, c))
            
hadMoves = True

i = 0
while hadMoves:
    if i == 10:
        ((y_min, y_max), (x_min, x_max)) = boundingBox(G)
        print((y_max-y_min+1)*(x_max-x_min+1)-len(elves))

    hadMoves = False
    proposals = defaultdict(lambda: [])
    
    e : Elf
    for e in elves:
        newPos, direction = e.propose(G, i)
        if newPos != None:
            proposals[newPos].append(e)
            #print(e, '->', newPos)
        
    # Second phase, iterate over all proposals and only move the elves that have a unique destination
    for target, movingElves in proposals.items():
        if len(movingElves) == 1:
            #print(target)
            movingElves[0].position = target
            hadMoves = True
         
    G2 = set()
    for e in elves:
        #print('Adding', e.position)
        G2.add(e.position)
        
    
    G = G2
    i += 1

print(i)
