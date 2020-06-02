from time import time
from math import *
import random

def gcd(A,B):
	'''
	A and B are integers.
	'''
	if A==0 or B==0:
		return(A if B==0 else B)
	else:
		r=A%B
		B_temp=min(A,B)
		while r!=0:
			B_temp=r
			r=A%B
			A=B
			B=r
		return B_temp

def expo_rapide(a,N,modulo):
	prod=1
	if N==1:
		return(a)
	elif N%2==0:
		c=expo_rapide((a**2)%modulo,N/2,modulo)
		prod=(prod*c)%modulo
	elif N%2==1:
		prod=(prod*a)%modulo
		c=expo_rapide((a**2)%modulo,(N-1)/2,modulo)
		prod=(prod*c)%modulo
	return prod

def generator(N,x,y):
	return(int(log2(N))*x+y)

def fermat(N,p): #Fermat
	N_save=N
	if N%2==0: #On retire les cas pairs
		return(N, " is even.")
	else:
		test=0
		i=0
		a=2
		b=1
		w=int(-log2(1-p)+1) #proba par défaut
		T=[]
		while (test==0 and i<w-1): #tant qu'on n'a pas de contre-exemple
			reset=False
			i=len(T)
			a_old=a			
			(b,a)=(a,generator(N,a,b)%N) #on génère un a

			while a==0 or a==1 or a_old==a or gcd(a,N)!=1:
				(b,a)=(a,generator(N,a,b)%N) #on génère un a

			if a in T :
				reset = True

			if not reset :
				T.append(a)
				y=expo_rapide(a,N-1,N) #on calcule a**(N-1)%N
				if y!=1: #Si a**(N-1)%N != 1, alors le critère est faux.
					test=1
	print("\nNumber 'a' tested :",T)
	if test==0:
		return(N, " is a prime or a Carmichael Number, with a probability of",p)
	elif test==1:
		return(N, " is not a prime")



if __name__=="__main__" :
	print("\n\n\tPrimality test based on Fermat's theorem.\n\n")
	N=int(input("Number to test : "))
	p=int(input("Exactness desired (i.e. 1-<margin of error>) : "))
	fermat(N,p)

