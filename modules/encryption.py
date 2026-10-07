
import os
import struct

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


MAGIC = b"SEIS"
VERSION = 1

SALT_SIZE = 16
NONCE_SIZE = 12
KEY_SIZE = 32

PBKDF2_ITERATIONS = 600_000


def derive_key(password, salt):
    """Create a 256-bit key from the password."""

    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=KEY_SIZE,
        salt=salt,
        iterations=PBKDF2_ITERATIONS,
    )

    return kdf.derive(password.encode("utf-8"))


def validate_password(password):
    """Check whether the password meets minimum security requirements."""

    if not password:
        return False, "Password is required."

    if len(password) < 8:
        return False, "Password must contain at least 8 characters."

    if not any(char.isupper() for char in password):
        return False, "Password must contain an uppercase letter."

    if not any(char.islower() for char in password):
        return False, "Password must contain a lowercase letter."

    if not any(char.isdigit() for char in password):
        return False, "Password must contain a number."

    if not any(not char.isalnum() for char in password):
        return False, "Password must contain a special character."

    return True, "Password is strong."


def encrypt_file(input_path, output_path, password):

    with open(input_path, "rb") as file:
        data = file.read()

    salt = os.urandom(SALT_SIZE)
    nonce = os.urandom(NONCE_SIZE)

    key = derive_key(password, salt)

    aes = AESGCM(key)

    ciphertext = aes.encrypt(
        nonce,
        data,
        None
    )

    header = (
        MAGIC +
        struct.pack("B", VERSION) +
        salt +
        nonce
    )

    with open(output_path, "wb") as file:
        file.write(header)
        file.write(ciphertext)

    return True


def decrypt_file(input_path, output_path, password):

    with open(input_path, "rb") as file:
        data = file.read()

    header_size = 4 + 1 + SALT_SIZE + NONCE_SIZE

    if len(data) <= header_size:
        raise ValueError("Invalid encrypted file.")

    if data[:4] != MAGIC:
        raise ValueError("Invalid SEIS encrypted file.")

    version = data[4]

    if version != VERSION:
        raise ValueError("Unsupported encrypted file version.")

    salt_start = 5
    salt_end = salt_start + SALT_SIZE

    nonce_start = salt_end
    nonce_end = nonce_start + NONCE_SIZE

    salt = data[salt_start:salt_end]
    nonce = data[nonce_start:nonce_end]

    ciphertext = data[nonce_end:]

    key = derive_key(password, salt)

    aes = AESGCM(key)

    try:

        plaintext = aes.decrypt(
            nonce,
            ciphertext,
            None
        )

    except Exception:

        raise ValueError(
            "Decryption failed. Wrong password or corrupted file."
        )

    with open(output_path, "wb") as file:
        file.write(plaintext)

    return True
