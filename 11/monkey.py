from copy import deepcopy
import sys

from numpy import product

monkeyLines = open(sys.argv[1]).read().split('\n\n')

class Monkey:
    
    def __init__(self) -> None:
        self.index = 0
        self.items = []
        self.operation = ''
        self.test = None
        self.trueTarget = None,
        self.falseTarget = None
    
    def __repr__(self) -> str:
        return 'Monkey ' + str(self.index) + '\n' + str(len(self.items)) + ' items' + '\nTrue target: ' + str(self.trueTarget) + '\nFalse target: ' + str(self.falseTarget)
        
    
monkeys = []
for block in monkeyLines:
    monkey = Monkey()
    monkeys.append(monkey)
    for l in block.split('\n'):
        line = l.strip()
        if line.startswith('Monkey'):
            monkey.index = int(line.removeprefix('Monkey').removesuffix(':'))
        elif line.startswith('Starting items:'):
            monkey.items = list(map(int, line.removeprefix('Starting items: ').split(', ')))
        elif line.startswith('Operation:'):
            monkey.operation = line.removeprefix('Operation: new = ')
        elif line.startswith('Test:'):
            monkey.test = int(line.removeprefix('Test: divisible by '))
        elif line.startswith('If true:'):
            monkey.trueTarget = int(line.removeprefix('If true: throw to monkey '))
        elif line.startswith('If false:'):
            monkey.falseTarget = int(line.removeprefix('If false: throw to monkey '))




# Idea here: (a mod k*n) mod n = a mod n
# So we set the modulus to the product of all "test" divisors.
modulus = product([monkey.test for monkey in monkeys])
   
def run(monkeys, p1):  
    inspectionCounts = [0] * len(monkeys)         
    for _ in range(10000 if not p1 else 20):
        for monkey in monkeys:
            while len(monkey.items) > 0:
                item = monkey.items.pop(0)
                inspectionCounts[monkey.index] += 1

                newVal = int(eval(monkey.operation.replace('old', str(item)))) % modulus
                
                if p1:
                    newVal = newVal // 3
                
                            
                t = newVal % monkey.test == 0
                if t:
                    monkeys[monkey.trueTarget].items.append(newVal)
                else:
                    monkeys[monkey.falseTarget].items.append(newVal)
                
    sortedCounts = sorted(inspectionCounts, reverse=True)

    print(sortedCounts[0] * sortedCounts[1])
    
m1 = deepcopy(monkeys)
m2 = deepcopy(monkeys)

run(m1, True)
run(m2, False)