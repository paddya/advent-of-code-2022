import sys

ranges = [[[int(rng) for rng in rangeStr.split('-')] for rangeStr in l.split(',')] for l in open(sys.argv[1]).read().split('\n')]

# Checks whether r1 completely contains r2
def contains(r1, r2):
    return r1[0] <= r2[0] and r1[1] >= r2[1]

# CHecks whether r1 overlaps with r2
def overlap(r1, r2):
    return r1[0] <= r2[0] and r1[1] >= r2[0]

count = 0
count_p2 = 0

for r in ranges:
    r1, r2 = r
    
    if contains(r1, r2) or contains(r2, r1):
        count += 1

    if overlap(r1, r2) or overlap(r2, r1):
        count_p2 += 1

print(count)
print(count_p2)