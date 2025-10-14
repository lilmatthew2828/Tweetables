import os
from cryptography.fernet import Fernet


def generate_key():
   key = Fernet.generate_key()
   with open("secret.key", "wb") as key_file:
       key_file.write(key)
   print("Key generated and saved as 'secret.key'.")


def load_key():
   with open("secret.key", "rb") as key_file:
       return key_file.read()


def encrypt_file():
   key = load_key()
   fernet = Fernet(key)


   file_name = input("Enter the name of the .txt file to encrypt (e.g., user.txt): ")
   try:
       with open(file_name, "rb") as file:
           original = file.read()


       encrypted = fernet.encrypt(original)


       output_file = file_name.replace(".txt", "_encrypted.txt")
       with open(output_file, "wb") as encrypted_file:
           encrypted_file.write(encrypted)


       print(f"Encryption complete! Encrypted file saved as '{output_file}'")


   except FileNotFoundError:
       print(f"File '{file_name}' not found!")
   except Exception as e:
       print(f"An error occurred: {e}")


def decrypt_file():
   key = load_key()
   fernet = Fernet(key)


   file_name = input("Enter the name of the encrypted file (e.g., user_encrypted.txt): ")
   try:
       with open(file_name, "rb") as enc_file:
           encrypted_data = enc_file.read()


       decrypted_data = fernet.decrypt(encrypted_data)


       output_file = file_name.replace("_encrypted.txt", "_decrypted.txt")
       with open(output_file, "wb") as dec_file:
           dec_file.write(decrypted_data)


       print(f"Decryption complete! Decrypted file saved as '{output_file}'")


   except FileNotFoundError:
       print(f"File '{file_name}' not found!")
   except Exception as e:
       print(f"An error occurred: {e}")


# === Main Menu ===
print("Welcome to the Crypto Tool!")
if not os.path.exists("secret.key"):
   generate_key()


choice = input("Do you want to (E)ncrypt or (D)ecrypt a file? ").lower()


if choice == 'e':
   encrypt_file()
elif choice == 'd':
   decrypt_file()
else:
   print("Invalid choice. Please select 'E' to encrypt or 'D' to decrypt.")



