from __future__ import annotations
from collections import defaultdict
import sys
import math

lines = open(sys.argv[1]).read().split('\n')

HEIGHT = len(lines)
WIDTH = len(lines[0])

NUM_WRAP = math.lcm(HEIGHT - 2, WIDTH - 2)

G = defaultdict(list)

for r, line in enumerate(lines):
    for c, char in enumerate(line):
        if r == 0 or c == 0 or r == HEIGHT - 1 or c == WIDTH - 1:
            continue
        if char != '.':
            G[(r, c)].append(char)
        
def printGrid(G, curPos=None):
    for y in range(HEIGHT):
        for x in range(WIDTH):
            if (y, x) == curPos:
                print('E', end='')
                continue
            if (y,x) != (0, 1) and (y,x) != (HEIGHT-1, WIDTH-2) and (y == 0 or x == 0 or y == HEIGHT - 1 or x == WIDTH - 1):
                print('#', end='')
                continue
            if (y, x) in G:
                if len(G[(y, x)]) > 1:
                    print(str(len(G[(y, x)])), end='')
                elif len(G[(y, x)]) == 1:
                    print(G[(y, x)][0], end='')
            else:
                print('.', end='')
        print('')


mv = {
    '^': (-1, 0),
    '>': (0, 1),
    '<': (0, -1),
    'v': (1, 0)
}

def add(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])

def wrapRow(x):
    if x == 0:
        return WIDTH - 2
    elif x == WIDTH - 1:
        return 1
    else:
        return x
    
def wrapColumn(y):
    if y == 0:
        return HEIGHT - 2
    elif y == HEIGHT- 1:
        return 1
    else:
        return y

def iterateGrid(G):
    G : defaultdict(list)
    G2 = defaultdict(list)
    # Just move everything to the next position
    for pos, blizzards in G.items():
        for b in blizzards:
            ny, nx = add(pos, mv[b])
            ny = wrapColumn(ny)
            nx = wrapRow(nx)
            G2[(ny, nx)].append(b)
    
    return G2

START_POSITION = (0, 1)
END_POSITION = (HEIGHT-1, WIDTH-2)

# Next step: Dijkstra, state can just be the current position and the round number % least_common_multiple(WIDTH, HEIGHT) since the rounds repeat after that

allMoves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Gets the current position and the grid for the next round, moves if the cell is empty
def findPossibleMoves(curState, G, endPos):
    states = []
    curPos, round = curState
    # First idea, do nothing if possible and if we are not in the start position (we assume we can move in the first round...)
    if curPos not in G:
        states.append((curPos, (round+1)))
    
    # Try moves in all directions
    for m in allMoves:
        newPos = add(curPos, m)
        r, c = newPos
        # Skip wall positions
        if newPos != endPos and (r <= 0 or c <= 0 or r >= HEIGHT - 1 or c >= WIDTH - 1):
            continue
        if newPos not in G:
            states.append((newPos, (round+1)))

    return states

def dist(t1, t2):
    return abs(t1[0]-t2[0]) + abs(t1[1]-t2[1])





GRID_CACHE = dict()
GRID_CACHE[0] = G

def search(initialState, endPos):
    Q = [initialState]
    visited = set()
    bestState = None

    while Q:
        state = Q.pop(0)
        
        pos, round = state
        modRound = round % NUM_WRAP
        
        if pos == endPos:
            bestState = state
            break
        
        G = GRID_CACHE[modRound]
        

        # We cache the grid because it repeats after a few rounds
        if modRound+1 in GRID_CACHE:
            G = GRID_CACHE[modRound+1]
        else:    
            G = iterateGrid(GRID_CACHE[modRound])
            GRID_CACHE[modRound+1] = G

        # print('\nNew grid for minute', round+1)
        # printGrid(G)
        newStates = findPossibleMoves(state, G, endPos)
        
            
        for ns in newStates:
            if not ns in visited:
                #print('Queuing state', ns, 'from', state)
                visited.add(ns)

                # Just don't have any priority right now
                Q.append(ns)
    return bestState


# Part 1
initialState = (START_POSITION, 0)
firstGoal = search(initialState, END_POSITION)
print(firstGoal[1])

# Part 2
secondStart = search(firstGoal, START_POSITION)
lastGoal = search(secondStart, END_POSITION)
print(lastGoal[1])