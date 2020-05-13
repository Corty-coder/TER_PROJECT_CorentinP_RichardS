#!/usr/bin/python

'''
if FACT == 1 :
	return the first prime factor encountered
else :
	return 1 if prime else 0
'''
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

def is_prime(N) :
	if N==0:
		return 0
	elif N==1 :
		return 1
	else :
		for i in Eratosthene(int(N**0.5)) :
			if N%i==0 : 
				return i
		return N


def main(N=213141) : #AFFICHER LES MESSAGES UNIQUEMENT LORS D'UNE ENTREE PAR L'UTILISATEUR, SINON RETOURNER LA REPONSE A "N EST IL PREMIER ?"
		return is_prime(N)

if __name__=="__main__":
	main()
