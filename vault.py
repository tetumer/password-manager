import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
from cryptography.hazmat.primitives import hashes
import getpass
import json
import secrets
import string

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

while True:
    print("1. Add new entry")
    print("2. View an entry")
    print("3. List all sites")
    print("x. Exit")

    choice = input("Choose an option: ")

    if choice == "1":
        site = input("Site name: ")
        username = input("Username: ")
        gen_choice = input("Generate a random password? (y/n): ")

        if gen_choice.lower() == "y":
            chars = string.ascii_letters + string.digits + "!@#$%^&*"
            site_password = ''.join(secrets.choice(chars) for _ in range(20))
            print("Generated password:", site_password)
        else:
            site_password = getpass.getpass("Site password: ")

        if site not in vault_data:
            vault_data[site] = {}
            vault_data[site][username] = {"password": site_password}

            aesgcm = AESGCM(key)
            nonce = os.urandom(12)
            message = json.dumps(vault_data).encode()
            ciphertext = aesgcm.encrypt(nonce, message, None)

            with open("vault.dat", "wb") as f:
                f.write(salt + nonce + ciphertext)

            print("Saved.")

    elif choice == "2":
        site = input("Which site do you want to view? ")
        if site in vault_data:
            print("Usernames for this site:", list(vault_data[site].keys()))
            username = input("Which username? ")
            if username in vault_data[site]:
                print("Password:", vault_data[site][username]["password"])
            else:
                print("No entry found for that username.")
        else:
            print("No entry found for that site.")

    elif choice == "3":
        print("Sites stored:", list(vault_data.keys()))

    elif choice.lower() == "x":
        print("Goodbye.")
        break

    else:
        print("Invalid option.")