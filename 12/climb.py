from collections import defaultdict
import sys

G = [[c for c in line] for line in open(sys.argv[1]).read().split('\n')]



H = len(G)
W = len(G[0])

def findCoords(G, target):
    for r in range(len(G)):
        for c in range(len(G[r])):
            if G[r][c] == target:
                return r, c
            
def mapChar(ch):
    if ch == 'S':
        return 0
    if ch == 'E':
        return ord('z') - ord('a')
    
    return ord(ch) - ord('a')
    
start = findCoords(G, 'S')
end = findCoords(G, 'E')

mv = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def add(tuple1, tuple2):
    return (tuple1[0] + tuple2[0], tuple1[1] + tuple2[1])

# Full disclosure: optimized after looking at /r/AdventOfCode
# We run the BFS from the highest point on the grid and stop once we
# reach a grid node that matches the value of "end"
# This dramatically speeds up Part 2 compared to the naive approach
# that computes the shortest path for each start node "a"
def downwardBfs(G, startCoords, end):
    
    D = defaultdict(int)

    D[startCoords] = 0
    
    queue = [startCoords]
    
    visited = set()
    visited.add(startCoords)

    while len(queue) > 0:
        current = queue.pop(0)
        cy, cx = current
        
        if G[cy][cx] == end:
            return D[current]
                
        cv = mapChar(G[cy][cx])
        
        for m in mv:
            neighbor = add(current, m)
            ny, nx = neighbor
            
            if not (0 <= ny < H and 0 <= nx < W):
                continue
            
            nv = mapChar(G[ny][nx])
            
            # In this implementation, we avoid stepping _down_ more than one
            # elevation unit at a time
            if nv < cv - 1:
                continue
            
            if not neighbor in visited:
                queue.append(neighbor)
                visited.add(neighbor)
                D[neighbor] = D[current] + 1
            
    return D[end]
    

print(downwardBfs(G, end, "S"))
print(downwardBfs(G, end, "a"))