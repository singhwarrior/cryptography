'''
Using Public Key encryption/Asymmetric Key Encryption makes sure that
encrypted data cannot be viewed by someone else. But it does not autheticate
the data person who sent the data is the same person or not.

Example:
-------
Walle wants to send message to Eva. He encrypts message by using public key
of Eva. But someone can hack the data and send his encrypted data, because 
public key is known for public.

To avoid this, Walle will use his private key to create digital signature. 
It will also enclude the ecrypted data of Eva. 

Once signature reaches Eva, Eva uses public key of Walle to verify the 
signature. If InvalidSignature Exception not thrown that means the signed 
data is sent by Walle and no one else. Hence now Eva can also read the message.

So digital signature serves following three purpose:
- Authentication(Identity)
- Non-Repudiation(Sender cannot deny having send the message later on)
- Integrity, i.e. Message was not altered while transit

Demerit:
-------
Lack of Authentication, Digital Signature itself does not verify its true
identity of Sender and his Public Key. 

Example: Walle sends a message to Eva Ecrypted with Public Key of Eva. He
also sends a digital signature which Eva can decrypt using Walle's Public Key.
But if a hacker has intercepted Walle's message and sends his signature and
public key, Eva will be able to verify the sugnature without knowing that
message is from wrong sender. 

Solution for this is Digital Certificate.
'''

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

# Private Key of Walle which is local to Walle and no one knows it
walle_private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend())

# Public Key of Walle who keeps it on public server/location
walle_public_key = walle_private_key.public_key()

from cryptography.hazmat.primitives import serialization

pem = walle_private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption())

with open('walle_private_key.pem', 'wb') as f:
 f.write(pem)

pem = walle_public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

with open('walle_public_key.pem', 'wb') as f:
 f.write(pem)

del pem
del walle_public_key
del walle_private_key

# Getting Public Key of Eva, who is receiver of Walle message
with open("eva_public_key.pem", "rb") as key_file:
        eva_public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )

# Getting Private key of Walle
with open("walle_private_key.pem", "rb") as key_file:
        walle_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

# Walle is using public key of Eva to encrypt the message
message = b'Hello Eva!'
encrypted = eva_public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

# Walle creating digital signature using his Private Key.
signature = walle_private_key.sign(
 		encrypted,
		padding.PSS(
			mgf=padding.MGF1(hashes.SHA256()),
			salt_length=padding.PSS.MAX_LENGTH),
		hashes.SHA256()
		)


print(f'Walle sends message "{message.decode()}" to Eva encrypted as follows')
print('====================ENCRYPTED MESSAGE STARTs=======================')
print(encrypted) 
print('====================ENCRYPTED MESSAGE ENDs=======================')

# Eva gets encrypted message and started decrypting it using her private_key.


# Eva reads public key of Walle to verify the digital signature
with open("walle_public_key.pem", "rb") as key_file:
        walle_public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )


is_signature_correct = False
try:
 walle_public_key.verify(
                	signature=signature,
                	data=encrypted,
                	padding=padding.PSS(
                    		mgf=padding.MGF1(hashes.SHA256()),
                    		salt_length=padding.PSS.MAX_LENGTH
                		),
                	algorithm=hashes.SHA256()
            		)
 is_signature_correct = True
except InvalidSignature:
 print('Signature not verified and hence the person sent the message is not Walle')
	
# After signature is verified, encrypted message is read by Eva
if is_signature_correct:
 
 with open("eva_private_key.pem", "rb") as key_file:
        eva_private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

 original_message = eva_private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

 print(f'Eva reads message "{original_message.decode()}"') 


