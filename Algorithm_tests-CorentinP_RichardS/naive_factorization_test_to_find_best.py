from time import time,sleep

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

def factor1(N):
	Factors={}
	T=is_prime(N)
	while T!=N:
		if T in Factors :
			Factors[T]+=1
		else :
			Factors[T]=1
		N=N//T

		if Factors != {} and Factors != {-1:1} :
			T=is_prime(N=N,min_prime=list(Factors.keys())[-1])#On envoie le plus petit grand facteur trouvé, car il n'y a pas besoin de faire des test avec des entiers plus petits : on sait qu'il ne marcheront de toutes facons pas.
		else :
			T=is_prime(N)
		
	if N in Factors :
		Factors[N]+=1
	else :
		Factors[N]=1
	return Factors

def factor2(N):
	L=Eratosthene(int(N**0.5))
	# L=[2]+list(range(3,int(N**0.5)+1,2))
	Factors={}
	for l in L :
		if N%l==0 :
			Factors[l]=1
			N=N//l
			while N%l==0 :
				N=N//l
				Factors[l]+=1
		if N==1 :
			break
	if N!=1:
		Factors[N]=1
	return Factors

def factor3(N):
	# L=Eratosthene(int(N**0.5))
	L=[2]+list(range(3,int(N**0.5)+1,2))
	Factors={}
	for l in L :
		if N%l==0 :
			Factors[l]=1
			N=N//l
			while N%l==0 :
				N=N//l
				Factors[l]+=1
		if N==1 :
			break
	if N!=1:
		Factors[N]=1
	return Factors

def main(bound=1000000) :
	mean1=0
	mean2=0
	mean3=0
	j=0
	for N in Eratosthene(bound) :
		print(N)
		if factor1(N) != factor2(N) :
			sleep(10)
		t=time()
		factor1(N)
		mean1+=time()-t

		t=time()
		factor2(N)
		mean2+=time()-t
		
		t=time()
		factor3(N)
		mean3+=time()-t

		if factor1(N) != factor2(N) or factor1(N) != factor3(N) or factor3(N) != factor2(N) :
			sleep(10)

		j+=1

	print("\n\nmethod 1-",round(mean1/j*10000,4),"e-4")
	print("method 2-",round(mean2/j*10000,4),"e-4")
	print("method 3-",round(mean3/j*10000,4),"e-4")


if __name__=="__main__" :
	main()

		