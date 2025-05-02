# utils/crypto_utils.py
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend
from cryptography import x509

# Load private key
def load_private_key(path):
    with open(path, "rb") as key_file:
        return serialization.load_pem_private_key(
            key_file.read(), password=None, backend=default_backend()
        )

# Load public key from certificate
def load_public_key_from_cert(path):
    with open(path, "rb") as cert_file:
        cert = x509.load_pem_x509_certificate(cert_file.read(), default_backend())
        return cert.public_key()

# Sign a file
def sign_data(data: bytes, private_key_path: str) -> bytes:
    private_key = load_private_key(private_key_path)
    return private_key.sign(
        data,
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

# Verify a signature
def verify_signature(data: bytes, signature: bytes, cert_path: str) -> bool:
    public_key = load_public_key_from_cert(cert_path)
    try:
        public_key.verify(
            signature,
            data,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )
        return True
    except Exception:
        return False
