# 🔐 Secure Media Vault

### Secure Image & Video Encryption System

Secure Media Vault is a Python-Flask based cybersecurity application designed to securely encrypt and decrypt image and video files using modern cryptographic techniques.

The system provides password-protected media encryption, file integrity verification, authentication, encryption/decryption history, security logging, and a security dashboard.

---

## 📌 Project Overview

Digital images and videos often contain sensitive or personal information. Storing these files without proper protection can expose them to unauthorized access.

**Secure Media Vault** addresses this problem by providing a secure local web application where users can:

* Upload image and video files
* Encrypt files using **AES-256-GCM**
* Protect encryption keys using password-based key derivation
* Decrypt files using the correct password
* Verify file integrity using **SHA-256**
* Authenticate users securely
* Maintain encryption/decryption history
* Record security events
* Monitor activity through a security dashboard

---

## 🎯 Objectives

The main objectives of this project are:

1. Protect sensitive image and video files from unauthorized access.
2. Implement strong symmetric encryption.
3. Secure encryption keys using password-based key derivation.
4. Detect corrupted or modified encrypted files.
5. Provide secure user authentication.
6. Maintain an audit trail of security-related activities.
7. Provide a simple web-based interface for secure media management.

---

## ✨ Features

### 🔒 Media Encryption

* Supports image and video files.
* Uses **AES-256-GCM** authenticated encryption.
* Generates a unique random salt for every encryption.
* Generates a unique random nonce for every encryption.
* Authentication tag protects ciphertext integrity.

### 🔑 Password-Based Security

Passwords are processed using:

* PBKDF2-HMAC-SHA256
* 600,000 iterations
* Random salt
* 256-bit derived encryption key

The application does not store encryption passwords in plaintext.

### 🛡️ File Integrity Verification

The application calculates a SHA-256 hash for files.

This can be used to detect:

* File modification
* File corruption
* Unexpected changes to decrypted files

### 👤 User Authentication

The application includes:

* Login system
* Password hashing
* Random password salts
* Password verification
* Password change functionality
* Session-based authentication

### 📜 Security Logging

Security-related activities are recorded in the database.

Examples include:

* Successful login
* Failed login
* Password changes
* Successful encryption
* Failed encryption/decryption
* Successful decryption
* Failed authentication attempts

### 📊 Security Dashboard

The security dashboard provides visibility into application activity, including:

* Total operations
* Successful operations
* Failed operations
* Encryption count
* Decryption count
* Security events

### 🗃️ Operation History

Encryption and decryption operations are stored with information such as:

* Filename
* Operation
* Status
* File size
* SHA-256 hash
* Timestamp

---

## 🔐 Cryptographic Architecture

The encryption process follows this general architecture:

```text
                    User Password
                         │
                         ▼
                ┌─────────────────┐
                │      PBKDF2     │
                │ HMAC-SHA256     │
                │ 600,000 rounds  │
                └────────┬────────┘
                         │
                         ▼
                  256-bit Key
                         │
                         ▼
              ┌──────────────────┐
              │    AES-256-GCM    │
              │    Encryption     │
              └────────┬─────────┘
                       │
                       ▼
                 Encrypted File
                       │
                       ▼
              SHA-256 Integrity Hash
```

---

## 📦 Encrypted File Format

Encrypted files contain a custom header followed by the encrypted data.

Conceptually:

```text
┌──────────────┬─────────┬──────────────┬────────────────────┐
│ Magic Header │ Version │     Salt     │       Nonce        │
├──────────────┼─────────┼──────────────┼────────────────────┤
│    SEIS      │    1    │   16 bytes   │     12 bytes       │
└──────────────┴─────────┴──────────────┴────────────────────┘
                         +
                  AES-GCM Ciphertext
                         +
                 Authentication Tag
```

### Parameters

| Component         | Value                            |
| ----------------- | -------------------------------- |
| Encryption        | AES-256-GCM                      |
| Key size          | 256-bit                          |
| KDF               | PBKDF2-HMAC-SHA256               |
| PBKDF2 iterations | 600,000                          |
| Salt              | 16 bytes                         |
| Nonce             | 12 bytes                         |
| Integrity         | AES-GCM authentication + SHA-256 |

---

## 🧱 Technology Stack

### Backend

* Python
* Flask

### Cryptography

* AES-256-GCM
* PBKDF2-HMAC-SHA256
* SHA-256
* Python `cryptography` library

### Database

* SQLite

### Frontend

* HTML5
* CSS3
* Flask/Jinja templates

### Development Tools

* Visual Studio Code
* Git
* GitHub
* Python Virtual Environment

---

## 📂 Project Structure

```text
Secure_Encryption_System/
│
├── app.py
├── requirements.txt
├── .env
├── .gitignore
│
├── test.jpg
├── test.mp4
├── test_encryption.py
├── test_video.py
├── test_database.py
├── test_tamper.py
├── test_hash.py
│
├── database/
│   ├── __init__.py
│   ├── database.py
│   ├── users.py
│   └── encryption.db
│
├── modules/
│   ├── __init__.py
│   ├── encryption.py
│   ├── decryption.py
│   └── hash_utils.py
│
├── encrypted/
├── decrypted/
├── uploads/
├── logs/
│
├── static/
│   └── style.css
│
├── templates/
│   ├── index.html
│   ├── history.html
│   ├── login.html
│   ├── change_password.html
│   ├── security_logs.html
│   └── security_dashboard.html
│
└── venv/
```

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/nithishpb-26/secure-media-vault.git
```

Navigate into the project:

```bash
cd secure-media-vault
```

---

## 2. Create a Virtual Environment

### Windows

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, run:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```

Then activate again:

```powershell
.\venv\Scripts\Activate.ps1
```

---

## 3. Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## 4. Environment Variables

Create a `.env` file in the project root if your local configuration requires environment variables.

Example:

```env
SECRET_KEY=your-secret-key
```

For a deployed environment, use a strong randomly generated secret key rather than committing secrets to GitHub.

**Never commit passwords, API keys, or other secrets to the repository.**

---

# ▶️ Running the Application

Activate the virtual environment:

```powershell
.\venv\Scripts\Activate.ps1
```

Start Flask:

```powershell
python app.py
```

The application will normally be available at:

```text
http://127.0.0.1:5000
```

Open the address in your browser.

---

# 🔑 Login

The application uses a database-backed user authentication system.

A default administrator can be configured using environment variables:

```env
ADMIN_USERNAME=your_username
ADMIN_PASSWORD=your_password
```

The application initializes the administrator account when configured.

### Important

Do not publish your actual administrator password in:

* GitHub
* README files
* Screenshots
* Project reports
* Public repositories

---

# 🖼️ How to Use

## 1. Login

Open the application and log in with your configured account.

```text
Login
  │
  ▼
Authentication
  │
  ▼
Secure Media Vault
```

---

## 2. Upload Media

Select an image or video file through the application.

Supported media can include:

```text
.jpg
.jpeg
.png
.gif
.mp4
```

Additional formats may be supported depending on the application's validation configuration.

---

## 3. Encrypt

Enter the encryption password and start the encryption process.

The application:

1. Reads the file.
2. Generates a random salt.
3. Derives a 256-bit key using PBKDF2-HMAC-SHA256.
4. Generates a random nonce.
5. Encrypts the file using AES-256-GCM.
6. Stores the encrypted output.
7. Calculates the SHA-256 hash.
8. Records the operation in the database.
9. Records a security event.

---

## 4. Decrypt

Select an encrypted file and provide the correct password.

The application verifies the encrypted data using AES-GCM authentication.

If the password is incorrect or the encrypted file has been modified, decryption fails.

Example error:

```text
Decryption failed. Wrong password or corrupted file.
```

---

# 🧪 Testing

The project contains several test scripts.

### Encryption Test

```powershell
python test_encryption.py
```

### Video Encryption Test

```powershell
python test_video.py
```

### Database Test

```powershell
python test_database.py
```

### Tamper Detection Test

```powershell
python test_tamper.py
```

### Hash Test

```powershell
python test_hash.py
```

These tests help verify the core security and database functionality.

---

# 🛡️ Security Design

The project follows several security principles.

### 1. Strong Encryption

AES-256-GCM provides both confidentiality and authenticated encryption.

### 2. Unique Salt

A random salt is generated for each encryption operation.

This prevents the same password from producing the same encryption key across files.

### 3. Unique Nonce

AES-GCM uses a randomly generated nonce for each encryption operation.

### 4. Password-Based Key Derivation

PBKDF2 increases the computational cost of password guessing attacks.

### 5. Authentication

AES-GCM authentication detects unauthorized modification of encrypted data.

### 6. Password Hashing

User passwords are stored using PBKDF2-HMAC-SHA256 with a unique salt.

### 7. Integrity Verification

SHA-256 hashes provide an additional mechanism for verifying file integrity.

### 8. Security Audit Trail

Important security events are stored in the database for monitoring and investigation.

---

# 📊 Database

The application uses SQLite.

### Encryption History

The `encryption_history` table stores information such as:

```text
id
filename
operation
status
file_size
sha256
timestamp
```

### Users

The `users` table stores:

```text
id
username
password_hash
salt
created_at
```

### Security Logs

The `security_logs` table stores security events such as:

```text
LOGIN_SUCCESS
LOGIN_FAILED
PASSWORD_CHANGED
ENCRYPT_SUCCESS
DECRYPT_SUCCESS
```

---

# 🚨 Threats Addressed

The system is designed to reduce the risk of:

* Unauthorized media access
* Password guessing
* Encrypted file tampering
* File corruption
* Unauthorized decryption
* Weak password storage
* Lack of security auditing

---

# ⚠️ Limitations

This project is intended primarily as an educational cybersecurity project.

Current limitations include:

* SQLite is suitable for a small/local deployment but is not ideal for high-concurrency production systems.
* Large video files are currently processed in memory and may require significant RAM.
* The Flask development server should not be used as a production server.
* Additional access-control mechanisms would be required for a large multi-user production system.
* Production deployments should use secure HTTPS configuration.
* Cloud deployments require persistent storage for uploaded, encrypted, decrypted, and database files.

---

# 🚀 Future Enhancements

Possible future improvements include:

* [ ] Chunk-based/streaming encryption for large videos
* [ ] Multi-user role-based access control
* [ ] Two-factor authentication
* [ ] Password recovery mechanism
* [ ] Automatic file expiration
* [ ] Secure cloud storage integration
* [ ] Malware scanning before encryption
* [ ] Advanced audit-log analysis
* [ ] Email security alerts
* [ ] Rate limiting for login attempts
* [ ] Account lockout after repeated failures
* [ ] Improved file-type validation
* [ ] Docker deployment
* [ ] Production-grade database
* [ ] Security monitoring integration
* [ ] SIEM integration

---

# 🔍 Cybersecurity Concepts Demonstrated

This project demonstrates practical knowledge of:

* Cryptography
* Symmetric encryption
* AES-GCM
* Password-based key derivation
* PBKDF2
* Cryptographic hashing
* File integrity
* Authentication
* Session management
* Secure password storage
* SQLite database security
* Security logging
* Audit trails
* Web application security
* Secure file handling
* Cybersecurity monitoring

---

# 💼 Project Relevance

This project is particularly relevant to cybersecurity roles such as:

* SOC Analyst
* Security Analyst
* Cybersecurity Engineer
* Application Security Intern
* Information Security Analyst
* Security Operations Intern

It demonstrates both **software development** and **cybersecurity fundamentals** through a practical application.

---

# 📸 Screenshots

Add screenshots of your application here.

Recommended screenshots:

### Login Page

```text
Add screenshot here
```

### Secure Media Vault Dashboard

```text
Add screenshot here
```

### Encryption Result

```text
Add screenshot here
```

### Decryption Result

```text
Add screenshot here
```

### Security Dashboard

```text
Add screenshot here
```

### Security Logs

```text
Add screenshot here
```

### Encryption History

```text
Add screenshot here
```

---

# 📋 Example Workflow

```text
             ┌──────────────┐
             │     Login    │
             └──────┬───────┘
                    │
                    ▼
          ┌───────────────────┐
          │ Secure Media Vault│
          └─────────┬─────────┘
                    │
          ┌─────────┴─────────┐
          │                   │
          ▼                   ▼
     Encrypt File        Decrypt File
          │                   │
          ▼                   ▼
      PBKDF2 KDF          Password
          │               Verification
          ▼                   │
     AES-256-GCM              ▼
          │              AES-GCM Verify
          ▼                   │
    Encrypted File            ▼
          │             Decrypted File
          │
          ▼
      SHA-256 Hash
          │
          ▼
     Security Log
          │
          ▼
       Database
```

---

# 📁 Output Directories

The application uses separate directories for different file operations:

```text
uploads/
    Uploaded files

encrypted/
    Encrypted media

decrypted/
    Decrypted media

logs/
    Application/security-related logs
```

Sensitive generated files should not be committed to the public repository.

---

# 🔐 Git Security

Before pushing the project to GitHub, ensure sensitive files are excluded.

Example `.gitignore`:

```gitignore
venv/
__pycache__/
*.pyc

.env

database/*.db

uploads/*
encrypted/*
decrypted/*
logs/*

*.mp4
*.jpg
*.jpeg
*.png
```

Never commit:

```text
.env
passwords
API keys
private keys
database files containing real user information
private media files
```

---

# 📜 License

This project is created for educational and academic purposes.

You may adapt the project for learning, research, and non-commercial educational use.

---

# ⚠️ Disclaimer

Secure Media Vault is an educational cybersecurity project and should not be considered a complete production-grade secure storage platform.

For production use, the application should undergo professional security testing, threat modeling, penetration testing, secure deployment configuration, access-control review, and cryptographic implementation review.

---

# 👨‍💻 Author

**Nithish P B**

Cybersecurity / Information Science Engineering Student

GitHub:

https://github.com/nithishpb-26

Project Repository:

https://github.com/nithishpb-26/secure-media-vault

---

# ⭐ Acknowledgements

This project was developed as a cybersecurity-focused academic project to explore practical implementation of:

* Secure file encryption
* Cryptographic key derivation
* Authentication
* File integrity
* Security logging
* Web application security

---

## 🔐 Secure Your Media. Protect Your Data.
