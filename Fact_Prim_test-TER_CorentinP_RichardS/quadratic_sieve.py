#! /usr/bin/env python3
'''This algorithm is a simplified version of the quadratic sieve.'''

import naive_factorization as factorize
from adapted_pivot import linear_solution
from random import randint
from itertools import count
from math import sqrt , log2
from time import time , sleep

def Classic_Writing(F):
	'''Return a more human-friendly vision of the factors found.'''
	i=0
	L=[]
	for prime,mult in F.items():
		if i==0:
			L.extend([str(prime),"^",str(mult)])
		else :
			L.extend([" * ", str(prime) , "^" , str(mult)])
		i+=1
	return ''.join(L)

def PI(B) :
	'''Returns the number of primes lower than B.'''
	return len(Eratosthene(B))

def Eratosthene(B):
	'''Returns the prime numbers between 2 and B.'''
	L=list(range(2,B+1))
	T=[]
	S=[]
	for i in range(len(L)) :
		T.append(True)
	for i in range(len(L)//2):
		if T[i]==True :
			for j in range(i+L[i],len(L),L[i]) :
				T[j]=False
	for i in range(len(L)):
		if T[i]==True:
			S.append(L[i])
	return S

def Step_1(N,B,depth,Old_dict) :
	'''Create a dictionary of factorized number of the form "m^2 - N" for m>sqrt(N).'''
	Q = lambda m : m**2-N
	D=dict(Old_dict)
	sqrt_N=int(N**.5)+1

	for m in count(sqrt_N):
		if m not in Old_dict.keys() :
			Q_tmp=Q(m)
			F_tmp=factorize.main(N=Q_tmp,PT="PTB",return_brut=True)
			D[m]=F_tmp
			if Check(Q_tmp) :
				return Fermat(m,Q_tmp)
			elif m>sqrt_N+25*depth:
				break
	return D

def Step_1_neg(N,B,depth,Old_dict) :
	'''Same as Step_1 but with -1 as factor.'''
	Q = lambda m : m**2-N
	D=dict(Old_dict)
	sqrt_N=int(N**.5)

	for m in range(sqrt_N,0,-1):
		if m not in Old_dict.keys() :
			Q_tmp=Q(m)
			F_tmp=factorize.main(N=Q_tmp,PT="PTB",return_brut=True)
			D[m]=F_tmp
			if m<sqrt_N-25*depth:
				break
	return D

def Check(Q):
	'''A check function that is aim to stop the loop of the Step_1.	'''
	if sqrt(Q)==int(sqrt(Q)):
		return True
	else :
		return False

def Fermat(a,b) :
	F1=int(a)-int(sqrt(b))
	return (F1,a,b)

def rm_not_B_smooth(Old_dict,B):
	'''Remove the numbers in D that are not B-smooth.'''
	L=[]
	D=dict(Old_dict)
	Erat=Eratosthene(B)
	for Q in D.keys() :
		for primes in D[Q].keys() :
			if primes >= B :
				L.append(Q)
				break
	for Q in L :
		del(D[Q])
	return D,Erat

def is_B_smooth(D_value,B) :
	'''Return true if D_value is B-smooth.'''
	for prime in D_value.keys() :
		if prime > B :
			return False
	return True

def Create_Array(D,B) :
	'''Creates an array with exponents of the primes in the base of the prime lower or equal to B.'''
	A=[]
	for Q in D.keys() :
		L=[Q]
		for i in [-1]+Eratosthene(B) :
			if i in D[Q].keys() :
				L.append(D[Q][i]%2)
			else :
				L.append(0)
		A.append(L)
	return A

def remove_empty_column(Array,f_base) :
	irrelevant_factors_index=[]
	for i in range(1,len(f_base)+1) :
		irrelevant=1
		for j in range(len(Array)):
			if Array[j][i] :
				irrelevant=0
				break	
		if irrelevant :
			irrelevant_factors_index.append(i)
			
	for i in irrelevant_factors_index[::-1] :
		for factors in Array :
			factors.pop(i)
		f_base.pop(i-1)
	return Array,f_base

def weight(n,array,step_1_dict,bound,f_base,margin) :
	Q = lambda m : m**2-n
	weight_array=[[' m ']]
	for prime in f_base[1:] :
		i=1
		while prime**i < bound :
			weight_array[0].append(prime**i)
			i+=1
	weight_array[0].append('sum')
	weight_array[0].append('log2')
	weight_array[0].append('difference (ratio)')
	i=0
	for number in step_1_dict.keys() :
		i+=1
		weight_array.append([number])
		for div in weight_array[0][1:-3] :
			if Q(number)%div==0 :
				weight_array[i].append(round(log2(div)))
			else :
				weight_array[i].append(0)
		s=sum(weight_array[i][1:])
		weight_array[i].append(s)
		weight_array[i].append(round(log2(abs(Q(number)))))
		weight_array[i].append((abs(weight_array[i][-1]-weight_array[i][-2]))/weight_array[i][-1])
	print("\n\t The weights are :")
	for line in weight_array :
		print(line)
	print("\n\t The following numbers have a difference (ratio) <=",margin,":")
	kept_numbers=[]
	for line in weight_array[1:] :
		if line[-1]<=margin :
			kept_numbers.append(line[0])
	print(kept_numbers)
	return [line for line in array if line[0] in kept_numbers]

def XY(D,A,S,N):
	X,Y=1,1
	total_prime_exp={}
	for i in range(len(S)) :
		if S[i]:
			X*=A[i][0]
			for prime,exp in D[A[i][0]].items() :
				# Y*=prime**exp
				if prime in total_prime_exp :
					total_prime_exp[prime]+=exp
				else :
					total_prime_exp[prime]=exp

	if -1 in total_prime_exp :
		del(total_prime_exp[-1])

	for prime,exp in total_prime_exp.items() :
		Y*=prime**(exp//2)

	return X%N,Y%N

def gcd(A,B):
	'''Return the qcd of A and B (integers).'''
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

def Non_trivial_factor(N,B,Sign,depth,Old_dict,start_time) :
	'''Return a non trivial divisor if possible.'''
	print("\n\n","="*100,"\n\t\t\t/!\\ - RETRYING WITH NEW PARAMETERS - /!\\\n","="*100,sep='')
	if Sign == "pos" :
		return main(N,B,"neg",depth,Old_dict,start_time)
	else :
		depth+=1
		if B<500 :
			return main(N,B+15,"pos_neg",depth,Old_dict,start_time)
		else :
			if depth < 999 :
				return main(N,B,"pos_neg",depth,Old_dict,start_time)
			else :
				return -1

def main(N=89394290864773,B=20,Sign="pos",depth=1,Old_dict={},start_time=0, timeout=0):
	'''
n : 	The number you want to run a primality test with or the number you want to factorize.
B : 	Smooth bound.
time :	The program stops if the timeout is exceeded. if timeout == 0 , endless run (within depth limit).
	'''
	#5917 					ok
	#213423564 				ok
	#4811383223				ok
	#89394290864773				ok = 9996263 * 8942771 ; execution time :  176.23433208465576 s.
	#2**(2**5)-1=4294967295 	ok
	if depth==1 :
		start_time=time()
	elif time()-start_time>=timeout and timeout>0:
		return -1,[]


##############################################################################################################################################################
#1 -

	if Sign == "pos" :
		D=Step_1(N,B,depth,Old_dict)
	elif Sign == "neg" :
		D=Step_1_neg(N,B,depth,Old_dict)
	else :
		D=Step_1(N,B,depth,Old_dict)
		if type(D)==dict :
			D2=Step_1_neg(N,B,depth,Old_dict)
			for K,V in D2.items() :
				D[K]=V
			del(D2)

	if type(D)==dict :
		smooth_D,f_base=rm_not_B_smooth(D,B)
		f_base=[-1]+f_base
		#printing
		print("\n\n\t List of numbers found in step_1, after having the non-",str(B),'-smooth removed :',sep='')
		if len(smooth_D.keys())!=0 :
			A=Create_Array(smooth_D,B)
			for K in smooth_D.keys():
				print(str(K)+'^2 -',N, '\t= ',K**2-N,'\t= ',Classic_Writing(smooth_D[K]))
		else :
			A=[]
			print("\t\t None of these are ",str(B),'-smooth.',sep='')



##############################################################################################################################################################



		#printing
		if A!=[] :
			print("\n\n\t Matrix of exponents mod(2) :\n A =")
			for a in A :
				print('|',' '.join(list(map(lambda x : str(x),a))),'|')
			print("\nbase :",'(',' '.join(list(map(lambda x : str(x),f_base))),')')
			if len(A)>1:
				A,f_base=remove_empty_column(A,f_base)
				print("\n\n\t Matrix of exponents mod(2) cleaned up (no white column) :\n A =")
				for a in A :
					print('|',' '.join(list(map(lambda x : str(x),a))),'|')
				print("\nbase :",'(',' '.join(list(map(lambda x : str(x),f_base))),')')
		else :
			print("\n\n\t The matrix A of exponents mod(2) is empty with these parameters.")



##############################################################################################################################################################



		if len(A)>1 :
			print("\n\n","-"*100,"\n",sep='')
			print("\t Giving weight to numbers in order to keep the more useful before trying to find a solution...")
			A=weight(N,A,smooth_D,B,f_base,margin=0.3)
			A,f_base=remove_empty_column(A,f_base)
#			print(weights)
			print("\n\t Finally, there are the following numbers remaining :\nA =")
			for a in A :
					print('|',' '.join(list(map(lambda x : str(x),a))),'|')
			print("\nbase :",'(',' '.join(list(map(lambda x : str(x),f_base))),')')



##############################################################################################################################################################



		if len(A) > 1 :
			print("\n\n","-"*100,"\n",sep='')
			print("\t Trying to find a linear combination of the form : A^t * S = (0)")

			S = linear_solution([a[1:] for a in A])
			if not 1 in S :
				print("S = ",S)
				return Non_trivial_factor(N,B,Sign,depth,D,start_time) # Try again with different parameters.
			Sol=[A[i][0] for i in range(len(A)) if S[i]]
			D_Sol={}
			for i in range(len(S)) :
				if S[i]:
					for prime,exp in D[A[i][0]].items() :
						if prime in D_Sol.keys() :
							D_Sol[prime]+= exp
						else :
							D_Sol[prime]=exp
			print("\n\t Solution found :")
			print("S = ",S)
			print("i.e. : ",Sol)
			print("\ni.e. : ", end='')
			print(" ( ",sep='',end='')
			for nb in Sol :
				print(nb,'{}'.format('*' if nb!=Sol[-1] else ''),sep='',end='')
			print(" )^2 = ",sep='',end='')
			print(Classic_Writing(D_Sol)," mod({})".format(N))
			print("\n","-"*100,sep='')
		else :
			print("\n\n\t No solution found with these parameters.")
			return Non_trivial_factor(N,B,Sign,depth,D,start_time) # Try again with different parameters.



##############################################################################################################################################################




		X,Y=XY(D,A,S,N)
		#printing
		print("\n\nLet's X \t= ",sep='',end='')
		print(" ( ",sep='',end='')
		for nb in Sol :
			print(nb,'{}'.format('*' if nb!=Sol[-1] else ''),sep='',end='')
		print(" ) mod(N) \t\t= ", X,sep='')
		print("Let's Y \t= sqrt( ", Classic_Writing(D_Sol), " ) mod(N)\t= ",Y, sep='')



##############################################################################################################################################################




		F=gcd(X-Y,N)
		#printing
		print("\n\n\t Compute the GCD :")
		print("GCD( X-Y , N ) =",F)
		if F!= 1 and F!=N :
			print("\n\n\t Factor",F,"found !")
		else :
			return Non_trivial_factor(N,B,Sign,depth,D,start_time) # Try again with different parameters.

	else :
		#D=D_tmp
		print("\n\tSquare found !")
		print("\n\n\tWe have : X^2 - N = Y^2")
		print("\n\t ", D[1] , "^2 - ",N," = ", int(sqrt(D[2])), "^2", sep='')
		print("\n\n Returning solution : N = (X-Y) * (X+Y) ")
		F=D[0]

	if F==1 :
		F=N

	print("\n\n\n","*"*100,sep='')
	print("\n\t\tN = {} = {} * {}\n".format(N,F,N//F))
	print("*"*100,"\n\n\n",sep='')
	return F

if __name__=="__main__":
	print("\n","="*100,"\n\n\t\t\t\tQUADRATIC SIEVE ALGORITHM\n\n","="*100,sep='')
	print("\t by Corentin P. and Richard S.")
	N=input("\n\n Number to factorize : ")
	T=time()
	if N=='' :
		F=main()
	else :
		F=main(int(N))
	if F==-1:
		print("\n\n\t After all this work, no solution could have been found.")
		print("\n The algorithm must continue to grow !\n\n")
	T=time()-T
	print("\t\t\t\t\t\t execution time : ",T,"s.")
