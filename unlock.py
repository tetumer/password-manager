import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
import getpass

with open("vault.dat", "rb") as f:
    data = f.read()

salt = data[0:16]
nonce = data[16:28]
ciphertext = data[28:]

print(salt)
print(nonce)
print(ciphertext)
password = getpass.getpass("Enter master password: ").encode()

kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=480000)
key = kdf.derive(password)

aesgcm = AESGCM(key)
decrypted = aesgcm.decrypt(nonce, ciphertext, None)

print(decrypted)