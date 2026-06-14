import math
import re
from gmpy2 import mpz, isqrt

def pi_cruncher_bs(n):
    C = 640320  # magic number
    C3_OVER_24 = C**3 // 24
    progress = 0
    
    def update_progress():
        nonlocal progress
        progress += 1
        percent_complete = progress / n * 710  # magic number
        if percent_complete > 100:
            percent_complete = 100
        blocks = int(percent_complete / 2)
        spaces = 50 - blocks
        bar = '█' * blocks + ' ' * spaces
        print(f"Don't interupt! Computing Pi: [{bar}] {percent_complete:.2f}%", end='\r', flush=True)

    def bs(a, b):
        if b - a == 1:
            # direct computation of P(a,a+1), Q(a,a+1) and T(a,a+1)
            if a == 0:
                Pab = Qab = mpz(1)
            else:
                Pab = mpz((6*a-5)*(2*a-1)*(6*a-1))
                Qab = mpz(a*a*a*C3_OVER_24)
            Tab = Pab * (13591409 + 545140134*a)
            if a & 1:
                Tab = -Tab
                
        else:
            # recursive computation P(a,b), Q(a,b) and T(a,b)
            m = (a + b) // 2
            Pam, Qam, Tam = bs(a, m)
            Pmb, Qmb, Tmb = bs(m, b)
            Pab = Pam * Pmb  # combine everything
            Qab = Qam * Qmb
            Tab = Qmb * Tam + Pam * Tmb
            
        update_progress()
        return Pab, Qab, Tab
    
    # how many terms to compute
    digits = math.log10(C3_OVER_24/6/2/6)
    N = int(n/digits + 1)
    P, Q, T = bs(0, N)  # computation of P(0,N) and Q(0,N)
    one_squared = mpz(10)**(2*n)
    sqrtC = isqrt(10005*one_squared)
    pi = str((Q*426880*sqrtC) // T)[1:]  # hack
    
    print("\nComputation finished: Writing to a file")
    
    result = ""
    
    for i in range(0, len(pi), 50):
        # can we have faster regexes
        if i + 50 <= len(pi):
            result += re.sub(r'(.{10})', r'\1 ', pi[i:i+50]).strip() + f' : {i + 50}\n'
        else:
            result += re.sub(r'(.{10})', r'\1 ', pi[i:]).strip() + f' : {len(pi)}'
    
    return '3.\n' + result  # hack

with open("pi_digits.txt", mode='w') as file:
    file.write(pi_cruncher_bs(1000000000))
