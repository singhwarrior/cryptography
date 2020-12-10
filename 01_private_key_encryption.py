# pip install cryptography

import cryptography
from cryptography.fernet import Fernet

'''
Private Key Encryption is the encryption mechanism where a
shared key is used for encrypting data. That is why it is 
also called Symmetric Key Encryption also.

There are two methods:
- Stream ciphers: Bit by bit encryption. Which is not used.
- Block ciphers: Block(group of bits) by block encryption.

Some of the Block ciphers: DES, Triple DES, IDEA, RC5, AES.

Following example uses AES(Advanced Encryption Standard).

Demerit: Since the key is shared between sender and reciever,
hence the message can be easily hacked.
'''

key = Fernet.generate_key()     # key is used to encrypt the content

with open('symmetric.key','wb') as file: # Storing private key to a file
 file.write(key)

del key

with open('symmetric.key','rb') as file: # Reading private key from a file
 key = file.read()

print(key.decode())


message = 'Hello encryption!!'

f = Fernet(key)
encrypted = f.encrypt(message.encode())   # Encrypting text message
print(encrypted)

decrypted = f.decrypt(encrypted)          # Decrypting text message
print(decrypted)

print(message==decrypted.decode())
 	
