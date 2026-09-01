import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
import getpass
import json

with open("vault.dat", "rb") as f:
    data = f.read()

salt = data[0:16]
nonce = data[16:28]
ciphertext = data[28:]

password = getpass.getpass("Enter master password: ").encode()
iterations = int(input("Enter iteration count: "))
kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations)
key = kdf.derive(password)

aesgcm = AESGCM(key)


decrypted = aesgcm.decrypt(nonce, ciphertext, None)
vault_data = json.loads(decrypted)

print("Sites stored:", list(vault_data.keys()))

site = input("Which site do you want to view? ")

if site in vault_data:
    entry = vault_data[site]
    print("Username:", entry["username"])
    print("Password:", entry["password"])
else:
    print("No entry found for that site.")