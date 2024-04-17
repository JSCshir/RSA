import sympy
import random


def create_public_key(p: int, q: int): # returns e, n
    def euler_phi_efficient(n):
        result = n
        p = 2
        while p * p <= n:
            if n % p == 0:
                while n % p == 0:
                    n //= p
                result -= result // p
            p += 1
        if n > 1:
            result -= result // n
        return result

    n = p * q
    phi_n = euler_phi_efficient(n)
    
    primes = list(sympy.primerange(2, n))
    
    coprime_primes = [prime for prime in primes if sympy.gcd(prime, phi_n) == 1]
    
    if not coprime_primes:
        raise ValueError("No valid prime found for e that is coprime to phi(n)")
    e = random.choice(coprime_primes)

    return e, n




def digitalize(mess: str): # returns message
    message = [format(ord(char), '08b') for char in mess]
    return message




def RSA_E(public_key: tuple, message: list): # returns message
    e, n = public_key
    for i in range(len(message)):
        message[i] = (message[i] ** e) % n
        
    return message
    
    
    
def RSA_D(private_key: tuple, encrypted_message: list): # returns message
    n, d = private_key
    decrypted_message = [(c ** d) % n for c in encrypted_message]
    return decrypted_message



def asciize(mess: list): # returns message
    message = ''.join(chr(int(binary, 2)) for binary in mess)
    return message



def find_possible_private_keys(n: int, e: int): # returns d

    factors = sympy.ntheory.factorint(n)
    if len(factors) != 2 or any(factors.values()) != 1:
        raise ValueError("n must be a product of two distinct primes")
    
    primes = list(factors.keys())
    p, q = primes[0], primes[1]

    phi_n = (p - 1) * (q - 1)
    

    d = sympy.mod_inverse(e, phi_n)
    
    if d is None:
        return []
    
    return d


"""
How to send:::
    1) create your public key (insert 2 prime numbers)
    2) now digitalize your message (input your message as a string)
    3) now you may encrypt using the public key and the message as your inputs
    4) send :)
    
How to recieve:::
    1) decrypt by inputing the private key and the message
        1a) if you do not have the private key, attempt to find it using the find_possible_private_keys by inputting the public key
    2) asciize the message to read
    3) done :)
"""