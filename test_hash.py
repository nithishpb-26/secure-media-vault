from modules.hash_utils import calculate_sha256


FILE = "test.jpg"


print("=" * 50)
print("SHA-256 FILE INTEGRITY TEST")
print("=" * 50)


print("\nCalculating SHA-256 hash...")

file_hash = calculate_sha256(FILE)


print("\nFile:")
print(FILE)

print("\nSHA-256:")
print(file_hash)

print("\nHash length:")
print(len(file_hash))

print("\n✓ SHA-256 hashing completed")

print("=" * 50)