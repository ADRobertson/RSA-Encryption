# -*- coding: utf-8 -*-
"""
Created on Tue Sep 20 14:56:50 2022
@author: Aidan Robertson
         Jake Davis
         Sam Games
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

    #print(potentialKey)
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
                #pow with third argument = (temp^d) % n
        temp = pow(temp, e, n)
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
                #pow with third argument = (temp^d) % n
        temp = pow(temp, d, n)
            #appends decrypted unicode character to decrypt list, which will be returned after for loop
        decrypt.append(temp)
    #returns a list containing the decrypted unicode characters
    return decrypt

def generateSignature(message, d, n):
    list = []
    for s in message:
        #print(s)
            #converts the message into ascii
        temp = ord(s)

            # generates signature with private key
        s = pow(temp, d, n)
        #print("S is " + str(s))

        #adds and stores characters in list
        list.append(s)

    return list

def verifySignature(signature, e, n):
    returnList = []
    #verify message with public key

    for s in signature:
        v = pow(s, e, n)
        returnList.append(v)

    #Checks to see if the message is a valid signature
    return returnList
# -----------------------------------RUN TIME CODE (MAIN)---------------------------------------------------
#generate two psuedo prime numbers p and q
seedP, seedQ = selectPQ(isPrime(candidateList()))

#generate phi (p-1)*(q-1)
phi = (seedP-1) * (seedQ-1)

#generates n, to be used with public key (n, e) aswell as private key (n, d)
n = seedP * seedQ

#Key Generation needs to take place BEFORE UI opens
#generate public key (e), passed phi
e = generatePublicKey(phi)

#returns private key at first index(d), passed e and fi
returnValues = generatePrivateKey(e, phi)

#used in conjunction with above code to verify that d is in fact returnValues[0]
for x in returnValues:
     if (e*x%phi == 1):
         d = x

encryptedMessages = []
decryptedMessages = []

signatureMessages = []
signatures = []

userType = 0


print("RSA Keys Have Been Generated...")

#determine initial user type (owner of keys or public user)
print("Please select your user type:")
print("\t1. A Public User")
print("\t2. The Owner Of The Keys")
print("\t3. Exit Program")
userType = input("Enter Your Choice: ")

while userType != '3':
    #if user is a public user
    if userType == '1':
        print("\nAs a Public User what would you like to do?")
        print("\t1. Send an Encrypted Message")
        print("\t2. Authenticate a digital signature")
        print("\t3. Exit")
        publicUserChoice = input("Enter Your Choice: ")

        #if user wants to send an encrypted message
        if publicUserChoice == '1':
                #let user input desired message to encrypt
            message = input("Enter a Message: ")
                #send message, public key, and n to encryptMessage function
            encryptedMessage = encryptMessage(message, e, n)
                #append encrypted message to encryptedMessages list (used later for I/O listing messages available to owner to decrypt)
            encryptedMessages.append(encryptedMessage)

        #if user wants to authenticate a digital signature
        elif publicUserChoice == '2':
            #if there are no signatures available to authenticate
            if len(signatures) == 0:
                print("There are no signatures available to authenticate...")
            #otherwise/ if there are signatures available to authenticate
            else:
                print("The Following Messages Are Available: ")
                #for loop to print out messages available to be authenticated
                for x, message in enumerate(signatures):
                    print(str(x+1) + ".", signatureMessages[x])

                #input to let user select which signature to authenticate
                validateSignatureChoice = input("Enter Your Choice: ")
                #subtract 1 from input becuase we add one earlier (so that the first item in list is available as '1' not '0')
                validateSignatureChoice = int(validateSignatureChoice) - 1

                #pass encrypted signature, public key to verifySignature, returns unecrypted unicode
                reducedSignature = verifySignature(signatures[validateSignatureChoice],e,n)

                #this for loop converts unicode decrypted signature to plain text
                plainTextSignatureList = []
                for s in reducedSignature:
                    temp = chr(s)
                    plainTextSignatureList.append(temp)

                #now that decrypted signature is in characters, use join function to make a string out of them
                plainTextSignature = ''.join(plainTextSignatureList)

                #if plainTextSignature is the same as the initial input by owner of the keys, (meaning it is validiated!)
                if (plainTextSignature == signatureMessages[validateSignatureChoice]):
                    print("Signature is Valid!")
                else:
                    print("Signature is Not Valid!")
        #if user wants to exit public user menu
        elif publicUserChoice == '3':
            #allow user to select whether they are owner of keys or public user again
            print("\nPlease select your user type:")
            print("\t1. A Public User")
            print("\t2. The Owner Of The Keys")
            print("\t3. Exit Program")
            userType = input("Enter Your Choice: ")

    #if user is owner of keys
    elif userType == '2':
        #allows user to determine what they'd like to do as owner of the keys
        print("\nAs the Owner of the Keys, what would you like to do?")
        print("\t1. Decrypt a received message")
        print("\t2. Digitally Sign a message")
        print("\t3. Exit")
        privateUserChoice = input("Enter Your Choice: ")

        #if user wants to decrypt a received message
        if privateUserChoice == '1':
            #if there are no encrypted messages available to decrypt
            if len(encryptedMessages) == 0:
                print("There are no messages available")
            #others/ there are encrypted messages available to decrypt
            else:
                #list messages available to decrypt (the lenght of the messages)
                for x, message in enumerate(encryptedMessages):
                    print(str(x + 1) + ". (length =" + str(len(message)) + ")")

                #allow user to make choice for which message is to be decrypted
                decryptMessageChoice = input("Enter your choice: ")
                #converts user input to integer (for slicing) and subtracts 1 (we added one earlier to make the first item appear as 1 instead of 0)
                decryptMessageChoice = int(decryptMessageChoice) - 1

                #passes encryptedMessage[choice of user] and private key to decryptMessage
                decryptedMessage = decryptMessage(encryptedMessages[decryptMessageChoice],d,n)

                #loops through decrypted message (in unicode list) and: converts it to plain text, appends it to list of characters in finalMessage List
                finalMessageList = []
                for x in decryptedMessage:
                    temp = chr(x)
                    finalMessageList.append(temp)

                #now that decrypted message is in plain text, join the list to form a string
                finalMessage = ''.join(finalMessageList)

                #print the formed string from finalMessageList
                print("Decrypted Message: ", finalMessage)

        #if user wants o digitally sign a message
        elif privateUserChoice == '2':
            #ask user to input their signature message
            signatureMessage = input("Enter a message: ")
            #adds plain text message to signatureMessages (for display at public user menu)
            signatureMessages.append(signatureMessage)
            #adds a list of encrypted characters to signatures list, this will eventually be used to pass to verifySignature when public user authenticates it
            signatures.append(generateSignature(signatureMessage, d, n))
            #confirms that the message was properly processed.
            print('Message signed and sent.')

        #if user wants to exit owner of keys menu
        elif privateUserChoice == '3':
            #allow user to select whether they are owner of the keys or public user again
            print("\nPlease select your user type:")
            print("\t1. A Public User")
            print("\t2. The Owner Of The Keys")
            print("\t3. Exit Program")
            userType = input("Enter Your Choice: ")

    #if user wants to exit the program entirely
    elif userType == '3':
        break

print("***The Program Run has Ended***")
