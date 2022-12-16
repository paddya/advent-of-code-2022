from __future__ import annotations
from functools import cmp_to_key
import sys
import re
import heapq
from copy import copy
from collections import defaultdict
from itertools import product

from numpy import nonzero


valvePattern = re.compile(r'Valve (\w+) has flow rate=(\d+)')
class Valve:
    
    def __init__(self, name, flowRate, neighbors) -> None:
        self.name = name
        self.flowRate = flowRate
        self.neighbors = neighbors

    def __repr__(self) -> str:
        return 'Valve {name} has flow rate={flowRate}'.format(name=self.name, flowRate=self.flowRate)

def mapLine(l):
    flowRate, neighbors = l.split('; ')
    
    neighbors = neighbors.removeprefix('tunnels lead to valves ').removeprefix('tunnel leads to valve ').split(', ')
    
    match = valvePattern.fullmatch(flowRate)
    
    return Valve(match.group(1), int(match.group(2)), neighbors)

class State:
    
    def __init__(self, location, elephant, openValves, minutes, elephantMinutes, total, valves):
        self.location = location
        self.elephant = elephant
        self.openValves = openValves
        self.minutes = minutes
        self.elephantMinutes = elephantMinutes
        self.total = total
        self.valves = valves

    def __repr__(self) -> str:
        return '{location}/{elephant}, open valves: {valves}, remaining: {remaining}, elephant remaining: {elRemaining}, total: {total}'.format(location=self.location, elephant=self.elephant, valves=' '.join(sorted(self.openValves)), remaining=self.minutes, elRemaining=self.elephantMinutes, total=self.total)


    def __hash__(self) -> int:
        return hash((self.location, self.elephant, tuple(sorted(self.openValves)), self.minutes, self.elephantMinutes, self.total))
    
    def __eq__(self, other) -> bool:
        return self.__hash__() == other.__hash__()
    
    def __lt__(self, other):
        return self.total < other.total

valves = [mapLine(l) for l in open(sys.argv[1]).read().split('\n')]

valveMap = dict()
for v in valves:
    valveMap[v.name] = v


D = dict()

# Compute distances between all valves

def bfs(source):
    D = dict()
    D[source] = 0
    
    Q = [source]
    visited = set()
    while len(Q) > 0:
        curNode = Q.pop(0)
        v = valveMap[curNode]
        
        for n in v.neighbors:
            if n not in visited:
                visited.add(n)
                D[n] = D[curNode] + 1
                Q.append(n)
    return D


for v in valves:
    D[v.name] = bfs(v.name)
    
visited = set()

TOTAL = defaultdict(lambda: 0)

def sortValves(v1, v2):
    if v1.flowRate == v2.flowRate:
        return 0
    return -1 if v1.flowRate > v2.flowRate else 1

nonZeroValves = [v for v in valves if v.flowRate > 0]
nonZeroValves.sort(key=cmp_to_key(sortValves))

numNonZeroValves = len(nonZeroValves)



def findPossibleMoves(state):
    state : State
            
    if state.minutes == 0 and state.elephantMinutes == 0:
        return []
        
    # Nothing left to do if all valves are open, don't bloat the state
    if len(state.openValves) == numNonZeroValves:
        return []
    
    states = []
    
    
    # Consider all the non-open valves and jump directly to them
    # Me and elephant don't move in tandem, so we need to handle state transitions independently
        
    for v in state.valves:                
        d1 = D[state.location][v.name]
        d2 = D[state.elephant][v.name]
        
        if d1 <= state.minutes:
            ov = set(state.openValves)
            ov.add(v.name)
            valves = state.valves - {v}
            remWhenOpen = state.minutes - d1 - 1
            total = state.total + remWhenOpen*v.flowRate
            
            key = tuple(sorted(ov))
            if not key in BEST or total >= BEST[key]:
                BEST[key] = total        
                states.append(State(v.name, state.elephant, ov, remWhenOpen, state.elephantMinutes, total, valves))
            
        if d2 <= state.elephantMinutes:
            ov = set(state.openValves)
            ov.add(v.name)
            valves = state.valves - {v}
            remWhenOpen = state.elephantMinutes - d2 - 1
            total = state.total + remWhenOpen*v.flowRate
            key = tuple(sorted(ov))
            if not key in BEST or total >= BEST[key]:
                BEST[key] = total     
                states.append(State(state.location, v.name, ov, state.minutes, remWhenOpen, total, valves))
        
        
        # # This might actually only work on this specific input, the safer bet would be to use (v1.name, v2.name, tuple(sorted(ov))) as the state key

        
        #states.append(newState)

    return states


def upperBound(state):
    # Upper bound is that we just open every valve in the current move
    potential = state.total
    for v in state.valves:   
        potential += max([max([state.minutes - D[state.location][v.name], state.elephantMinutes - D[state.elephant][v.name]]) - 1, 0]) * v.flowRate
    
    return potential


for minutes in [(30, 0), (26, 26)]:
    m1, m2 = minutes
    curMax = 0

    Q = []
    BEST = dict()
    initialState = State('AA', 'AA', set(), m1, m2, 0, set(nonZeroValves))
    heapq.heappush(Q, (0, initialState))
    i = 0
    while Q:
        state : State
        pot, state = heapq.heappop(Q)
        
        if -pot < curMax:
            continue

        i += 1
        
        if state.total > curMax:
            curMax = state.total
            
        curMax = max([curMax, state.total])
        
        newStates = findPossibleMoves(state)
        
        for ns in newStates:
            if not ns in visited:
                potential = upperBound(ns)
                if potential > curMax:
                    visited.add(ns)

                    heapq.heappush(Q, (-potential, ns))

    print(curMax)