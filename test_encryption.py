from modules.encryption import encrypt_file, decrypt_file


password = "MySecurePassword123!"


input_file = "test.jpg"
encrypted_file = "encrypted/test.jpg.enc"
decrypted_file = "decrypted/test_restored.jpg"


print("Starting encryption...")

encrypt_file(
    input_file,
    encrypted_file,
    password
)

print("Encryption successful!")
print("Encrypted file:", encrypted_file)


print("\nStarting decryption...")

decrypt_file(
    encrypted_file,
    decrypted_file,
    password
)

print("Decryption successful!")
print("Decrypted file:", decrypted_file)