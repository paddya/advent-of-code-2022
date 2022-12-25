import math
import sys


def fromSnafu(snafu):
    exp = len(snafu) - 1
    
    mapping = {
        '0': 0,
        '1': 1,
        '2': 2,
        '-': -1,
        '=': -2
    }
        
    total = 0
    for digit in snafu:
        decimal = mapping[digit]
        total += decimal * 5**exp
        exp -= 1
    return total
        

# Computes the maximum number that can be formed with all exponents 0 <= exp < maxExponent
def exclusiveMax(maxExponent):
    return sum(2*(5**exp) for exp in range(maxExponent))

EXMAX = dict()
for i in range(100):
    EXMAX[i] = exclusiveMax(i)

def toSnafu(num):
    curExp = 0
    
    # Compute the maximum exponent required first
    while True:
        localMax = EXMAX[curExp]
        # The previous exponent was good enough, since we are now over
        if localMax >= abs(num):
            curExp = curExp - 1
            break
        curExp += 1
        
        
    mapping = {
        -2: '=',
        -1: '-',
        0: '0',
        1: '1',
        2: '2'
    }
    
    # Start with the number itself, then find each digit from left to right and subtract digit * 5**curExp every time
    rem = num
    digits = []
    while curExp >= 0:      
        absRem = abs(rem)
        digit = 0
                
        # There probably is a solution without a loop here...
        while EXMAX[curExp] < absRem - digit*5**curExp:
            digit += 1

        if rem < 0:
            digit *= -1
        rem = rem - digit*5**curExp
        
        digits.append(mapping[digit])
        curExp -= 1
        
    return ''.join(digits)
    
    
 
# Roundtrips a decimal number and checks if the result matches   
def roundTrip(num):
    snafu = toSnafu(num)
    print(str(num), ' => ', snafu)
    return fromSnafu(snafu) == num

print(toSnafu(sum(fromSnafu(l) for l in open(sys.argv[1]).read().split('\n'))))