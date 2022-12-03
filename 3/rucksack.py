import sys

lines = [l for l in open(sys.argv[1]).read().split('\n')]

print(ord('a'), ord('A'))

def mapToNumber(str: str):
    if str.lower() == str:
        return ord(str) - 96
    
    return ord(str) - 38
    

total = 0
for l in lines:
    first, second = set(l[0:int(len(l)/2)]), set(l[int(len(l)/2):])

    
    intersection = first.intersection(second)
    
    total += sum([mapToNumber(k) for k in intersection])

    
print(total)


total_p2 = 0

while True:
    if len(lines) == 0:
        break
    
    first, second, third = set(lines.pop()), set(lines.pop()), set(lines.pop())
    
    int1 = first.intersection(second)
    final = int1.intersection(third)
    
    total_p2 += sum([mapToNumber(k) for k in final])
    
print(total_p2)