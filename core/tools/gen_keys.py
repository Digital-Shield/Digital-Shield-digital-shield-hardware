from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from cryptography.hazmat.primitives import serialization

# Generate a new Ed25519 private key
private_key = Ed25519PrivateKey.generate()

# Get the public key from the private key
public_key = private_key.public_key()

# Convert keys to hexadecimal format

private_key_hex = private_key.private_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PrivateFormat.Raw,
    encryption_algorithm=serialization.NoEncryption()
).hex()

public_key_hex = public_key.public_bytes(
    encoding=serialization.Encoding.Raw,
    format=serialization.PublicFormat.Raw
).hex()

# Print the keys
print(f"固件私钥(Hex): {private_key_hex}")
print(f"固件公钥(Hex): {public_key_hex}")


