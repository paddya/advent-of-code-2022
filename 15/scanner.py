import sys
import re
from intervaltree import *

pattern = re.compile(r'^Sensor at x=(-?\d+), y=(-?\d+): closest beacon is at x=(-?\d+), y=(-?\d+)')

def distance(p1, p2):
    return abs(p1[0]-p2[0]) + abs(p1[1]-p2[1])

class Scanner:
    
    def __init__(self, x, y, bx, by) -> None:
        self.scanner = (x, y)
        self.distance = distance(self.scanner, (bx,by))
        
def buildScanner(line):
    match = pattern.fullmatch(line)
    
    return Scanner(int(match.group(1)), int(match.group(2)), int(match.group(3)), int(match.group(4)))



scanners = [buildScanner(l) for l in open(sys.argv[1]).read().split('\n')]

targetY = int(sys.argv[2])

boundX = int(sys.argv[3])
boundY = int(sys.argv[4])

def add(t1, t2):
    return (t1[0]+t2[0], t1[1]+t2[1])


def fasterSearch(targetY):
    x = 0
    while x <= boundX:
        found = False
        for s in scanners:
            dst = distance(s.scanner, (x, targetY))
            if dst < s.distance:
                dx = s.distance - abs(s.scanner[1] - targetY)
                x = s.scanner[0] + dx + 1
                found = True
                break
        if not found:
            return x
        
    return None
        
for y in range(boundY, -1, -1):
    x = fasterSearch(y)
    if x != None:
        print(4000000*x+y)
        break
        
                

def searchAt(targetY):
    T = IntervalTree()

    for s in scanners:
        closestPoint = (s.scanner[0], targetY)
        dst = distance(s.scanner, closestPoint)
        
        remaining = s.distance-dst
        
        if remaining >= 0:
            rmin = max(0, closestPoint[0]-remaining)
            rmax = min(closestPoint[0]+remaining, boundX)
            T.add(Interval(rmin, rmax+1))
                    
    # for s in scanners:
    #     if s.beacon[1] == targetY:
    #         T.chop(s.beacon[0]-1, s.beacon[0])
    T.merge_overlaps()
    T.merge_neighbors(distance=0)
    total = 0
    ivs = sorted([t for t in T])
    for l in T:
        total += l.end - l.begin
    return total, ivs[0].end

# for y in range(boundY):
#     if y % 10000 == 0:
#         print(y)
#     num, x = searchAt(y)
#     if num < boundX+1:
#         print(4000000*x+y)
#         break
        