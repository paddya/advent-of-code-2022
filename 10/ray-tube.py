import sys

commands = open(sys.argv[1]).read().split('\n')

ip = 0
cycle = 0

X = 1

isRunningAdd = False
nextDiff = 0

acc = 0

screen = [['░░' for _ in range(40)] for _ in range(6)]

def printScreen(screen):
    for row in screen:
        print(''.join(row))
        
def cycleToCoords(cycle):
    return divmod(cycle - 1, 40)

# Each loop iteration is a cycle, but we don't advance the instruction pointer in every iteration
while ip < len(commands):
    cycle += 1
    currentlyDrawing = cycleToCoords(cycle)
    
    # Check if there is overlap between the current drawing position and the sprite
    hasOverlap = abs(X - currentlyDrawing[1]) <= 1
    
    if hasOverlap:
        screen[currentlyDrawing[0]][currentlyDrawing[1]] = '██'


    if cycle in [20, 60, 100, 140, 180, 220]:
        acc += cycle*X

    
    # If we are currently running an addx, it will finish in this cycle instead
    if isRunningAdd:
        X += nextDiff
        isRunningAdd = False
        nextDiff = False
        ip += 1
        continue
    
    cmd = commands[ip]
    
    # Just increase the instruction pointer with a noop
    if cmd == "noop":
        ip += 1
    if cmd.startswith('addx'):
        nextDiff = int(cmd.removeprefix('addx '))
        isRunningAdd = True

print(acc)
printScreen(screen)
