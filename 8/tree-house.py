import sys

grid = [[int(k) for k in row] for row in open(sys.argv[1]).read().split('\n')]

visible = set()

height = len(grid)
width = len(grid[0])

# Top to bottom
for c in range(0, width):
    localMax = -1
    
    for r in range(0, height):
        if grid[r][c] > localMax:
            visible.add((r, c))
        localMax = max([localMax, grid[r][c]])
        
# Bottom to top:
for c in range(0, width):
    localMax = -1
    
    for r in range(height-1, 0, -1):
        if grid[r][c] > localMax:
            visible.add((r, c))
        localMax = max([localMax, grid[r][c]])
        
# Left to right:
for r in range(0, height):
    localMax = -1
    
    for c in range(0, width):
        if grid[r][c] > localMax:
            visible.add((r, c))
        localMax = max([localMax, grid[r][c]])
        
# Right to left:
for r in range(0, height):
    localMax = -1
    
    for c in range(width-1, 0, -1):
        if grid[r][c] > localMax:
            visible.add((r, c))
        localMax = max([localMax, grid[r][c]])

print(len(visible))

maxScore = 0

mv = [
    [1, 0],
    [-1, 0],
    [0, 1],
    [0, -1]
]

for r in range(0, height):
    for c in range(0, width):
        # Walk in all directions
        score = 1
        print('Looking at ' + str(r) + ", " + str(c))
        for m in mv:
            rr = r
            cc = c
            curHeight = grid[r][c]
            numVisible = 0
            while True:
                rr = rr + m[0]
                cc = cc + m[1]
                
                if 0 <= rr < height and 0 <= cc < width:
                    numVisible += 1
                    
                    if grid[rr][cc] >= curHeight:
                        break
                else:
                    break
            score *= numVisible
        maxScore = max([maxScore, score])
        
print(maxScore)
            