import sys
import math

input = [c for c in open(sys.argv[1]).read()]


rocks = []

rocks.append({(0, 0), (0, 1), (0, 2), (0, 3)})
rocks.append({(0, 1), (1, 0), (1, 1), (1, 2), (2, 1)})
rocks.append({(0, 0), (0, 1), (0, 2), (1, 2), (2, 2)})
rocks.append({(0, 0), (1, 0), (2, 0), (3, 0)})
rocks.append({(0, 0), (0, 1), (1, 0), (1, 1)})



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

cm = math.lcm(len(rocks), len(input))

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


def merge(S, lowerLeft, R):
    s = set(S)
    for c in R:
        cc = add(lowerLeft, c)
        s.add(cc)
    return s



# Idea: Additional height only depends on the last four rows

CACHE = dict()

def numInLastFourRows(BLOCKED, curHeight):
    num = 0
    S = set()
    for y in range(curHeight - 50, curHeight):
        for x in range(0, 7):
            if (y, x) in BLOCKED:
                num += 1
                S.add((y-curHeight+50, x))
    
    return sorted(S)

def signature(R):
    maxY = max([y for (y,x) in R])
    return frozenset([(maxY-y,x) for (y, x) in R if maxY-y<=30])



def simulate(numRocks):

    CACHE = dict()
    BLOCKED = set()
    
    jetIdx = 0
    i = 0
    curHeight = 0
    
    added = 0
    
    while i < numRocks:
        rIndex = i % len(rocks)
        R = rocks[rIndex]
        
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
                for c in R:
                    cc = add(lowerLeft, c)
                    curHeight = max([curHeight, cc[0] + 1])
                    BLOCKED.add(cc)
                break
            
            ci = checkIntersection(newLowerLeft, BLOCKED, R)
            
            if ci:
                lowerLeft = newLowerLeft
                
                #print('Falling one unit to ', lowerLeft)
                #printGrid(merge(BLOCKED, lowerLeft, R), 7, curHeight + 7)

            else:
                for c in R:
                    cc = add(lowerLeft, c)
                    curHeight = max([curHeight, cc[0] + 1])
                    BLOCKED.add(cc)
                    
                key = (jetIdx % len(input), rIndex, signature(BLOCKED))
                if key in CACHE:
                    #print('Found in cache', key)
                    oldIteration, oldHeight = CACHE[key]
                    heightDiff = curHeight - oldHeight
                    timeDiff = i - oldIteration

                    # Compute how often we can repeat the current cycle while still keeping under the limit
                    amt = (numRocks-i) // timeDiff
                    added += amt*heightDiff
                    i += amt*timeDiff
                CACHE[key] = (i, curHeight)
                break
        #printGrid(BLOCKED, 7, curHeight + 3)
        #print('\n====\n')
        i += 1  
    return curHeight+added


print(simulate(2022))
print(simulate(1000000000000))

