# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:15:52 2022
@authors: landon, Alvin, Aidan
"""
import math
import random

#p = 588173
#q = 961811
n = 0
e = 0
phi = 0
d = 0
sig = []
encrypSig = 0
decrypSig = 0
numSig = 0
sigList = []
publicList = []
privateList = []

#Get prime numbers 
def genPrime():
    k = 3
    prime = False
    
    while not prime:
        num = random.randint(100000, 999999)
        if isPrime(num, k):
            return num
    #for i in range(500):
     #   x = random.randint(500000,5000000)
      #  if(x % 2 != 0 and x % 3 != 0 and x % 5 != 0 and x % 7 != 0 and x % 11 != 0 and x % 13 != 0):
       #     a = x
        #    return a

#Check Primes   
def isPrime(n, k):
    
    if n == 1 or n == 4:
        return False
    elif n == 2 or n == 3:
        return True
    
    else:
        for i in range(k):
            
            a = random.randint(2, n-2)
            if mod(a, n-1, n) != 1:
                return False
            
#Mods potential primes
def mod(a, n, p):
    res = 1
    
    a = a % p
    
    while n > 0:
        if n % 2:
            res = (res * a) % p
            n = n-1
        else:
            a = (a ** 2) % p
            
            n = n // 2
    return res % p
#Function call
#p = genPrime()
#q = genPrime()
#print(p)
#print(q)

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

# Encrypt per chunk
def encrypt(e, n, msg, chars = 4, bits = 8):
    if type(msg) == str:
        msg = chunkify(msg, chars, bits)
    return [pow(c, e, n) for c in msg]

# Decrypt per chunk
def decrypt(n, d, data, chars = None, bits = None):
    result = [pow(i, d, n) for i in data]
    if chars and bits:
        result = dechunkify(result, chars, bits)
    return result

# Test code for consolidating 4 characters at a time into an integer
# sum([ord("test"[i]) << 8 * i for i in range(4)])

# Chunkify
# **NOT** ENCRYPTION!!!
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
# **NOT** DECRYPTION!!!
# Chunkify in reverse. Chars and bits must be the same.
def dechunkify(chunks, chars = 4, bits = 8):
    result = ""
    mask = 2**bits-1
    for chunk in chunks:
        for i in range(chars):
            result += chr((chunk >> bits * i) & mask)
    return result.strip("\x00")
        

#Signature Encryption
def sigEncrypt(c, d, n):
    s = pow(int(c),d,n)
    return s


#Signature Decryption
def sigDecrypt(s, e, n):
    i = pow(s,e,n)
    return i


while(True):
    #wtf is N
    p = genPrime()
    q = genPrime()
    print (p)
    print (q)
    e,n,phi = pubKeyGen(p,q)
    d = privKeyGen(e, phi)
    #print("N is:", n)
    #print("E is:", e)
    print("\n")
    print ("RSA keys have been generated.")
    
    print("Please select your user type:")
    print("\t1. A public user")
    print("\t2. The owner of the keys")
    print("\t3. Exit program ")
    
    choice = input()
    
    while choice == "1":
        print("As a public user, what would you like to do?")
        print("\t1. Send an encrypted message")
        print("\t2. Authenticate a digital signature")
        print("\t3. Exit")
        choice2 = input()
        
        if choice2 == "1":
            message = input("Enter a message > ")
            publicList.append(message)
            #encryption of message letter by letter
            msg_chunks = chunkify(message)
            msg_c = encrypt(e, n, msg_chunks)
            print("Message encrypted and sent")
            privateList.append(msg_c)
            print(msg_c)
            break
        
        elif choice2 == "2":
            print("Signature Authentication has been selected.")
            if len(sig) == 0:
                print("There are no signature to authenticate")
                break
            else:
                print("The following messages are available: ")
                count = 0
                for x in sig:
                    print(count, ". ", x)
                    count+=1
                sigChoice = int(input("Enter your choice: ")) #what is this used for? - i wanted to do a way to choose what message to decrypt but never finished
                decrypSig = sigDecrypt(encrypSig, e, n)
                print("Decrypted: ", decrypSig, " Encrypted", numSig)
            
                if (numSig == decrypSig):
                    print("Signature verified.")
                else:
                    print("Signature is not Valid")
           
            break
        
        elif choice2 == "3":
            choice = "0"
            break
        
    while choice == "2":
        print("As the owner of the keys, what would you like to do?")
        print("\t1. Decrypt a received message ")
        print("\t2. Digitally sign a message")
        print("\t3. Exit")
        choice2 = input()
        
        if choice2 == "1":
            if msg_c is None:
                print("There are no messages available")
            else:
                print("The following messages are available:")
                for x in range(len(privateList)):
                    print("- Message #{0}".format(x)) # is this intentional? - aidan
                    #print(x + 1, "Message #", x + 1, ": ") should we use this one? - Alvin
                messageChoice = int(input("Enter your choice: "))
                
                if messageChoice < len(privateList):
                    decrypMessage = dechunkify(decrypt(n, d, privateList[messageChoice]))
                    print("Decrypted message: ", decrypMessage)
                
            break     
        
        elif choice2 == "2":
            print("Enter a message:")
            signature = input
            sigList.append(signature)
            for x in signature:
                # this was a string cast - was this ever intentional?
                numSig += ord(x) - 96
            encrypSig = sigEncrypt(numSig, d, n)
            print("Message signed and sent.")
            break
        
        elif choice2 == "3":
            choice = 0
            break
    
    if choice == "3":
        print("Bye for now!")
        break
