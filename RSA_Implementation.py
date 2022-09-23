# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 14:56:50 2022

@author: Aidan Robertson
         Jake Davis
"""

#import statements
import math
import random

#------------------------------FUNCTION DECLARATIONS------------------------------------------------------------

#Generates list of pseudo prime candidates
def candidateList(n = 1000000):
    l = []
    for i in range(200):
        c = random.randint(n, 10 * n)
        if c %2 != 0 and c %3 != 0 and c %7 != 0 and c %11 != 0:
            l.append(c)
    return l

#Checks to see which numbers in the candidate list are pseudo prime
def isPrime(candList = [2]):
    primeList = []
    while len(primeList) < 2:
        for i in candList:
            pseudo = True
            #Fermat's test * 40
            for j in range (40):
                p = random.randint(2, i//2)
                if pow(p, i - 1, i) != 1 or math.gcd(p, i) != 1:
                    pseudo = False
                    break
            if pseudo:
                primeList.append(i)
        if len(primeList) < 5:
            candList = candidateList()
    return primeList

#Selects our p and q from the psuedo prime list above
def selectPQ(pList = []):
    if len(pList) < 2:
        print('Two or more prime numbers required.')
        return
    else:
        p = pList.pop()
        q = pList.pop()
        #Prevent duplicates
        while p == q:
            q = pList.pop()
        return p, q

#Called in generatePrivateKey to determine d
def extendedGcd(a, b):
    if b == 0:
        return (1, 0, a)
    (x, y, d) = extendedGcd(b, a%b)

    return y, x - a//b*y, d

#GCD function is used because it can help to determine if two
#numbers are RELATIVE PRIME (if the function returns 1)
def generatePublicKey(phi):
    #generate random number to be tested
    potentialKey = random.randint(0,phi)

    print(potentialKey)
        #if potentialKey (generated integer) is relative prime to phi
    if math.gcd(phi, potentialKey) == 1:
        #print("Found Key...")

            #return public key
        return potentialKey
        #if potentialKey (generated integer) is not relative prime
        #recursively call generateKeys
    else:
        #print("Not Found...")
        return generatePublicKey(phi)


def generatePrivateKey(e, phi):
    x, y, d = extendedGcd(e, phi)
        #x variable returned is to be used as private key, along with n
    return x,y,d

#encrypts message when called and passed the message (plaintext form), e, n
def encryptMessage(message, e, n):
    sumc = []
    #loop through characters in message
    for c in message:
            #convert message[i] into unicode (ascii basically)
        temp = ord(c)
            #temp^e % n to encrypt message using public key
        temp = pow(temp, e) % n
            #appends encrypted character to sumc list, which will be returned after for loop
        sumc.append(temp)
    return sumc

#decrypts message when called and passed the message (encrypted form), n, and the private key (d)
def decryptMessage(message, d, n):
    decrypt = []
    # loops through 'characters' in the message (they are actually numbers bc unicode)
    for c in message:
        temp = c
            #mod to make sure d remains non-negative, avoids decryption error
        if d < 0:
            d = d%phi
            #runs decryption algorithm using the private keys generated earlier
        temp = pow(temp, d) % n
            #appends decrypted unicode character to decrypt list, which will be returned after for loop
        decrypt.append(temp)
    #returns a list containing the decrypted unicode characters
    return decrypt


# -----------------------------------RUN TIME CODE (MAIN)---------------------------------------------------
#P
#seedP = 151 # this will eventually need to be automatically generated at runtime
#Q
#seedQ = 167 # this will eventually need to be automatically generated at runtime

#generate two psuedo prime numbers p and q
seedP, seedQ = selectPQ(isPrime(candidateList()))

#--------------DEBUG--------------
    #prints phi
print("p = " + str(seedP))
print("q = " + str(seedQ))
#---------------------------------

#generate phi (p-1)*(q-1)
phi = (seedP-1) * (seedQ-1)

#--------------DEBUG--------------
    #prints phi
print("phi = " + str(phi))
#---------------------------------
#generates n, to be used with public key (n, e) aswell as private key (n, d)
n = seedP * seedQ

#--------------DEBUG--------------
    #prints n
print("N = " + str(n))
#---------------------------------

#generate public key (e), passed phi
e = generatePublicKey(phi)

#returns private key at first index(d), passed e and fi
returnValues = generatePrivateKey(e, phi)

#used in conjunction with above code to verify that d is in fact returnValues[0]
for x in returnValues:
     if (e*x%phi == 1):
         d = x
         print(d)

#--------------DEBUG--------------
    #prints return for value
#print(returnValues)
    # prints public key (n, e) and private key (n, d)
print("Public Key = " + str(n)+ ","+ str(e))
print("Private Key = " + str(n)+ ","+ str(d))
#---------------------------------

message = input("Please Enter Message To Be Encrypted: ")
message2 = []

#returns encryptedMessage (characters in unicode, with encryption algorithm)
encryptedMessage = encryptMessage(message, e, n)

#--------------DEBUG--------------
for c in message:
    message2.append(ord(c))
print("Initial Message = ", message)
print("ASCII Message = ", message2)
print("Encrypted Message = ", encryptedMessage)
#----------------------------------

#decrypts message when passed encryptedMessage, priavte key (d), n
decryptedMessage = decryptMessage(encryptedMessage, d, n)

print("Decrypted Message = ", decryptedMessage)

#converts decrypted unicode to characters and appends them to returnedMessage list
returnedMessage = []
for c in decryptedMessage:
    value = chr(c)
    returnedMessage.append(value)

print("Returned Message = ", returnedMessage)
