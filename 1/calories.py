
# Compute the total for all elves first
elves = [
    sum([int(k) for k in e.split('\n')]) 
    for e in open('input.txt').read().strip().split('\n\n')
]

elves.sort(reverse=True)

# After sorting, the list can be used to print solutions for both parts
print(elves[0])
print(sum(elves[0:3]))