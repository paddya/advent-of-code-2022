import sys

moves = [(words[0], int(words[1])) for words in [line.split(' ') for line in open(sys.argv[1]).read().split('\n')]]


DIR = {
    'D': (-1, 0),
    'U': (1, 0),
    'L': (0, -1),
    'R': (0, 1),
    'UL': (1, -1),
    'UR': (1, 1),
    'DL': (-1, -1),
    'DR': (-1, 1)
}

def isAdjacent(p1, p2):
    return abs(p1[0]-p2[0]) <= 1 and abs(p1[1]-p2[1]) <= 1

def hasOneCommonAxis(p1, p2):
    return p1[0] == p2[0] or p1[1] == p2[1]

def printVisited(visited):
    for y in range(-20, 20):
        for x in range(-20, 20):
            if (-y, x) in visited:
                print('#', end='')
            else:
                print('.', end='')
        print('')
        
def printKnots(knots):
    for y in range(-20, 20):
        for x in range(-20, 20):
            printed = False
            for i in range(len(knots)):
                if knots[i] == (-y, x):
                    print(str(i) if i != 0 else 'H', end='')
                    printed = True
                    break
            if not printed:
                if (y, x) == (0, 0):
                    print('s', end='')
                else:
                    print('.', end='')
        print('')


# Returns the jump direction required, depending on the position of reference and point   
def requiredJumpDirection(reference, point):
    ry, rx = reference
    py, px = point
    
    # Top right
    if ry > py and rx > px:
        return 'UR'
    # Top left
    elif ry > py and rx < px:
        return 'UL'
    # Bottom left
    elif ry < py and rx < px:
        return 'DL'
    # Bottom right
    elif ry < py and rx > px:
        return 'DR'
        
    # Above
    elif ry > py and rx == px:
        return 'U'
    # Below
    elif ry < py and rx == px:
        return 'D'
    # Left
    elif ry == py and rx < px:
        return 'L'
    # Right
    elif ry == py and rx > px:
        return 'R'
    

def runSimulation(numKnots):
    knots = [(0, 0)] * numKnots

    visited = set()
    visited.add((0, 0)) # Just to make sure the starting point is in the visited set
    
    for m in moves:
        direction, numSteps = m
        dy, dx = DIR[direction]
            
        for i in range(numSteps):
            knots[0] = (knots[0][0] + dy, knots[0][1] + dx)
            for knotIdx in range(1, numKnots):
                prevKnot = knots[knotIdx - 1]
                curKnot = knots[knotIdx]
                if not isAdjacent(prevKnot, curKnot):
                    reqDir = requiredJumpDirection(prevKnot, curKnot)

                    ddy, ddx = DIR[reqDir]
                    curKnot = (curKnot[0] + ddy, curKnot[1] + ddx)
                        

                    knots[knotIdx] = curKnot
                # else:
                #     print('Knot ' + str(knotIdx) + ' does not need to be moved, still adjacent: ', prevKnot, curKnot)
            visited.add(knots[numKnots - 1])

    print(len(visited))
    
runSimulation(2)
runSimulation(10)
