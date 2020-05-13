#! /usr/bin/env python3
from time import time
from random import randint

def print_matrix(matrix) :
	'''
	Affiche une liste de liste sous forme d'une matrice.
	'''
	print('-'*50+"\nM =")
	for m in matrix :
		print(m)
	print('\n'+'-'*50)

def random_matrix(n,m) :
	'''
	Renvoie une matrice de taille aléatoire entre n*n et m*m (carree ou non) de 0 et de 1.
	'''
	n,m=randint(n,m),randint(n,m)
	matrix=[[randint(0,1) for i in range(n)] for j in range(m)]
	return matrix


def linear_solution(A,file=0):
	''' Pivot de gausse adapté pour fonctionner avec une matrice rectangulaire arbitraire mod(2).
	input : matrice A de taille arbitraire mod(2)
	output : solution linéaire S telle que A^T*S=0'''
	class SolutionError(ValueError):
		'''Trying to attribute a different value to an already fixed variable.'''

	def transpose(matrix) :
		''' Renvoie la transposée d'une matrice donnée.'''
		transposed_matrix=[[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]
		return transposed_matrix

	def pivot(matrix) :
		''' 
		Ceci est l'actuel pivot de Gauss adapté avec une matrice rectangulaireoù les coefficients sont modulo 2.
		'''
		def sort(matrix) :
			'''
			Algorithme de tri. 
			Il est ajouté après chaque ligne un nombre qui représente le nombre de 0 avec le premier 1 (en partant de la gauche). 
			Puis un tri par ordre croissant est fait du haut vers le bas en utilisant ces nombres : 
				-> la ligne avec le plus petit nombre (le moins de 0 à gauche) est la première, etc.
			Enfin, ca dernière colonne est supprimée.
			'''
			for row in matrix :
				zeros=0
				for m in row :
					if m==0 :
						zeros+=1 											#on compte le nombre de 0 avant de rencontrer un 1
					else :
						break
				row.append(zeros)											#on ajouter le nombre le nombre de 0 au bout de la ligne.
			#bubble sort START #### (Algorithme bubble sort, pas le plus efficace mais compte tenu du "petit" jeu de donnés que nous manipulons, il est suffisant.) exemple de bubble sort : https://www.youtube.com/watch?v=Cq7SMsQBEUw
			sorted_row=0 #on compte le nombre de ligne triées
			while sorted_row<len(matrix) : 									#tant que toutes les lignes ne sont pas triées
				for i in range(len(matrix)-sorted_row-1):
					if matrix[i][-1] > matrix[i+1][-1] :					#on compare la ligne i avec la suivante, si elle comporte plus de 0
						matrix[i], matrix[i+1] = matrix[i+1], matrix[i]	  	#alors on les inverse
				sorted_row+=1												#quand un premier "balayage" à été fait, on sait qu'au moins ligne avec le plus de 0 est à sa place, etc.
			#bubble sort END
			matrix=[m[0:-1] for m in matrix]								#on enlève la dernière colonne
			return matrix

		def eliminate(matrix,row,column) :
			'''
			Prend en entrée la matrice, une line et une colonne.
			L'algorithme balaille toute la matrice de haut en bas (par ligne) --sauf la ligne qu'il a eu en entrée-- :
			si une ligne à un 1 sur la colonne donnée en entrée, alors il soustrait (mod 2) la ligne donnée en entrée à la ligne courante.

			L'idée est d'utiliser cet algorithme en meme temps qu'un "balayage" horizontale, de gauche à droite ;
			ainsi, chaque élément de la matrice donné en entrée (matrix[row][column]) est un pivot, et on fait donc bien l'algorithme du pivot de Gauss.

			La subtilité ici est qu'en plus de faire la différence des lignes sous le pivot (pour échelonner la matrice),
			on fait aussi cette différence au dessus (pour réduire la matrice).
			'''
			def subtract(row1,row2):
				'''Soustraction de deux listes (deux lignes d'une matrice).'''
				row1=[(row1[i]+row2[i])%2 for i in range(len(row1))]
				return row1

			for i in range(len(matrix)) :
				if i != row :
					if matrix[i][column] == 1 :
						matrix[i]=subtract(matrix[i],matrix[row])
			return sort(matrix)

		if matrix==[] : return matrix

		row=0 #initialisation à l'élément 0,0
		column=0 
		eliminated=False #variable dééfinissant si la matrice est sous forme echelonnee reduite
		while column<len(matrix[0]) and row<len(matrix) and not eliminated :
			matrix=sort(matrix) #tri des lignes
			while matrix[row][column]==0 :
				column+=1 #on avance sur la droite de la matrice pour une ligne donnée jusqu'à rencontrer un 1
				if column >= len(matrix[0]) : #on arrête si on a atteint la dernière colonne, cela signifie que la matrice est echelonnee reduite.
					eliminated=True
					break
			if eliminated==False: #si la matrice n'est pas echelonnee
				matrix=eliminate(matrix,row,column) #alors on soustraint la ligne en cours à toutes les lignes qui ont un 1 sur la colonne en cours.
			row+=1 #on passe à la ligne suivante
			column+=1 #colonne suivant également
		return matrix

	def solution(matrix) :
		'''
		L'algorithme 'déduit' une solution compte tenu de la matrice échelonnée réduite.
		'''
		def remove_empty(matrix) :
			row_to_remove=[]
			for i in range(len(matrix)) : #on parcours les lignes de la matrice
					if sum(matrix[i]) == 0 :
						if i not in row_to_remove : row_to_remove.append(i)
			row_to_remove.sort(reverse=True)

			for i in row_to_remove :
				matrix.pop(i)
			return matrix

		def one(matrix,combi,run_TOM) :
			'''
			L'algorithme se contente de gérer les lignes un seul 1.
			Si il y a un seul 1 dans la ligne alors la variable en même position vaut 0.
			Une fois modifiée la ligne est supprimée.
			On remplace également toutes les lignes en même position que la variable vallant 0 par un 0.
			'''
			row_to_remove=[]

			still_one=True
			while still_one :
				still_one=False
				for i in range(len(matrix)) : #on parcours les lignes de la matrice
					if sum(matrix[i]) == 1 :  #si il y a un seul 1, à l'emplacement de ce 1 on met un 0 dans combi
						run_TOM=False
						still_one = True
						for j in range(len(matrix[i])) :
							if matrix[i][j]==1 :
								##################
								if combi[j] == 1 : #Erreur si on modifie la solution alors que la variable était déjà fixée.
									raise SolutionError()
								##################
								combi[j] = 0
								for row in matrix :
									row[j] = 0
								if i not in row_to_remove : row_to_remove.append(i)
								break #une fois fait, un break pour éviter de parcourir inutilement le reste de la ligne

			row_to_remove.sort(reverse=True)
			for i in row_to_remove :
				matrix.pop(i)

			return matrix,combi,run_TOM

		def two(matrix,combi,run_TOM):
			'''L'algorithme prend en charge les lignes avec deux 1.
			Les deux 1 doivent se simplifiés, il faut donc que les variables associées soient égales à 1 (car 1*1+1*1=0 mod(2)).
			Une fois les variables remplacées, la ligne est supprimée.'''
			row_to_remove=[]
			for i in range(len(matrix)) :
				if sum(matrix[i]) == 2 :  #si il y a deux 1, à l'emplacement de ces 1 on met un 1 dans combi
					if i not in row_to_remove : row_to_remove.append(i)
					j_s=[]
					for j in range(len(matrix[i])) :
						if matrix[i][j]==1 :
							j_s.append(j)

					for j in j_s :
						##################
						if combi[j] == 0 : #Erreur si on modifie la solution alors que la variable était déjà fixée.
							raise SolutionError()
						##################
						combi[j] = 1

					for  row in matrix :
						if row[j_s[0]]==row[j_s[1]]==1 :
							row[j_s[0]]=0
							row[j_s[1]]=0
					break

			if row_to_remove != [] :
				run_TOM=False

			row_to_remove.sort(reverse=True)
			for i in row_to_remove :
				matrix.pop(i)
							
			return matrix,combi,run_TOM

		def replace(matrix,combi,run_TOM=True):
			'''
			Il s'agit de compter le nombre de variables ayant pour valeur 1 dans chaque ligne/équation. Ensuite, il s'agit de remplacer ces variables 1 deux par deux (si il y a 2 variables 1, alors elles se simplifient).
			'''
			combi_save=list(combi)
			for i in range(len(matrix)):
				if sum(matrix[i]) > 2 :
					remove_even_nomber_of_one=True
					for j in range(len(matrix[i])):
						if matrix[i][j]==1 and combi[j]==1: #pour chaque 1 dans la solution, on remplace le 1 de la colonne par un 0 (on le supprime).
							run_TOM=False
							matrix[i][j] = 0
							if remove_even_nomber_of_one == True : # Il faut supprimer un nombre pair de 1.
								remove_even_nomber_of_one = False # Si une fois tous les 1 correspondant à une variable 1 dans la solution supprimés, il n'y a qu'un nombre impaire de 1 supprimés dans la ligne en cours, alors il faut en supprimer un autre (pour conserver le 0 mod(2)).
							else :
								remove_even_nomber_of_one = True
					if remove_even_nomber_of_one == False : # On supprime ici le 1 le plus à gauche sur la ligne pour qu'un nombre pair de 1 soit éliminés.
						for j in range(len(matrix[i])) :
							if matrix[i][j] == 1 :
								matrix[i][j] = 0
								##################
								print_matrix(matrix)
								if combi[j] == 0 : #Erreur si on modifie la solution alors que la variable était déjà fixée.
									raise SolutionError()
								##################
								combi[j] = 1
								remove_even_nomber_of_one=True
								break

			return matrix,combi,run_TOM

		def three_or_more(matrix,combi) :
			''' Ici, il s'agit de prendre en charge un espace vectoriel. En effet si trois 1 ou plus sont sur une ligne et ne sont pas simplifiable, c'est qu'un espace vectoriel entier de solution est possible.
			Il faut donc prendre une solution particulière.
			Si le nombre de 1 sur la ligne est pair, on fixes toutes les variables correspondantes en 1.
			Sinon, on fixe la premiere à 0 et toutes les autres à 1.'''
			for row in matrix :
				if sum(row) > 2 :
					if sum(row)%2==0: # cas pair
						for j in range(len(row)) :
							if row[j]==1 :
								##################
								if combi[j] == 0 : #Erreur si on modifie la solution alors que la variable était déjà fixée.
									raise SolutionError()
								##################
								row[j] = 0
								combi[j] = 1
					elif sum(row)%2==1: # cas impair
						zero=False
						for j in range(len(row)) :
							if row[j]==1:
								if not zero : # on remplace la première variable par un zero, puis la variable "zero" devient vraie et alors on remplecera les autres par des 1.
									zero=True
									##################
									if combi[j] == 1 : #Erreur si on modifie la solution alors que la variable était déjà fixée.
										raise SolutionError()
									##################
									combi[j] = 0
									row[j] = 0
									for line in matrix :
										if line[j] == 1 :
											line[j] = 0
								else :
									##################
									if combi[j] == 0 : #Erreur si on modifie la solution alors que la variable était déjà fixée.
										raise SolutionError()
									##################
									combi[j] = 1
									row[j] = 0
					break

			return matrix,combi


		matrix_copy=list(matrix) #on copie la matrice originale
		combi=[ None for i in range(len(matrix[0])) ] #on fixe chaque variable à 0

		while matrix_copy!=[] : #on continue tant qu'il y a des lignes non nulles dans la matrice (si la solution est trouvée alors la matrice sera vide lors du passage de la fonction "replace").
			run_TOM=False #TOM=three_or_more ; on ne lance pas la fonction "three or more" tant que des changements peuvent être faits en utilisant les autres méthodes. Cela permet de ne pas choisir une solution particulière d'un espace vecctoriel, si en fait il ne s'agit pas d'un e.v. Ce qui entrainement presque surement un conflict (on aurait une solution avec une ligne et une autre avec une autre ligne).
			matrix_copy=pivot(matrix_copy) #on refait une pivot avec la matrice, cette ligne est inutile lors de la première itération du while mais devient nécessaire pour éviter les conflicts par la suite
			while run_TOM==False :
				run_TOM=True #on propose de lancer l'algorithme three_or_more, mais cette variable restera "True" seulement si il n'y a aucun changement effectués sur la matrice au cours des prochaines étapes. Cela signifiera qu'il y a un e.v. de solution possible.
				matrix_copy=remove_empty(matrix_copy) #on enlève les lignes vides.
				# if matrix_copy==[]: #on arrete 
				# 	break
				matrix_copy,combi,run_TOM=one(matrix_copy,combi,run_TOM)
				matrix_copy,combi,run_TOM=two(matrix_copy,combi,run_TOM)
				matrix_copy=pivot(matrix_copy) #on refait un pivot pour eviter les conflicts
				matrix_copy,combi,run_TOM=replace(matrix_copy,combi,run_TOM) #on remplaces les variables connues dans la matrice
				matrix_copy=pivot(matrix_copy) #on refait un pivot pour eviter les conflicts
			matrix_copy,combi=three_or_more(matrix_copy,combi)	
			matrix_copy,combie,run_TOM=replace(matrix_copy,combi)

		combi=list(map( lambda i : 0 if i==None else i , combi )) #si la matrice est vide mais qu'il reste des "None" dans la solution, on les remplace par des 0.

		return combi

	#1- TRANSPOSITION
	M=transpose(A)
	###############
	print("TRANSPOSITION")
	print_matrix(M)
	###############	

	#3- PIVOT
	M=pivot(M)
	###############
	print("PIVOT")
	print_matrix(M)
	###############	

	#5- IMPRESSION DE LA COMBINAISON
	combi=solution(M)

	return combi


def test_solution(matrix,combi) :
	'''Algorithme permettant de tester si la solution donne bien "matrix^T*combi=(0)".'''
	def transpose(matrix) :
		transposed_matrix=[[matrix[i][j] for i in range(len(matrix))] for j in range(len(matrix[0]))]
		return transposed_matrix

	matrix=transpose(matrix)
	resultat=[]
	for i in range(len(matrix)) :
		somme=0
		for j in range(len(matrix[i])) :
			somme+= combi[j]*matrix[i][j]
		somme=somme%2
		resultat.append(somme)

	return resultat


def control(nb_of_test=1000,	min_matrix=15,	max_matrix=150, write_all=False):
	'''Algorithme de controle du pivot.
	write_all : True ="ecrire toutes les matrices et les resultats trouver dans le log" ; "False"=ecrire seulement les matrices qui menent a une erreur, une fausse 'solution'.
	nb_of_test : nombre de tests à effectuer
	min_matrix : taille minimum des matrices a tester
	max_matrix : taille maximum des matrices a tester'''

	mean_time=0
	wrong=0
	zero=0
	error=0
	with open("log_pivot"+str(time()), "w") as file :
		for a in range(nb_of_test) :
			T=time()
			try :
				matrix=random_matrix(min_matrix,max_matrix) #matrice aléatoire de taille n*m pour n et m compris aléaoirement entre 3 et 10.
				if write_all :
					file.write("test numero ="+str(a)+"\n\nM =[\n")
					for m in matrix :
						file.write(str(m)+",\n")
					file.write("]")
				combi = linear_solution(matrix,file)
				if 1 not in combi :
					zero += 1
				resultat=test_solution(matrix,combi)
				if write_all :
					file.write("\nsolution = "+str(combi))
					file.write("\nresultat = "+str(resultat))
				if 1 in resultat :
					file.write("\nWRONG\n")
					file.write("test numero ="+str(a)+"\n\nM =[\n")
					for m in matrix :
						file.write(str(m)+",\n")
					file.write("]")
					wrong+=1
				if write_all :
					file.write("\n\n"+"-"*200+"\n\n")
			except :
				error+=1
				file.write("\nERROR\n")
				file.write("test numero ="+str(a)+"\n\nM =[\n")
				for m in matrix :
					file.write(str(m)+",\n")
				file.write("]")
			finally :
				mean_time+=(time()-T)/nb_of_test

		print("\n"*10)
		print("nombre de test = "+str(nb_of_test))
		print("\nwrong = "+str(wrong)+"\t;\tratio = "+str(wrong/nb_of_test*100)+"%")
		print("if the solution found lead to M^T*S != (0).")
		print("\nerror = "+str(error)+"\t;\tratio = "+str(error/nb_of_test*100)+"%")
		print("if the solution couldn't be found.")
		print("\nzero = "+str(zero)+"\t;\tratio = "+str(zero/nb_of_test*100)+"%")
		print("if the solution found if (0...0).")
		print("\ntotal_time = "+str(mean_time*nb_of_test))
		print("")
		print("mean_time = "+str(mean_time))
		print("")

		file.write("nombre de test = "+str(nb_of_test))
		file.write("\n\nwrong = "+str(wrong)+"\t;\tratio = "+str(wrong/nb_of_test*100)+"%")
		file.write("\nif the solution found lead to M^T*S != (0).")
		file.write("\n\nerror = "+str(error)+"\t;\tratio = "+str(error/nb_of_test*100)+"%")
		file.write("\nif the solution couldn't be found.")
		file.write("\n\nzero = "+str(zero)+"\t;\tratio = "+str(zero/nb_of_test*100)+"%")
		file.write("\nif the solution found if (0...0).")
		file.write("\n\ntotal_time = "+str(mean_time*nb_of_test))
		file.write("\n")
		file.write("\nmean_time = "+str(mean_time))
		file.write("\n")

