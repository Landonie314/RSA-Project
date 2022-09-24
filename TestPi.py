# -*- coding: utf-8 -*-
"""
Created on Wed Sep 14 11:15:52 2022
@authors: landon, Alvin, Aidan
"""
import math
import random

CANDIDATE_TESTS = (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37)
# added a couple primes past 13 for better actual prime chance
# may impact performance with the addition of more numbers. can this be fixed?


# Prime number generator
# Extra options included for performance & security tuneup
def genPrimes(floor=500000,ceil=5000000,cand_num=500,fermat_num=50):
    sufficient = False
    while not sufficient:
        cand = []
        for i in range(cand_num):
            x = random.randint(floor,ceil)
            if not False in [x % t != 0 for t in CANDIDATE_TESTS]:
                # If these conditions are passed the number may be prime
                cand.append(x)
        # Candidates generated, filter them down using Fermat's test
        cand_f = [i for i in cand if fermat(i, fermat_num)]
        # If at least 2 pseudoprimes have been generated, the list is sufficient.
        # If not, do it over again.
        sufficient = True if len(cand_f) >= 2 else False
    # Return two non-repeating pseudoprimes from the list at random.
    p = cand_f.pop(random.randint(0,len(cand_f)-1))
    q = cand_f.pop(random.randint(0,len(cand_f)-1))
    return p, q
        

# Fermat's Test
# Pseudoprime candidate verification.
def fermat(n, tests=50):
    a = 0
    for foo in range(tests):
        # Select a in the lower half of n such that a and n are
        # relatively prime. This should work immediately if n is
        # truly prime, but it doesnt't hurt to make sure.
        while math.gcd(a, n) != 1:
            a = random.randint(2, n//2)
        # Apply Fermat's Little Theorem.
        # If any number a between 0 and n does not satisfy
        # a^(n-1) % n = 1, then the number is definitely not prime.
        if pow(a, n-1, n) != 1:
            return False
    return True


# (Extended) Euclid's Algorithm
# Keypair generation (publickey, privatekey)
# Publickey: (e, n)   Privatekey: (d, n)
def genKeypair(p, q):
    n = p*q
    e = 0
    phi = (p-1)*(q-1)

    # should not take long; e is usually a single-digit number
    for x in range(phi):
        if(math.gcd(x,phi) == 1 and x > 1):
            e = x
            break
    
    # generate d using extended euclid gcd
    d = extended_gcd(e, phi)[0] % phi
    # pubkey, privkey
    return ((e, n), (d, n))


# Extended GCD Utility
def extended_gcd(a=1, b=1):
    if b == 0:
        return (1, 0, a)
    (x, y, d) = extended_gcd(b, a%b)
    return y, x - a//b*y, d


# Encrypt per chunk
def encrypt(publickey, msg, chars = 4, bits = 8):
    if type(msg) == str:
        msg = chunkify(msg, chars, bits)
    return [pow(c, publickey[0], publickey[1]) for c in msg]


# Decrypt per chunk
def decrypt(privatekey, data, chars = None, bits = None):
    result = [pow(i, privatekey[0], privatekey[1]) for i in data]
    if chars and bits:
        result = dechunkify(result, chars, bits)
    return result


# Test code for consolidating 4 characters at a time into an integer
# sum([ord("test"[i]) << 8 * i for i in range(4)])


# Chunkify
# **NOT** ENCRYPTION!!!
# Turns sets of (chars) characters at a time into single integers
# with the same binary representation in memory.
# Default is 32-bit integers. (8 bits per character, 4 characters per chunk)
# Meant to deter the use of frequency analysis on per-character encryption.
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
def sigEncrypt(c, privKey):
    s = pow(int(c),privKey[0],privKey[1])
    return s


#Signature Decryption
def sigDecrypt(s, pubKey):
    i = pow(s,pubKey[0],pubKey[1])
    return i



if __name__ == "__main__":

    sigList = []
    publicList = []
    privateList = []
    #wtf is N
    (p, q) = genPrimes()
    print (p, q)
    pubKey, privKey = genKeypair(p, q)
    print ("RSA keys have been generated.")

    while 1:
        
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
                msg_c = encrypt(pubKey, msg_chunks)
                print("Message encrypted and sent")
                privateList.append(msg_c)
                print(msg_c)
                break
            
            elif choice2 == "2":
                print("Signature Authentication has been selected.")
                if len(sigList) == 0:
                    print("There are no signatures to authenticate")
                    break
                else:
                    print("The following messages are available: ")
                    count = 0
                    for x in sigList:
                        print(count, ". ", x)
                        count+=1
                    sigChoice = int(input("Enter your choice: "))
                    sig = sigList[sigChoice]
                    decrypSig = sigDecrypt(sig[0], pubKey)
                    print("Decrypted:", decrypSig, "Original:", sig[1])
                
                    if (sig[1] == decrypSig):
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
                        decrypMessage = dechunkify(decrypt(privKey, privateList[messageChoice]))
                        print("Decrypted message:", decrypMessage)
                    
                break     
            
            elif choice2 == "2":
                signature = input("Enter a message:")
                numSig = 0
                for x in signature:
                    # this was a string cast - was this ever intentional?
                    numSig += ord(x)
                sigList.append((sigEncrypt(numSig, privKey), numSig))
                print("Message signed and sent.")
                break
            
            elif choice2 == "3":
                choice = 0
                break
        
        if choice == "3":
            print("Bye for now!")
            break
