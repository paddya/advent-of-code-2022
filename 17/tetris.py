import sys

input = [c for c in open(sys.argv[1]).read()]

print(input)

rocks = []

rocks.append({(0, 0), (0, 1), (0, 2), (0, 3)})
rocks.append({(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)})
rocks.append({(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)})
rocks.append({(0, 0), (1, 0), (2, 0), (3, 0)})
rocks.append({(0, 0), (0, 1), (1, 0), (1, 1)})

BLOCKED = set()

def printGrid(S, w, h):
    for y in range(h-1, -1, -1):
        for x in range(w):
            if (y, x) in S:
                print('#', end='')
            else:
                print('.', end='')
        print('')

MIN = 0
MAX = 7

curHeight = 0

def add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

def checkBounds(lowerLeft, r):
    for c in r:
        cc = add(lowerLeft, c)
        if not (0 <= cc[1] < MAX):
            return False
    return True

def checkIntersection(lowerLeft, S, R):
    for c in R:
        cc = add(lowerLeft, c)
        if cc in S:
            return False
    
    return True

def addRock(lowerLeft, R):
    global curHeight
    for c in R:
        cc = add(lowerLeft, c)
        curHeight = max([curHeight, cc[0] + 1])
        BLOCKED.add(cc)

def merge(S, lowerLeft, R):
    s = set(S)
    for c in R:
        cc = add(lowerLeft, c)
        s.add(cc)
    return s

jetIdx = 0
i = 0
for i in range(2022):
    R = rocks[i % len(rocks)]
    
    i += 1
    
    if i % (len(rocks) * len(input)) == 0:
        print(i, curHeight)


    lowerLeft = (curHeight + 3, 2)
    #print('Starting at', lowerLeft)

    while True:
        direction = input[jetIdx % len(input)]
        
        newLowerLeft = lowerLeft
        dir = ''
        if direction == '<':
            dir = 'left'
            newLowerLeft = (lowerLeft[0], lowerLeft[1] - 1)
        elif direction == '>':
            dir = 'right'
            newLowerLeft = (lowerLeft[0], lowerLeft[1] + 1)
        
        cb = checkBounds(newLowerLeft, R)
        ci = checkIntersection(newLowerLeft, BLOCKED, R)
        if cb and ci:
            lowerLeft = newLowerLeft
            #print('Pushed', dir, 'to', lowerLeft)
        #else:
            #print('Push', dir, 'blocked')
            
        jetIdx += 1
        
        # printGrid(merge(BLOCKED, lowerLeft, R), 7, curHeight + 7)
        # print('\n====\n')
        
        newLowerLeft = (lowerLeft[0] - 1, lowerLeft[1])
        
        if newLowerLeft[0] < 0:
            #print('At the bottom, not falling further')
            addRock(lowerLeft, R)
            break
        
        ci = checkIntersection(newLowerLeft, BLOCKED, R)
        
        if ci:
            lowerLeft = newLowerLeft
            
            #print('Falling one unit to ', lowerLeft)
            #printGrid(merge(BLOCKED, lowerLeft, R), 7, curHeight + 7)

        else:
            #print(BLOCKED)
            #print('blocked at', lowerLeft)
            addRock(lowerLeft, R)
            break
    #printGrid(BLOCKED, 7, curHeight + 3)
    #print('\n====\n')
print(curHeight)

        
    