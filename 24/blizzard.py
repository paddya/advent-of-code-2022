from __future__ import annotations
from collections import defaultdict, deque
import sys

lines = open(sys.argv[1]).read().split('\n')

HEIGHT = len(lines)
WIDTH = len(lines[0])

# Store horizontal and vertical blizzards in separate sets
# because each axis repeats faster than the whole grid 
# which takes LCM(WIDTH-2, HEIGHT-2) iterations
GX = defaultdict(list)
GY = defaultdict(list)

for r, line in enumerate(lines):
    for c, char in enumerate(line):
        if r == 0 or c == 0 or r == HEIGHT - 1 or c == WIDTH - 1:
            continue
        if char != '.':
            if char == '>' or char == '<':
                GX[(r, c)].append(char)
            else:
                GY[(r, c)].append(char)
                    
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


allMoves = [(-1, 0), (1, 0), (0, -1), (0, 1)]

# Computes all possible moves from a given state and
# future grid
def findPossibleMoves(curState, GX, GY, endPos):
    states = []
    curPos, round = curState
    # Do nothing if there is no blizzard in the current spot in the next round
    if curPos not in GX and curPos not in GY:
        states.append((curPos, (round+1)))
    
    # Try moves in all directions
    for m in allMoves:
        newPos = add(curPos, m)
        r, c = newPos
        # Skip wall positions
        if newPos != endPos and (r <= 0 or c <= 0 or r >= HEIGHT - 1 or c >= WIDTH - 1):
            continue
        if newPos not in GX and newPos not in GY:
            states.append((newPos, (round+1)))

    return states

def dist(t1, t2):
    return abs(t1[0]-t2[0]) + abs(t1[1]-t2[1])


GRID_CACHE_X = dict()
GRID_CACHE_X[0] = GX

GRID_CACHE_Y = dict()
GRID_CACHE_Y[0] = GY

# Implements a breadth-first search over the state space
def search(initialState, endPos):
    Q = deque([initialState])
    visited = set()
    bestState = None

    while Q:
        pos, round = state = Q.popleft()   

        if pos == endPos:
            bestState = state
            break

        # Compute the current grid state by either looking it up
        # from the cache or by iterating the grid from the last round
        roundX = round % (WIDTH - 2)
        roundY = round % (HEIGHT -2)
        
        GX = GRID_CACHE_X[roundX]
        GY = GRID_CACHE_Y[roundY]

        if roundX+1 in GRID_CACHE_X:
            GX = GRID_CACHE_X[roundX+1]
        else:    
            GX = iterateGrid(GRID_CACHE_X[roundX])
            GRID_CACHE_X[roundX+1] = GX
            
        if roundY+1 in GRID_CACHE_Y:
            GY = GRID_CACHE_Y[roundY+1]
        else:    
            GY = iterateGrid(GRID_CACHE_Y[roundY])
            GRID_CACHE_Y[roundY+1] = GY


        newStates = findPossibleMoves(state, GX, GY, endPos)
                    
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