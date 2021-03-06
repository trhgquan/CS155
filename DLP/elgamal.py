from utils.bigmod import BigMod
from utils.xeuclidean import XEuclidean
from dh import DiffieHellman
import random

class Elgamal(DiffieHellman):
    @staticmethod
    def generate_key(p : int) -> tuple:
        '''Generate Elgamal key

        Input:
            - p : (Z_p)
        
        Output:
            - p : (Z_p)
            - g : generator of (Z_p)
            - d : decryption key (private)
            - e : encryption key (public)
        '''
        p, g = DiffieHellman.generate_key(p)
        d = random.randrange(2, p - 1)
        e = BigMod.power(g, d, p)
        return (p, g, d, e)

    @staticmethod
    def encrypt(message : str, e : int, p : int, g : int) -> tuple:
        '''Encrypt a message, using ElGamal

        Input:
            - message : message to encrypt
            - e : encryption key
            - p : (Z_p)
            - g : generator of (Z_p)
        
        Output:
            - c1, c2 : pair of cipher generated by ElGamal
        '''
        x = random.randrange(2, p - 1)
        c1 = BigMod.power(g, x, p)
        c2 = [BigMod.mul(c, BigMod.power(e, x, p), p) for c in Elgamal.encode(message)]

        return (c1, c2)

    @staticmethod
    def decrypt(d : int, c1 : int, c2 : list, p : int) -> str:
        '''Decrypt a cipher message, using ElGamal

        Input:
            - d : Decryption key
            - c1, c2 : pair of cipher
            - p : (Z_p)
        
        Output:
            - Decrypted string
        '''
        inverse_c1 = XEuclidean.inverse_modulo(BigMod.power(c1, d, p), p)
        return Elgamal.decode([BigMod.mul(inverse_c1, int(c), p) for c in c2.rstrip().split(' ')])
