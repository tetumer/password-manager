import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes

salt = os.urandom(16)
password = b"teasty password"
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(), 
    length=32, 
    salt=salt,  
    iterations=480000
    )
key = kdf.derive(password)

print(key)
aesgcm = AESGCM(key)
nonce = os.urandom(12)
message = b"Chat gpt is thousand times better than claude"
ciphertext = aesgcm.encrypt(nonce, message, None)

print(ciphertext)
decrypted = aesgcm.decrypt(nonce, ciphertext, None)

print(decrypted)