#!/usr/bin/env python3

import naive_primality_test as PTB
import Pollard_rho as PsR
import quadratic_sieve as QS
import time

def Classic_Writing(F):
	i=0
	L=[]
	for prime,mult in F.items():
		if i==0:
			L.extend([str(prime),"^",str(mult)])
		else :
			L.extend([" * ", str(prime),"^",str(mult)])
		i+=1
	return ''.join(L)

def main(N=2, PT="PTB", return_brut=False):
	if N>= 0 :
		Factors = {}
	else :
		Factors = {-1:1}
		N=-N

	T=eval(PT).main(N=N)		
	while T!=N:
		if T in Factors :
			Factors[T]+=1
		else :
			Factors[T]=1
		N=N//T
		T=eval(PT).main(N)
		
	if N in Factors :
		Factors[N]+=1
	else :
		Factors[N]=1

	if not return_brut :
		return Classic_Writing(Factors)
	else :
		return Factors

if __name__=="__main__":
	N=int(input("\n\tnumber to factorize : "))
	factors=main(N,PT="PTB")
	print(f"the factors of {N} are :\n",factors)