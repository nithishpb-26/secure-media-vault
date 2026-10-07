from modules.encryption import encrypt_file, decrypt_file


CORRECT_PASSWORD = "MySecurePassword123!"
WRONG_PASSWORD = "WrongPassword123!"


print("=" * 50)
print("SECURE VIDEO ENCRYPTION SECURITY TEST")
print("=" * 50)


print("\n[1] Encrypting video with correct password...")

encrypt_file(
    "test.mp4",
    "encrypted/test.mp4.enc",
    CORRECT_PASSWORD
)

print("✓ Video encrypted successfully")


print("\n[2] Trying to decrypt with WRONG password...")

try:

    decrypt_file(
        "encrypted/test.mp4.enc",
        "decrypted/test_wrong_password.mp4",
        WRONG_PASSWORD
    )

    print("❌ SECURITY TEST FAILED")

except ValueError as error:

    print("✓ SECURITY TEST PASSED")
    print("✓ Wrong password was rejected")
    print("Reason:", error)


print("\n" + "=" * 50)
print("TEST COMPLETED")
print("=" * 50)