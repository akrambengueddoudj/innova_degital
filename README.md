# 🔐 SafeB2BExchange - Overview

**SafeB2BExchange** is a Django-based secure document exchange platform developed for **Challenge 3** of Innova Digital Hackathon. It enables encrypted document sharing between agents and clients, incorporating digital signatures, audit logging, and role-based access control to ensure trust and traceability in B2B transactions.

---

## 🔑 Security Overview

SafeB2BExchange uses the following mechanisms to secure data transmission and storage:

- **Symmetric Encryption:** Uploaded documents are encrypted using Fernet (AES-based), ensuring data is unreadable at rest.
- **Digital Signatures:** Both senders and receivers digitally sign documents using their RSA private keys to verify authenticity and detect tampering.
- **Audit Logging:** All sensitive operations — uploads, downloads, and signatures — are logged with timestamps and user references.
- **Private Key Management:** Keys are stored outside the database and are loaded securely via environment variables.

> ⚠️ **End-to-End Encryption (E2EE):**  
> The project is structured to support true E2EE in future versions by incorporating hybrid encryption (AES + RSA) and client-side decryption. Current encryption is server-handled for practicality in this phase.

---

## 🐧 System Compatibility

> ⚠️ Important Note:  
> This project was developed and tested on Ubuntu/Linux, which ensures:
>
> - Better compatibility with Linux-based self-hosted servers (Apache, NGINX).
> - Native support for shell scripts, permissions, and case-sensitive paths.
>
> 🪟 Windows Warning:  
> On Windows environments, some features (like file paths or deployment scripts) may not function as expected without modifications.

---

## 🎯 Challenge Objectives & How They're Met

| Objective                                         | Implementation                                                                 |
|--------------------------------------------------|--------------------------------------------------------------------------------|
| **1. Secure file exchange**                      | Files are encrypted before storage using AES encryption.                       |
| **2. Mutual document signing**                   | Sender and receiver sign the document using RSA-based digital signatures.      |
| **3. Tamper-proof history (audit trail)**        | Detailed audit logs track actions (upload/download/sign) by user and time.     |
| **4. Role-based interactions (agent/client)**    | Custom user profiles and access control restrict actions based on role.        |
| **5. Integrity and non-repudiation**             | Digital certificates and signatures ensure authenticity; signed files are immutable.            |
| **6. Potential for E2EE adoption**               | Architecture supports upgrading to hybrid encryption with client-side decryption. |

---
