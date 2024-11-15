import argparse
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
import os
import base64

def generate_key(password):
    salt = os.urandom(16)
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=salt,
        iterations=480000,
    )
    key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
    with open("secret.key", "wb") as file:
        file.write(salt + key)
    print("Nyckeln 'secret.key' har skapats.")

def load_key(password):
    try:
        with open("secret.key", "rb") as file:
            salt = file.read(16)
            stored_key = file.read()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password.encode()))
        if key != stored_key:
            raise ValueError("Fel lösenord.")
        return key
    except FileNotFoundError:
        print("Nyckeln 'secret.key' saknas.")
        exit(1)
    except Exception as e:
        print(f"Error: {e}")
        exit(1)

def create_file(file_path):
    if not os.path.exists(file_path):
        with open(file_path, "w") as file:
            file.write("Min hemliga fil.")
        print(f"Filen '{file_path}' har skapats.")
    else:
        print(f"Filen '{file_path}' finns redan.")

def encrypt_file(file_path, password):
    create_file(file_path)
    key = load_key(password)
    cipher_suite = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            file_data = file.read()
        encrypted_data = cipher_suite.encrypt(file_data)
        encrypted_file_path = file_path + ".enc"
        with open(encrypted_file_path, "wb") as file:
            file.write(encrypted_data)
        print(f"Filen har krypterats och sparats som '{encrypted_file_path}'.")
    except Exception as e:
        print(f"Error: {e}")

def decrypt_file(file_path, password):
    key = load_key(password)
    cipher_suite = Fernet(key)
    try:
        with open(file_path, "rb") as file:
            encrypted_data = file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        with open(file_path, "wb") as file:
            file.write(decrypted_data)
        print(f"Filen '{file_path}' har dekrypterats.")
    except FileNotFoundError:
        print(f"Filen '{file_path}' hittades inte.")
    except Exception as e:
        print(f"Error: {e}")

def main():
    parser = argparse.ArgumentParser(description="Projekt Frans Schartau - Filkrypteringsverktyg.")
    parser.add_argument("command", choices=["generate-key", "encrypt", "decrypt"], help="Välj ett kommando")
    parser.add_argument("--file", help="Sökvägen till filen som ska krypteras eller dekrypteras")
    parser.add_argument("--password", required=True, help="Lösenord för att skapa eller läsa nyckeln")

    args = parser.parse_args()

    if args.command == "generate-key":
        generate_key(args.password)
    elif args.command == "encrypt":
        if not args.file:
            print("Ange filen som ska krypteras.")
        else:
            encrypt_file(args.file, args.password)
    elif args.command == "decrypt":
        if not args.file:
            print("Ange filen som ska dekrypteras.")
        else:
            decrypt_file(args.file, args.password)

if __name__ == "__main__":
    main()