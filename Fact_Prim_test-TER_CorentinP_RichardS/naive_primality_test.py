#!/usr/bin/env python3

def Eratosthene(B):
	'''Returns the prime numbers between 2 and B.'''
	L=list(range(B+1))
	T=[True] * (B+1)
	T[0]=T[1]=False

	for i in range(2,int(B**0.5)+1):
		if T[i]==True :
			for j in range(i**2,B+1,i) :
				T[j]=False
				
	S=[L[i] for i in range(len(L)) if T[i]==True]
	return S

def is_prime(N,min_prime=2) :
	if N==0:
		return 0
	elif N==1 :
		return 1
	else :
		# for i in Eratosthene(int(N**0.5)) :
		if min_prime == 2 :
			list_to_test=[2]+list(range(3,int(N**0.5)+1,2))
		else :
			list_to_test=list(range(min_prime,int(N**0.5)+1,2))

		for i in list_to_test :
			if N%i==0 : 
				return i
		return N
		
def main(N,min_prime=2) :
	return is_prime(N,min_prime)

if __name__=="__main__":
	N=6709616788079
	factor = main(N)
	print(f"\n\tThe smallest factor of {N} is {factor}.")
