import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
import getpass
import json

if os.path.exists("vault.dat"):
    with open("vault.dat", "rb") as f:
        data = f.read()
    salt = data[0:16]
    old_nonce = data[16:28]
    old_ciphertext = data[28:]

    master_password = getpass.getpass("Enter master password: ").encode()
    iterations = int(input("Enter iteration count: "))
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations)
    key = kdf.derive(master_password)

    aesgcm = AESGCM(key)
    decrypted = aesgcm.decrypt(old_nonce, old_ciphertext, None)
    vault_data = json.loads(decrypted)
else:
    salt = os.urandom(16)
    master_password = getpass.getpass("Set a new master password: ").encode()
    iterations = int(input("Enter iteration count: "))
    kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=iterations)
    key = kdf.derive(master_password)
    vault_data = {}

site = input("Site name: ")
username = input("Username: ")
site_password = getpass.getpass("Site password: ")

vault_data[site] = {"username": username, "password": site_password}

aesgcm = AESGCM(key)
nonce = os.urandom(12)
message = json.dumps(vault_data).encode()
ciphertext = aesgcm.encrypt(nonce, message, None)

with open("vault.dat", "wb") as f:
    f.write(salt + nonce + ciphertext)

print("Saved.")