import re
import sys

lines = open(sys.argv[1]).read().split('\n')

class File:
    def __init__(self, name, size) -> None:
        self.name = name
        self.size = size
        pass

class Directory:
    
    def __init__(self, name: str, parent) -> None:
        self.name = name
        self.parent = parent
        self.directories = []
        self.files = []
        pass
    
    def addDirectory(self, name: str):
        newDir = Directory(name, self)
        self.directories.append(newDir)
        
    def addFile(self, name, size):
        self.files.append(File(name, size))
        
    def getDir(self, name):
        for dir in self.directories:
            if dir.name == name:
                return dir
            
    def size(self):
        total = sum([f.size for f in self.files]) + sum([d.size() for d in self.directories])
        return total
    
    def __repr__(self):
        return 'Directory ' + self.name + " -- " + str(self.size())
        
        
root = Directory('Root', None)

cwd = None
readingDirectory = False

for line in lines:
    if line == '$ cd /':
        cwd = root
    elif line == '$ ls':
        assert cwd != None
        readingDirectory = True
    elif line.startswith('$ cd'):
        targetDir = line.removeprefix('$ cd ')
        if targetDir == '..':
            cwd = cwd.parent
        else:
            cwd = cwd.getDir(targetDir)
    else:
        if line.startswith('dir'):
            dirName = line.removeprefix('dir ')
            cwd.addDirectory(dirName)
        else:
            size, name = line.split(' ')
            cwd.addFile(name, int(size))
            
# Walk the tree and add up all directories with less than 100K size

def sumDirs(current: Directory):
    total = current.size() if current.size() < 100000 else 0
    
    total += sum([sumDirs(d) for d in current.directories])
    return total




print(sumDirs(root))

availableSpace = 70000000
required = 30000000

freeSpace = availableSpace-root.size()
toFree = required-freeSpace

# First step, collect all directories which have the minimum size into a list
def collectDirs(current: Directory):
    candidates = []
    # We can actually ignore all directories that are smaller than the min size
    if current.size() >= toFree:
        candidates.append(current)
        
        subDirs = [sd for d in current.directories for sd in collectDirs(d)]
        if len(subDirs) > 0:
            candidates += subDirs
        
    return candidates

print(min(collectDirs(root), key=lambda d: d.size()).size())


