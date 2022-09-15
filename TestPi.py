# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:15:52 2022
@authors: landon, Alvin, Aidan
"""
import math


#Euclid's Algorithim
#Public Key Generation
def pubKeyGen(p,q):
   n = p*q
   e = 0
   phi = (p-1)*(q-1)

   for x in range(phi):
       if(math.gcd(x,phi) == 1 and x > 1):
          e = x
          break
   return(e,n,phi)

#Extended Euclid's algorithm
#Private Key Generation
def privKeyGen(e, phi):
    d_old = 0; r_old = phi
    d_new = 1; r_new = e
    while r_new > 0:
        a = r_old // r_new
        (d_old, d_new) = (d_new, d_old - a * d_new)
        (r_old, r_new) = (r_new, r_old - a * r_new)
    return d_old % phi if r_old == 1 else None


def main():
    p = 1
    q = 1
    n = 1
    e = 1
    phi = 1
    d = 1
    