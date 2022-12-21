import sys

cubes = [tuple(map(int, l.split(','))) for l in open(sys.argv[1]).read().split('\n')]

S = set()

for c in cubes:
    S.add(c)
    

mv = [(0, 0, 1), (0, 1, 0), (1, 0, 0), (-1, 0, 0), (0, -1, 0), (0, 0, -1)]

def add(t1, t2):
    return (t1[0] + t2[0], t1[1] + t2[1], t1[2] + t2[2])    

k = 0



def extent(cubes):
    min_x = 10e9
    min_y = 10e9
    min_z = 10e9

    max_x = 0
    max_y = 0
    max_z = 0

    for c in cubes:
        min_x = min(min_x, c[0])
        min_y = min(min_y, c[1])
        min_z = min(min_z, c[2])

        max_x = max(max_x, c[0])
        max_y = max(max_y, c[1])
        max_z = max(max_z, c[2])
        
    return (min_x, min_y, min_z), (max_x, max_y, max_z)

(min_x, min_y, min_z), (max_x, max_y, max_z) = extent(cubes)

AIR = set()

for c in cubes:
    for m in mv:
        cc = add(c, m)
        if cc not in S:
            k += 1
            AIR.add(cc)  
print(k)    

# We can run a BFS on any air cube and check if we can reach any cube that is outside the mass
# We can also eliminate all the cubes we visited while running the BFS
def isEnclosed(c):
    
    Q = [c]
        
    visited = set([c])
    
    while Q:
        
        cube = Q.pop(0)

        if cube[0] < min_x or cube[0] > max_x or cube[1] < min_y or cube[1] > max_x or cube[2] < min_z or cube[2] > max_z:
            #print('Air reachable from ', c, ' - aborting with ', len(visited))
            return False, set()
        
        # All the neighbors
        for m in mv:
            cc = add(cube, m)
            if cc not in visited and cc not in S:
                visited.add(cc)
                Q.append(cc)
                
    
    
    return True, visited            
    # print('Air not reachable from', c)


ENCLOSED = set()

for c in AIR:
    if c in ENCLOSED:
        continue
    isEnc, visited = isEnclosed(c)
    if isEnc:
        #print(c, 'is enclosed, ', len(visited))
        ENCLOSED |= visited
        #ENCLOSED.add(c)

k2 = 0
for c in cubes:
    for m in mv:
        cc = add(c, m)
        if cc not in S and cc not in ENCLOSED:
            k2 += 1

print(k2)