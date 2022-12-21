import sys

class Node:
    
    def __init__(self, name) -> None:
        self.name = name
        self.left = None
        self.right = None
        self.op = None
        self.value = None
    
    def __repr__(self):
        if self.value != None:
            return self.name + ' = ' + str(self.value)
        elif self.op != None:
            return self.name + ' = ' + self.left.name + ' ' + self.op + ' ' + self.right.name
        return '<not implemented>'
    
    def compute(self):
        if self.value != None:
            return self.value
        elif self.op != None:
            if self.op == '*':
                return self.left.compute() * self.right.compute()
            elif self.op == '+':
                return self.left.compute() + self.right.compute()
            elif self.op == '-':
                return self.left.compute() - self.right.compute()
            elif self.op == '/':
                l = self.left.compute()
                r = self.right.compute()
                return l // r
            elif self.op == '=':
                return self.left.compute(), self.right.compute()
            else:
                assert False
                
    def hasVar(self):
        if isinstance(self.value, VarRef):
            return True
        if self.op != None:
            return self.left.hasVar() or self.right.hasVar()
        else:
            return False
        
    def subtreeByVar(self):
        subtreeWithVar = self.left if self.left.hasVar() else self.right
        otherSubtree = self.left if subtreeWithVar == self.right else self.right
        
        return subtreeWithVar, otherSubtree
        
    def print(self):
        if isinstance(self.value, VarRef):
            return 'x'
        if self.value != None:
            return str(self.value)
        else:
            return '(' + self.left.print() + ' ' + self.op + ' ' + self.right.print() + ')'

class NodeRef:
    
    def __init__(self, name):
        self.name = name
        
class VarRef:
    
    def __init__(self):
        pass

lines = [tuple(map(lambda x: x.strip(), l.split(':'))) for l in open(sys.argv[1]).read().split('\n')]

nodes = dict()

for l in lines:
    name, op = l
    nodes[name] = n = Node(name)
    
    if op.isnumeric():
        n.value = int(op)
    else:
        left, op, right = op.split(' ')
        n.left = NodeRef(left)
        n.right = NodeRef(right)
        n.op = op
        
# Second pass, replacing node refs with proper nodes
for name, n in nodes.items():
    if n.left != None:
        n.left = nodes[n.left.name]
    if n.right != None:
        n.right = nodes[n.right.name]
        
print(nodes['root'].compute())

root = nodes['root']

root.op = '='
nodes['humn'].value = VarRef()
#print(root.left.hasVar(), root.right.hasVar())
#print(root.print())

# Idea: for each node, only one subtree can actually contain a variable
# So we always look at root.left or root.right and their subtrees
# The subtree without the variable can be moved to the other side by adding
# a new node on the other side with the inverted operation

inversionMap = {'+': '-', '-': '+', '*': '/', '/': '*'}

withVar, withoutVar = root.subtreeByVar()
print('Should match', withoutVar.compute())

print(root.print())
while True:
    
    # Do this in every iteration since the children actually change every round
    withVar, withoutVar = root.subtreeByVar()

    
    
    shouldRemain, shouldMove = withVar.subtreeByVar()
    #print(withVar)
    #print(shouldMove)
    
    newOp = ''
    newNode = None
    
    movingPartIsRightChild = True if withVar.right == shouldMove else False
    
    if withVar.op != "/" and withVar.op != "-" or movingPartIsRightChild:
        newOp = inversionMap[withVar.op]
        newNode = Node('moving ' + str(shouldMove) + ' with new op ' + newOp)
        newNode.left = withoutVar
        newNode.right = shouldMove
        newNode.op = newOp
        
        if withoutVar == root.left:
            root.left = newNode
            root.right = shouldRemain
        else:
            root.right = newNode
            root.left = shouldRemain
    else:
        # We only have to handle the cases where we have to move the dividend
        if withVar.op == '/':
            # A/x = B => 1/x = B/A => x = A/B
            newNode = Node('moving ' + str(shouldMove) + ' with new op /')
            newNode.right = withoutVar
            newNode.left = shouldMove
            newNode.op = '/'
            
            if withoutVar == root.left:
                root.left = newNode
                root.right = shouldRemain
            else:
                root.right = newNode
                root.left = shouldRemain
        elif withVar.op == '-':
            # A-x = B => -x = B-A => x = A-B
            newNode = Node('moving ' + str(shouldMove) + ' with new op /')
            newNode.right = withoutVar
            newNode.left = shouldMove
            newNode.op = '-'
            
            if withoutVar == root.left:
                root.left = newNode
                root.right = shouldRemain
            else:
                root.right = newNode
                root.left = shouldRemain

    #print('moving', shouldMove, 'with new op', newOp)


    print(root.print())
    
    # If the only node left on either side is the variable, we are done
    if root.left.name == 'humn' or root.right.name == 'humn':
        break
    

_, solution = root.subtreeByVar()
print(solution.compute())