
import copy
import sys
import re


initialArrangement, moves = open(sys.argv[1]).read().split('\n\n')

# Simplify the initial arrangement first by dropping everything that is not a letter

pattern = re.compile(r"((   |\[[A-Z]\]) ?)+")

lines = initialArrangement.split('\n')[:-1]
stacks = [[] for _ in range(10)]

for l in lines:
    # Just walk the line in steps of three characters
    offset = 0
    # Start at stack 1 to save some mapping math later
    stackNum = 1
    while offset <= len(l) - 3:
        item = l[offset:offset+3]
        
        if item != "   ":
            stacks[stackNum].append(item[1])
        
        offset += 4
        stackNum += 1



def parseMoveLine(m):
    pattern = re.compile("move (\d+) from (\d+) to (\d+)")
    matches = re.match(pattern, m)
    num, src, dst = int(matches.group(1)), int(matches.group(2)), int(matches.group(3))
    
    return (num, src, dst)


parsedMoves = [parseMoveLine(m) for m in moves.split('\n')]

stackBackup = copy.deepcopy(stacks)

# Part 1
for m in parsedMoves:
    num, src, dst = m
    
    for _ in range(num):
        stacks[dst].insert(0, stacks[src].pop(0))

    
stacks.pop(0)
message = [s[0] for s in stacks if len(s) > 0]
print(''.join(message))


# Part 2
stacks = stackBackup

for m in parsedMoves:
    num, src, dst = m
    
    tmp = []
    for _ in range(num):
        tmp.append(stacks[src].pop(0))
    
    tmp.reverse()
    for c in tmp:
        stacks[dst].insert(0, c)
    
stacks.pop(0)
message = [s[0] for s in stacks if len(s) > 0]
print(''.join(message))

    