# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:15:52 2022

@author: landon, Alvin
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



def main():
    p = 1
    q = 1
    n = 1
    e = 1
    phi = 1
    d = 1
    