from modules.encryption import encrypt_file, decrypt_file
import os


# ==============================
# CONFIGURATION
# ==============================

PASSWORD = "MySecurePassword123!"

ORIGINAL_FILE = "test.jpg"

ENCRYPTED_FILE = "encrypted/tamper_test.jpg.enc"

DECRYPTED_FILE = "decrypted/tamper_test_restored.jpg"


print("=" * 60)
print("AES-256-GCM TAMPER DETECTION TEST")
print("=" * 60)


# ==============================
# STEP 1 — ENCRYPT
# ==============================

print("\n[1] Encrypting original file...")

encrypt_file(
    ORIGINAL_FILE,
    ENCRYPTED_FILE,
    PASSWORD
)

print("✓ Encryption successful")


# ==============================
# STEP 2 — MODIFY ENCRYPTED FILE
# ==============================

print("\n[2] Modifying encrypted file...")

with open(ENCRYPTED_FILE, "r+b") as file:

    file.seek(-1, os.SEEK_END)

    original_byte = file.read(1)

    file.seek(-1, os.SEEK_END)

    modified_byte = bytes([
        original_byte[0] ^ 0xFF
    ])

    file.write(modified_byte)


print("✓ Encrypted file modified")


# ==============================
# STEP 3 — TRY DECRYPTION
# ==============================

print("\n[3] Attempting to decrypt modified file...")

try:

    decrypt_file(
        ENCRYPTED_FILE,
        DECRYPTED_FILE,
        PASSWORD
    )

    print("❌ TAMPER TEST FAILED")

    print(
        "Modified encrypted file was accepted."
    )

except ValueError as error:

    print("✓ TAMPER TEST PASSED")

    print(
        "✓ Modified encrypted file was rejected."
    )

    print(
        "✓ AES-GCM authentication detected tampering."
    )

    print(
        "Reason:",
        error
    )


# ==============================
# COMPLETE
# ==============================

print("\n" + "=" * 60)

print("TAMPER DETECTION TEST COMPLETED")

print("=" * 60)