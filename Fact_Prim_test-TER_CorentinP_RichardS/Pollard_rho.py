from math import *
from time import time

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


def f(x,c):
	return x**2+c	


def rho_pollard(n=2921, s=2):
	(x_i,x_2i)=(s,s)
	c=1
	g=1
	timer=time()

	while g==1 or g==n:
		(x_i,x_2i)=(f(x_i,c)%n,f(f(x_2i,c),c)%n)
		g=gcd((x_i-x_2i)%n,n)

		if g==n:
			c+=2

		t=time()-timer

		if t>200:
			g=rho_pollard(n,int(2+random()*(n-3)))

	return(g)


if __name__=="__main__" :
	print("\n\n\tFactorization algorithm -- Pollard's Rho.\n\n")
	N=input("Number to factorize : ")
	print("A factor of",N,"is",rho_pollard(N))