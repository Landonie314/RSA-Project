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

# Encrypt per character
def encrypt(e, n, msg):
   return [pow(c, e, n) for c in chunkify(msg)]

# Test code for consolidating 4 characters at a time into an integer
# sum([ord("test"[i]) << 8 * i for i in range(4)])

# Chunkify
# Consolidates messages into integer chunks of (chars) characters each,
# at (bits) bits per character. Default is 32-bit integers representing
# 4 characters at a time.
# Meant to prevent the encrypted message becoming a glorified
# substitution cipher.
def chunkify(msg, chars = 4, bits = 8):
    chunks = []
    for i in range(math.ceil(len(msg) / chars)):
        chunk = msg[chars*i : chars*(i+1)] # can take out of bounds indices, for some reason. ok!
        chunk += '\x00' * (chars - len(chunk)) # add null characters if too short
        chunkbytes = []
        for j in range(chars):
            codepoint = ord(chunk[j])
            if codepoint > 2**bits-1: # too big for given bit count?
                raise OverflowError(f"Character '{chunk[j]}': Value too large to be represented")
            chunkbytes.append(codepoint << bits * j) # shift n*j bits to the left
        chunks.append(sum(chunkbytes))
    return chunks

# Dechunkify
# Chunkify in reverse. Chars and bits must be the same.
def dechunkify(chunks, chars = 4, bits = 8):
    result = ""
    mask = 2**bits-1
    for chunk in chunks:
        for i in range(chars):
            result += chr((chunk >> bits * i) & mask)
    return result.strip("\x00")
        

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
            message = input("Enter a message > ")
            #encryption of message letter by letter
            msg_c = encrypt(e, n, message)
            print(msg_c)
                
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
