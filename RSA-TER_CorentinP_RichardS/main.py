#! /usr/bin/env python3

import RSA_encrypt
import RSA_generate_decrypt

choice=0
while choice<1 or choice>2 :
    print("\n\n\tQuel algorithme voulez-vous executer ?")
    print("\n 1 - Générer une clef RSA et décrypter le cryptogramme qui sera encrypter avec cette clef.")
    print(" 2 - Recevoir une clef publique RSA et encrypter un message.")
    choice=int(input("\n : "))

if choice == 1 :
	RSA_generate_decrypt.main()
elif choice == 2 :
	RSA_encrypt.main()