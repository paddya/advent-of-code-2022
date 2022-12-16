import sys
from itertools import zip_longest
from functools import cmp_to_key
import json

listPairs = [[json.loads(l) for l in block.split('\n')] for block in open(sys.argv[1]).read().split('\n\n')]

idxSum = 0

def compare(l1, l2):
    if isinstance(l1, int) and isinstance(l2, int):
        if l1 == l2:
            return None
        return l1 < l2
    elif isinstance(l1, list) and isinstance(l2, list):
        for t1, t2 in zip_longest(l1, l2):
            if t1 == None:
                return True
            if t2 == None:
                return False
            res = compare(t1, t2)
            if res != None:
                return res
    elif isinstance(l1, int) and isinstance(l2, list):
        return compare([l1], l2)
    elif isinstance(l1, list) and isinstance(l2, int):
        return compare(l1, [l2])
    
def sortFunction(l1, l2):
    res = compare(l1, l2)
    if res == None:
        return 0
    if res:
        return -1
    else:
        return 1

allLists = [[[2]], [[6]]]
for idx, pair in enumerate(listPairs):
    l1, l2 = pair
    allLists.append(l1)
    allLists.append(l2)
    if compare(l1, l2):
        idxSum += idx + 1
    
print(idxSum)
allLists.sort(key=cmp_to_key(sortFunction))

idx1 = -1
idx2 = -1

for idx, l in enumerate(allLists):
    if l == [[2]]:
        idx1 = idx + 1
    if l == [[6]]:
        idx2 = idx + 1
        
print(idx1 * idx2)