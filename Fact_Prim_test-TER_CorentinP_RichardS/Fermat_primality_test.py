from time import time
from math import *
import random


def exponentiation(N): #algorithme pour mettre N-1 sous somme de puissances de 2
	L=[]
	N_save=N
	for k in range(int((log(N,e))/log(2,e)),-1,-1):
		M=N-2**k
		if M>=0:
			N=M
			L.append(k)
	a=0
	return(L)

def expo(a,N):
	L=exponentiation(N-1)
	prod=1
	for i in range(len(L)):
		c=1
		n=0
		gamma=2**L[i]
		while n<gamma:
			n+=1
			c=(a*c)%N
		prod=(prod*c)%N
	return(prod)


def generator(x,y):
	return(3*x+y)


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
			(b,a)=(a,generator(a,b)%N) #on génère un a
			while a==0 or a==1 or a_old==a :
				(b,a)=(a,generator(a,b)%N) #on génère un a

			if a in T :
				reset = True

			if not reset :
				T.append(a)
				y=expo(a,N)
			#y=a_puissance_expo(N_save,exponentiation(N),a) #on calcule a**(N-1)%N
				if y!=1: #Si a**(N-1)%N != 1, alors le critère est faux.
					test=1
	print(T)
	if test==0:
		return(N, " is a prime or a Carmichael Number with a probability of",p,"%")
	elif test==1:
		return(N, " is not a prime")


if __name__=="__main__" :
	print("\n\n\tPrimality test based on Fermat's theorem.\n\n")
	N=int(input("Number to test : "))
	p=float(input("Exactness desired (i.e. 1-<margin of error>) : "))
	fermat(N,p)

# a=13451
# N=3421201


# rt=2001911

# z=789002777
# d=789002775

# print(exponentiation(29))