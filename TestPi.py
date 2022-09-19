# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:15:52 2022
@authors: landon, Alvin, Aidan
"""
import math

p = 588173
q = 961811
n = 0
e = 0
phi = 0
d = 0

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

# Extended GCD Utility
def extended_gcd(a=1, b=1):
    if b == 0:
        return (1, 0, a)
    (x, y, d) = extended_gcd(b, a%b)
    return y, x - a//b*y, d


while(True):
    #wtf is N
    e,n,phi = pubKeyGen(p,q)
    print("N is:", n)
    print("E is:", e)
    print("\n")
    print ("RSA keys have been generated.")
    
    print("Please select your user type:")
    print("\t1. A public user")
    print("\t2. The owner of the keys")
    print("\t3. Exit program ")
    
    choice = input()
    
    while(choice == "1"):
        print("As a public user, what would you like to do?")
        print("\t1. Send an encrypted message")
        print("\t2. Authenticate a digital signature")
        print("\t3. Exit")
        choice2 = input()
        
        if(choice2 == "1"):
            print("Enter a message:")
            ###
            message = input()
            #encryption of message letter by letter
            for k in range(len(message)):
                print (ord(message[k]))
                letter = (ord(message[k]))
                letter = pow(letter, e)
                letter = math.log(letter,n)
                print (letter)
                
            print("Message encrypted and sent.")
            break     
        
        elif(choice2 == "2"):
            ###
            print("There are no signature to authenticate.")
            break
        
        elif(choice2 == "3"):
            choice = "0"
            break
        
    while(choice == "2"):
        print("As the owner of the keys, what would you like to do?")
        print("\t1. Decrypt a received message ")
        print("\t2. Digitally sign a message")
        print("\t3. Exit")
        choice2 = input()
        
        if(choice2 == "1"):
            print("The following messages are available:")
            ###
            break     
        
        elif(choice2 == "2"):
            print("Enter a message:")
            ###
            print("Message signed and sent.")
            break
        
        elif(choice2 == "3"):
            choice = 0
            break
    
    if(choice == "3"):
        print("Bye for now!")
        break
