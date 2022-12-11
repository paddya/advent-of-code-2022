import sys

input = open(sys.argv[1]).read().strip()

windowSize = int(sys.argv[2])

for offset in range(windowSize, len(input)):
    substr = input[offset-windowSize:offset]
    chars = set([c for c in substr])
    
    if len(chars) == windowSize:
        print(offset)
        break