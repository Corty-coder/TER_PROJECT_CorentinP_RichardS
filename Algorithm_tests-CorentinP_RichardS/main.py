#! /usr/bin/env python3

import naive_factorization_test_to_find_best
import eratosthene_test

choice=0
while choice<1 or choice>2 :
    print("\n\n\tQuel algorithme voulez-vous executer ?")
    print("\n 1 - Algorithme permettant de tester la meilleur méthode pour la factorisation naive")
    print(" 2 - Algorithme comparant l'utiliter du crible d'Érathostène pour tester la primalité d'un nombre")
    choice=int(input("\n : "))

if choice == 1:
	bound=int(input("\nFaire le test jusqu'à la borne :"))
	naive_factorization_test_to_find_best.main(bound)
elif choice == 2:
	bound=int(input("\nFaire le test jusqu'à la borne (max = 4761) :"))+1
	eratosthene_test.main()