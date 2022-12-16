import copy
import sys

lines = [[[int(s) for s in k.split(',')] for k in l.split(' -> ')] for l in open(sys.argv[1]).read().split('\n')]


ENV = set()

maxY = 0

for l in lines:
    for idx in range(len(l) - 1):
        start, end = l[idx:idx+2]
        sx, sy = start
        ex, ey = end
        
        maxY = max([maxY, sy, ey])
        
        # If the x value changes, we'll keep y constant
        if sx < ex:
            for x in range(sx, ex+1):
                ENV.add((x, ey))
        elif sx > ex:
            for x in range(sx, ex-1, -1):
                ENV.add((x, ey))
        elif sy < ey:
            for y in range(sy, ey+1):
                ENV.add((ex, y))
        elif sy > ey:
            for y in range(sy, ey-1, -1):
                ENV.add((ex, y))


floorY = maxY + 2


mv = [(0, 1), (-1, 1), (1, 1)]

def add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1])

for p2 in [False, True]:
    numSandUnits = 0

    S = copy.copy(ENV)

    # Instead of always starting at (500, 0),
    # we can keep track of the current route of each sand unit
    # by pushing every location to the stack.
    # We then start with the next sand unit at the step prior
    # to the previous stop.
    stack = [(500, 0)]
    while (500, 0) not in S:
        prev = stack.pop()
        s = prev
        
        infinity = False
        while True:
            stack.append(s)

            hasMoved = False
            if not p2 and s[1] > maxY:
                infinity = True
                break
            # Determine movement
            for m in mv:
                ns = add(s, m)
                if ns not in S and (not p2 or ns[1] < floorY):
                    hasMoved = True
                    s = ns
                    break
            
            if not hasMoved:
                break
            

        if infinity:
            break
        S.add(s)
        # The stack should ways end with the location prior to the previous
        # stop, so we remove the element we just added again
        assert s == stack.pop()
        numSandUnits += 1
    
    print(numSandUnits)
    
    