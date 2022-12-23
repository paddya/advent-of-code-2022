from collections import defaultdict
import re
import sys

grid, instructions = open(sys.argv[1]).read().split('\n\n')

pattern = re.compile(r'^(R|L)(\d+)')
steps = []

# Hack: we're facing right at first
instructions = 'R' + instructions
while len(instructions) > 0:
    match = pattern.match(instructions)
    
    steps.append((match.group(1), int(match.group(2))))
    instructions = instructions.removeprefix(match.group(0))
    
lines = grid.split('\n')

G = defaultdict(lambda: ' ')
# Keep track of the line start and ends to make wrapping easier
RSTART = dict()
REND = dict()

CSTART = dict()
CEND = dict()

hasColumnStarted = defaultdict(lambda: False)
hasColumnEnded = defaultdict(lambda: False)

for r, line in enumerate(lines):
    line = ("{:<" + str(len(lines[0])) + "}").format(line)
    hasLineStarted = False
    hasLineEnded = False
    for c, char in enumerate(line):
        if char == ' ':
            if hasColumnStarted[c] and not hasColumnEnded[c]:
                CEND[c] = r - 1
                hasColumnEnded[c] = True 
            if hasLineStarted and not hasLineEnded:
                REND[r] = c - 1
                hasLineEnded = True
            continue
        else:
            if not hasColumnStarted[c]:
                CSTART[c] = r
                hasColumnStarted[c] = True
            if not hasLineStarted:
                hasLineStarted = True
                RSTART[r] = c
            G[(r, c)] = char
    if not hasLineEnded:
        REND[r] = len(line) - 1

# End every column that we started
for k in CSTART:
    if not hasColumnEnded[k]:
        CEND[k] = len(lines) - 1
    

startNode = None
for i in range(RSTART[0], REND[1]):
    if G[(0, i)] == '.':
        startNode = (0, i)
        break

curPos = startNode

mv = {
    'R': (0, 1),
    'L': (0, -1),
    'U': (-1, 0),
    'D': (1, 0)
}


x_min = min([v for k, v in RSTART.items()])
x_max = max([v for k, v in REND.items()])

y_min = min([v for k, v in CSTART.items()])
y_max = max([v for k, v in CEND.items()])


# for x in range(x_max+1):
#     print('Column', x, 'Column start: ', CSTART[x], ' -- Column end: ', CEND[x])

# for y in range(y_max+1):
#     print('Row', y, 'Row start: ', RSTART[y], ' -- Row end: ', REND[y])

# move t1 by t2 while staying in the grid
def move(t1, direction):
    t2 = mv[direction]
    ny = (t1[0] + t2[0])
    nx = (t1[1] + t2[1])
    
    #print(t1, t2, (ny, nx))
    
    #print(nx, ny, RSTART[ny], REND[ny], CSTART[nx], CEND[ny])
    # If nx would be before the line start, we wrap around to the end
    if direction == 'L' and nx < RSTART[ny]:
        #print(nx, RSTART[ny])
        #print('Wrap left')
        nx = REND[ny]
    if direction == 'R' and nx > REND[ny]:
        #print('Wrap right')
        nx = RSTART[ny]
    
    if direction == 'U' and ny < CSTART[nx]:
        #print('Wrap top')
        ny = CEND[nx]

    if direction == 'D' and ny > CEND[nx]:
        #print('Wrap bottom')
        ny = CSTART[nx]
    
    return (ny, nx)

visited = dict()


def printGrid(G):
    print('')
    for y in range(y_max+1):
        for x in range(x_max+1):
            if (y, x) in visited:
                print(visited[(y,x)], end='', file=sys.stderr)
            elif not (y, x) in G:
                print(' ', end='', file=sys.stderr)
            else:
                print(G[(y,x)], end='', file=sys.stderr)
        print('', file=sys.stderr)
    print('', file=sys.stderr)
            



directions = ['R', 'D', 'L', 'U']
invertedDirections = {
    'R': 'L',
    'L': 'R',
    'U': 'D',
    'D': 'U'
}

# Our first step contains a direction change, so we start facing up to be in the right
# direction after rotating
directionIdx = 3


for s in steps:
    movement, numSteps = s
    
    if movement == 'R':
        directionIdx = (directionIdx + 1) % 4
    elif movement == 'L':
        directionIdx = (directionIdx - 1) % 4
    
    direction = directions[directionIdx]
    
    visited[curPos] = direction
    for _ in range(numSteps):
        target = move(curPos, direction)
        #print('Try to touch ', target, ' by moving ', direction)
        #printGrid(G)
        # simplest case, we can just move
        if G[target] == '.':
            visited[curPos] = direction
            curPos = target
            continue
        
        if G[target] == '#':
            #print('Encountered wall at ', target ,' - stopping')
            break
        
        
        assert False

#printGrid(G)
r, c = curPos
print((r+1)*1000+(c+1)*4+directionIdx)


# Steps to take for part 2:

# 1. Provide a way to map coordinates to cube sides
# 2. Figure out which edge we are leaving on to figure out the next side
# 3. Figure out the position and direction on the next side

# Transition map with 12 entries for s


# Key: coordinate ranges => will always iterate over whole map until a side matches, then will return values
SIDE_MAP = dict()
SIDE_MAP[((0, 49), (50, 99))] = 2
SIDE_MAP[((0, 49), (100, 149))] = 1
SIDE_MAP[((50, 99), (50, 99))] = 3
SIDE_MAP[((100, 149), (50, 99))] = 4
SIDE_MAP[((100, 149), (0, 49))] = 5
SIDE_MAP[((150, 199), (0, 49))] = 6

INVERTED_MAP = dict()
for k, v in SIDE_MAP.items():
    INVERTED_MAP[v] = k

def getSide(pos):
    y, x = pos
    for ((y_min, y_max), (x_min, x_max)), side in SIDE_MAP.items():
        if y_min <= y <= y_max and x_min <= x <= x_max:
            return side
    return None

# Neither direction nor coordinates need to change

NO_CHANGE = 0
INVERT_DIRECTION_ROW = 1
TOP_TO_BOTTOM = 2
BOTTOM_TO_RIGHT = 3
TOP_TO_LEFT = 4
LEFT_TO_TOP = 5
RIGHT_TO_BOTTOM = 6
BOTTOM_TO_TOP = 7
N = dict()
N[(1, 'L')] = (2, NO_CHANGE) # 2 -> 1 no coordinate change necessary, it just works
N[(1, 'R')] = (4, INVERT_DIRECTION_ROW)
N[(1, 'U')] = (6, TOP_TO_BOTTOM)
N[(1, 'D')] = (3, BOTTOM_TO_RIGHT)

N[(2, 'L')] = (5, INVERT_DIRECTION_ROW)
N[(2, 'R')] = (1, NO_CHANGE)
N[(2, 'U')] = (6, TOP_TO_LEFT)
N[(2, 'D')] = (3, NO_CHANGE)

N[(3, 'L')] = (5, LEFT_TO_TOP)
N[(3, 'R')] = (1, RIGHT_TO_BOTTOM)
N[(3, 'U')] = (2, NO_CHANGE)
N[(3, 'D')] = (4, NO_CHANGE)

N[(4, 'R')] = (1, INVERT_DIRECTION_ROW)
N[(4, 'L')] = (5, NO_CHANGE)
N[(4, 'U')] = (3, NO_CHANGE)
N[(4, 'D')] = (6, BOTTOM_TO_RIGHT)

N[(5, 'R')] = (4, NO_CHANGE)
N[(5, 'L')] = (2, INVERT_DIRECTION_ROW)
N[(5, 'U')] = (3, TOP_TO_LEFT)
N[(5, 'D')] = (6, NO_CHANGE)

N[(6, 'R')] = (4, RIGHT_TO_BOTTOM)
N[(6, 'L')] = (2, LEFT_TO_TOP)
N[(6, 'U')] = (5, NO_CHANGE)
N[(6, 'D')] = (1, BOTTOM_TO_TOP)

def move2(pos, direction):
    m = mv[direction]
    ny = (pos[0] + m[0])
    nx = (pos[1] + m[1])
    
    newPos = (ny, nx)
    prevSide = getSide(pos)
    nextSide = getSide(newPos)
    
    ((y_min, y_max), (x_min, x_max)) = INVERTED_MAP[prevSide]
    oldYOffset = pos[0] - y_min
    oldXOffset = pos[1] - x_min
    
    if prevSide == nextSide:
        return (ny, nx), direction
    else:
        # Side transition
        newSide, transform = N[(prevSide, direction)]
        ((new_y_min, new_y_max), (new_x_min, new_x_max)) = INVERTED_MAP[newSide]
        # The luckiest case: we can switch sides without direction change
        if transform == NO_CHANGE:
            return (ny, nx), direction
        elif transform == INVERT_DIRECTION_ROW:
            # Invert direction
            newDirection = invertedDirections[direction]
            # x offset stays the same, however we get the inverted y offset
            nx = new_x_min + oldXOffset
            ny = new_y_max - oldYOffset
            
            return (ny, nx), newDirection
        elif transform == TOP_TO_BOTTOM:
            nx = new_x_min + oldXOffset
            ny = new_y_max
            return (ny, nx), direction
        elif transform == BOTTOM_TO_RIGHT:
            nx = new_x_min + oldYOffset
            ny = new_y_min + oldXOffset
            return (ny, nx), 'L'
        elif transform == TOP_TO_LEFT:
            nx = new_x_min
            ny = new_y_min + oldXOffset
            
            return (ny, nx), 'R'
        elif transform == LEFT_TO_TOP:
            nx = new_x_min + oldYOffset
            ny = new_y_min
            
            return (ny, nx), 'D'
        elif transform == RIGHT_TO_BOTTOM:
            nx = new_x_min + oldYOffset
            ny = new_y_max
            return (ny, nx), 'U'
        elif transform == BOTTOM_TO_TOP:
            nx = new_x_min + oldXOffset
            ny = new_y_min
            
            return (ny, nx), direction
        return None


def debug_move2(pos, dir):
    newPos, newDir = move2(pos, dir)
    
    print(pos, '(', dir, ',', getSide(pos), ')', '->', newPos, '(', newDir, ',', getSide(newPos), ')')

# # Side 1, no change
# debug_move2((0, 100), 'R')
# debug_move2((0, 100), 'L')
# debug_move2((0, 149), 'R')
# debug_move2((0, 149), 'U')
# debug_move2((49, 149), 'D')
# print('')
# # Side 2
# debug_move2((0, 99), 'R')
# debug_move2((0, 50), 'L')
# debug_move2((0, 50), 'U')
# debug_move2((49, 99), 'D')
# print('')
# # Side 3
# debug_move2((50, 50), 'L')
# debug_move2((50, 99), 'R')
# debug_move2((99, 99), 'R')
# debug_move2((50, 50), 'U')
# debug_move2((99, 50), 'D')
# print('')
# # Side 4
# debug_move2((100, 99), 'R')
# debug_move2((100, 50), 'L')
# debug_move2((100, 50), 'U')
# debug_move2((149, 99), 'D')
# print('')
# # Side 5
# debug_move2((100, 49), 'R')
# debug_move2((100, 0), 'L')
# debug_move2((149, 0), 'L')
# debug_move2((100, 0), 'U')
# debug_move2((149, 0), 'D')
# print('')
# # Side 6
# debug_move2((199, 0), 'L')
# debug_move2((199, 49), 'R')
# debug_move2((150, 0), 'U')
# debug_move2((199, 0), 'D')
# debug_move2((199, 49), 'D')

# debug_move2((149, 50), 'D')



curPos = startNode
directionIdx = 3
visited = dict()

enableLogs = False

for s in steps:
   
    
    movement, numSteps = s
        
    if movement == 'R':
        directionIdx = (directionIdx + 1) % 4
    elif movement == 'L':
        directionIdx = (directionIdx - 1) % 4
    
    direction = directions[directionIdx]

    
    visited[curPos] = direction
    for _ in range(numSteps):
        target, newDirection = move2(curPos, direction)
        #printGrid(G)
        # simplest case, we can just move
        if G[target] == '.':
            visited[curPos] = direction
            curPos = target
            direction = newDirection
            directionIdx = directions.index(newDirection)
            continue
        
        if G[target] == '#':
            break
        
        
        assert False

#printGrid(G)

r, c = curPos
print((r+1)*1000+(c+1)*4+directionIdx)