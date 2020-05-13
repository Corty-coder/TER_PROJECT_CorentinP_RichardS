# TER_PROJECT_CorentinP_RichardS
factorization algorithms, primality test algorithms and RSA encrypting and deciphering algorithm. All written in python. For our research project.

naive_primality_test.py :   a simple primality test using Eratosthenes sieve.
naive_factorization.py :    a simple factorazation algorithm, using the above algorithm. Also used in further algorithms (such as quadratic_sieve.py

Pollard_s_Rho.py :          Pollard's Rho factorization algorithm.

adapted_pivot.py :          linear regrassion algorithm adapted to take an n*m matrix M with componant living in Z/2Z as input and outputs a linear solution S such as M^T*S=(0).
quadratic_sieve.py :        quadratic sieve factorization algorithm. Uses the above "adapted_pivot" and "naive_factorization" algorithms.

RSA_encrypt_derypt.py :     RSA encrypting and deciphering algorithm. Uses the pre-generated "list_of_prime". This algorithm is used when testing the quadratic_sieve algorithm.
