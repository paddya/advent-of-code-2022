
import sys


lines = [[k for k in l.split(' ')] for l in open(sys.argv[1]).read().split('\n')]


# This could be a lot shorter by defining a two-dimensional lookup table
def outcome(opponent, me):
    if opponent == "A" and me == "X":
        return 3
    
    if opponent == "A" and me == "Y":
        return 6
    
    if opponent == "A" and me == "Z":
        return 0
    
    if opponent == "B" and me == "X":
        return 0
    
    if opponent == "B" and me == "Y":
        return 3
    
    if opponent == "B" and me == "Z":
        return 6
    
    if opponent == "C" and me == "X":
        return 6
    
    if opponent == "C" and me == "Y":
        return 0
    
    if opponent == "C" and me == "Z":
        return 3

def mychoice(opponent, result):
    if opponent == "A" and result == "X":
        return "Z"
    
    if opponent == "A" and result == "Y":
        return "X"
    
    if opponent == "A" and result == "Z":
        return "Y"
    
    if opponent == "B" and result == "X":
        return "X"
    
    if opponent == "B" and result == "Y":
        return "Y"
    
    if opponent == "B" and result == "Z":
        return "Z"
    
    if opponent == "C" and result == "X":
        return "Y"
    
    if opponent == "C" and result == "Y":
        return "Z"
    
    if opponent == "C" and result == "Z":
        return "X"

total = 0    
total_p2 = 0
m = {
    "X": 1,
    "Y": 2,
    "Z": 3
}

for l in lines:
    total += outcome(l[0], l[1]) + m[l[1]]
    me = mychoice(l[0], l[1])
    total_p2 += outcome(l[0], me) + m[me]

print(total)
print(total_p2)