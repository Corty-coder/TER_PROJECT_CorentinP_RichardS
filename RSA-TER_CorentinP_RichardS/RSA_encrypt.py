#! /usr/bin/env python3
from random import randint
import os

def random_prime(mini=5000,maxi=10000):
	#max(maxi)=10.000
	p=randint(mini,maxi)
	with open('list_of_primes_up_to_104743','r') as primes :
		prime=primes.read()
		prime=prime.split('\n')
		p=prime[p]
	return int(p)

def gcd(a,b):
	'''
Returns gcd(a,b) using the Euclidean algorithm.
	'''
	if a==0 or b==0:
		return(a if b==0 else b)
	else:
		r=a%b
		b_tmp=min(a,b)
		while r!=0:
			b_tmp=r
			r=a%b
			a=b
			b=r
		return b_tmp

def egcd(m,n) :
	'''
Extanded Euclidean algorithm.
m stands for the number to invert
n stands for tho modulus
requierment : n>m ; gcd(m,n)=1
	'''
	#https://fr.wikipedia.org/wiki/Algorithme_d%27Euclide_%C3%A9tendu
	(r, u, v, r1, u1, v1) = (m, 1, 0, n, 0, 1)
	while r1 != 0 :
		q=r//r1
		(r,u,v,r1,u1,v1)=(r1,u1,v1,r-q*r1,u-q*u1,v-q*v1)
	return u%n

def choose_e(phi) :
	e = randint(2,phi-1)
	forbiden_e=[]
	while gcd(e,phi) != 1 :
		forbiden_e.append(e)
		e = randint(2,phi-1)
		if e in forbiden_e :
			e+=1
	return e

def str_to_int(text) :
	number=''
	for character in text :
		c=str(ord(character))
		while len(c)<3 :
			c='0'+c
		number=number+c
	return number

def encrypt(clear,public_key) :
	clear=clear
	e,n=public_key
	clear_splitted=[clear[i:i+9] for i in range(0,len(clear),9)] #split by 9 int i.e. 3 letters (1)
	cipher=[]
	for m in clear_splitted :
		c=str(pow(int(m),e,n))
		while len(c)<10 : #make strings of len 10 so that it can be splitted in dectypt (2)
			c='0'+c
		cipher.append(c)
	cipher=''.join(cipher)
	return cipher


def decrypt(cipher,private_key) :
	d,n=private_key
	clear=[]
	cipher_splitted=[cipher[i:i+10] for i in range(0,len(cipher),10)]#split by 10 as in encrypt as in (2)
	for c in cipher_splitted :
		m=str(pow(int(c),d,n))
		while len(m)<9 : #make strings of len 9 i.e. 3 letters as in (1)
			m='0'+m
		clear.append(m)
	clear=''.join(clear)
	return clear

def int_to_str(number) :
	number_splitted=[number[i:i+3] for i in range(0,len(number),3)]
	text_splitted=[str(chr(int(ascii_character))) for ascii_character in number_splitted]
	return ''.join(text_splitted)

def main() :
	os.system('clear')
	#message=str_to_int(input("\n\n\t Enter the message you want to encrypt with RSA :\n\n "))

	print("\n\n","="*100," \n\n\t\t\t\t\tR . S . A .\n\t\t\t\tKEY RECEPTION AND ENCRYPTION\n\n","="*100,"\n", sep='')
	
	print("\n Note : The code divides the message by groups of 3 letters (9 numbers when converted to ASCII)\nin order to encrypt them. \nThen it reassembles the groups into one string. And does the same backwards to decipher.\n")

	# print("\n\t Here you have to copy the RSA public key you received and paste it below. Then, you will be\nable to write a message which will be encrypted with the same key. You will have to send the cipher\nthereby generated.\n")

	print("\n","="*39," encrypt a message ","="*42,"\n", sep='')
	public_key=input("\t . enter the public key you received (of the form '(e,n)'\n : ")
	public_key=public_key[1:-1].split(", ")
	e,n=int(public_key[0]),int(public_key[1])
	public_key=(e,n)

	message=str_to_int(input("\t . enter the message you want to encrypt\n : "))

	print("\t . translating you message to an integer using ASCII...")
	print(" :",message)

	print("\t . generating cipher using the public key...")
	cipher=encrypt(message,public_key)

	print("\n\t The cipher you must send in clear is :")
	print("\n",cipher,"\n\n\n")

if __name__=="__main__" :
	main()