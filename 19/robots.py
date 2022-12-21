from __future__ import annotations
import sys
import re
from copy import copy
import random
from collections import defaultdict
import math

lPattern = re.compile(r'Blueprint (\d+): Each ore robot costs (\d+) ore. Each clay robot costs (\d+) ore. Each obsidian robot costs (\d+) ore and (\d+) clay. Each geode robot costs (\d+) ore and (\d+) obsidian.')

class Blueprint:
    
    def __init__(self, id, resourceUsage):
        self.id = id
        self.resourceUsage = resourceUsage
        
        self.maxima = defaultdict(lambda: 0)
        for k, usages in self.resourceUsage.items():
            for amount, res in usages:
                self.maxima[res] = max(self.maxima[res], amount)
                
class State:
    
    def __init__(self, resources, robots, minutes):
        self.resources = resources
        self.robots = robots
        self.minutes = minutes
        
    def __repr__(self) -> str:
        return '{res} - {robots} - {minutes}'.format(res=tuple(self.resources.items()), robots=tuple(self.robots.items()), minutes=self.minutes)
    
    def __hash__(self) -> int:
        res = tuple(sorted(self.resources.items()))
        robots = tuple(sorted(self.robots.items()))
        return hash((res, robots, self.minutes))
    
    def __eq__(self, __o: object) -> bool:
        return hash(self) == hash(__o)

def mapLine(l):
    match = lPattern.fullmatch(l.strip())
    id = int(match.group(1))
    usage = dict()
    usage['ore'] = [(int(match.group(2)), 'ore')]
    usage['clay'] = [(int(match.group(3)), 'ore')] 
    usage['obsidian'] = [(int(match.group(4)), 'ore'), (int(match.group(5)), 'clay')]
    usage['geode'] = [(int(match.group(6)), 'ore'), (int(match.group(7)), 'obsidian')]
    
    return Blueprint(id, usage)

bps = [mapLine(l) for l in open(sys.argv[1]).read().split('\n')]


BEST = dict()
curBest = 0
numCacheHits = 0
def simulate(blueprint, state):
    global curBest
    global numCacheHits
    
    #print('\n==========\n')
    #print(state)
    
    # if state in CACHE:
    #     #print('Cache hit!')
    #     return CACHE[state]
    
    # Produce resources
    state : State
    if state.minutes == 0:
        return state.resources['geode']
    
    
    # Assumption: for every remaining minute, we create a new geode robot, prune if we don't beat curBest
    maxGeode = state.resources['geode']
    minutes = state.minutes
    while minutes >= 0:
        maxGeode += minutes + state.robots['geode']
        minutes -= 1
    
    if maxGeode < curBest:
        return 0
    
    newResources = dict()
    for k, v in state.resources.items():
        newResources[k] = state.resources[k] + state.robots[k]
    
    # One option: just do nothing
    doNothing = State(newResources, state.robots, state.minutes - 1)
    newStates = []
    
    
    # TODO: For each robot, actually add the next possibility to build it as the next state
    # Check if we can produce any robot, prioritizing geode ones
    for robot in ['geode', 'obsidian', 'clay', 'ore']:
        # We do not need another robot if we already produce the maximum requirement for this resource
        if robot != 'geode':
            if state.robots[robot] >= blueprint.maxima[robot]:
                continue
        
        usage = blueprint.resourceUsage[robot]
        hasEnough = True
        canProduceAllResources = True
        numRounds = 0
        for (amount, resource) in usage:
            # We have to check state.resources here because we only have the resources from the beginning of the minute
            if state.resources[resource] < amount:
                hasEnough = False
                if state.robots[resource] == 0:
                    canProduceAllResources = False    
                else:
                    numRounds = max([numRounds, math.ceil((amount - state.resources[resource]) / state.robots[resource]) + 1])
        
        res = copy(newResources)
        if hasEnough:
            for (amount, resource) in usage:
                res[resource] -= amount
            robots = copy(state.robots)
            robots[robot] += 1
            newStates.append(State(res, robots, state.minutes - 1))
            #print('Could produce new robot for ', robot)
            
        elif canProduceAllResources:
            # Add the resources for numRounds
            for k in res:
                res[k] += (numRounds - 1) * state.robots[k]
            
            for (amount, resource) in usage:
                res[resource] -= amount
            robots = copy(state.robots)
            robots[robot] += 1
            remaining = state.minutes - numRounds
            if remaining >= 0:
                #print('Can produce new robot ', robot, ' in ', numRounds)

                newStates.append(State(res, robots, remaining))
    
    if len(newStates) == 0:
        newStates.append(doNothing)
        
    m = 0
    for s in newStates:
        #print('Queuing new state', s)
        maxGeode = simulate(blueprint, s)
        if maxGeode > m:
            m = maxGeode
    
    #CACHE[state] = m
    if m > curBest: 
        curBest = m
        print(curBest, state, len(CACHE))
    
    
    return m
    # Decide which robot to build if possible
    
    # Branch out into each possible new state
    

# total = 0
# for bp in bps:
#     CACHE = dict()
#     m = simulate(bp, State({'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}, {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}, 24))
#     total += bp.id * m
# print(total)

p2 = 1
for bp in bps[0:3]:
    CACHE = dict()
    curBest = 0
    m = simulate(bp, State({'ore': 0, 'clay': 0, 'obsidian': 0, 'geode': 0}, {'ore': 1, 'clay': 0, 'obsidian': 0, 'geode': 0}, 32))
    p2 *= m
    print(m)
    
print(p2)
