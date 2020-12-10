'''
Public Key encryption which is also called Asymmetric Key Encryption
as well, can solve the problem of Private Key Encryption.

It is called Asymmetric Key Encryption because it needs two paired keys
i.e. public key and private key both for encryption and decryption.

Lets say we have two persons who want to communicate between each other
privately, so that no one can see their conversations. Lets assume their
names are Walle and Eva. 

Walle is sender and Eva is reciever of the message. In Public Key 
Encryption always communication starts from receiver:

- Eva creates a pair of keys, private key and public key.
- Eva keeps private key locally but public key is shared to public key
  server, from where anypone can access her public key.
- Walle access Eva's public key and encrypts his message and send to Eva
- Eva gets the encrypted message and using private key, she decrypts the 
  message

Demerit: Since public key is accessible to everyone, hence anyone can access
and can send encrypted message to Eva pretending that he is Walle. Hence to
identify the sender we need digital signature.

'''

# RSA (Rivest–Shamir–Adleman) is one of the first public-key cryptosystems 
# and is widely used for secure data transmission
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa

private_key = rsa.generate_private_key(
		public_exponent=65537,
		key_size=2048,
		backend=default_backend())

public_key = private_key.public_key()

from cryptography.hazmat.primitives import serialization
pem = private_key.private_bytes(
		encoding=serialization.Encoding.PEM,
		format=serialization.PrivateFormat.PKCS8,
		encryption_algorithm=serialization.NoEncryption())

with open('eva_private_key.pem', 'wb') as f:
 f.write(pem)

pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

with open('eva_public_key.pem', 'wb') as f:
 f.write(pem)

del pem
del public_key
del private_key

# Walle started for sending message. For that he gets the public key of
# Eva and then encrypt the message.
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

with open("eva_public_key.pem", "rb") as key_file:
        public_key = serialization.load_pem_public_key(
            key_file.read(),
            backend=default_backend()
        )


message = b'Hello Eva!'
encrypted = public_key.encrypt(
        message,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

print(f'Walle sends message "{message.decode()}" to Eva encrypted as follows')
print('====================ENCRYPTED MESSAGE STARTs=======================')
print(encrypted) 
print('====================ENCRYPTED MESSAGE ENDs=======================')

# Eva gets encrypted message and started decrypting it using her private_key.
with open("eva_private_key.pem", "rb") as key_file:
        private_key = serialization.load_pem_private_key(
            key_file.read(),
            password=None,
            backend=default_backend()
        )

original_message = private_key.decrypt(
        encrypted,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

print(f'Eva reads message "{original_message.decode()}"') 


