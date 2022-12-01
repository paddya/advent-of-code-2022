
# Compute the total for all elves first
elves = sorted([
    sum([int(k) for k in e.split('\n')]) 
    for e in open('input.txt').read().strip().split('\n\n')
], reverse=True)

# After sorting, the list can be used to print solutions for both parts
print(elves[0])
print(sum(elves[0:3]))