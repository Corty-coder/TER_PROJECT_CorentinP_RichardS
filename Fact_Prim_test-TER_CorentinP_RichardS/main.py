#! /usr/bin/env python3

import adapted_pivot
import Fermat_primality_test
import naive_factorization
import naive_primality_test
import Pollard_rho
import quadratic_sieve

from time import time

choice=0
while choice<1 or choice>5 :
    print("\n\n\tQuel algorithme voulez-vous executer ?")
    print("\n 1 - Test de primalité naïf")
    print(" 2 - Test de primalité de utilisant le petit théorème de Fermat")
    print(" 3 - Algorithme de factorisation naïf")
    print(" 4 - Algorithme de factorisation - Rho de Pollard")
    print(" 5 - Algorithme de factorisation - Crible quadratique")
    choice=int(input("\n : "))
    
print("\n","="*50,"\n\n")
if choice == 1 :
    print("Test de primalité naïf.")
    N=int(input("Entier à tester : "))
    t=time()
    test=naive_primality_test.main(N)
    if test==N or test==1 :
        print("\nN est premier.")
    else :
        print("\nN est composé.")
elif choice == 2 :
    print("Test de primalité utilisant le petit algorithme de Fermat.")
    N=int(input("Entier à tester : "))
    p=float(input("Précision désirée (i.e. 1-<marge d'erreur>) entre 0 et 1 : "))
    t=time()
    print("\n",Fermat_primality_test.fermat(N,p))
elif choice == 3 :
    print("Algorithme de factorisation naif.")
    N=int(input("Entier à factoriser : "))
    t=time()
    print(N,"=",naive_factorization.main(N))
elif choice == 4 :
    print("Algorithme de factorisation - Rho de Pollard")
    N=int(input("Entier à factoriser : "))
    t=time()
    N1=Pollard_rho.rho_pollard(N)
    print(N,"=",N1,"*",N//N1)
elif choice == 5 :
    print("Algorithme de factorisation - Crible quadratique")
    N=int(input("Entier à factoriser : "))
    t=time()
    quadratic_sieve.main(N)

print("\t\t\t\t execution time : ",time()-t,"s.")
    
    