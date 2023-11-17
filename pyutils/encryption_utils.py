import string
import rsa
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.backends import default_backend


def encrypt1(message: str):
    encrypted = ""
    for c in message:
        if c.isnumeric() or (c.isupper() is False and c.islower() is False):
            encrypted += c
            continue

        if c.isupper(): letters = string.ascii_uppercase
        else: letters = string.ascii_lowercase

        i = letters.index(c)
        n = i + 6
        if n >= 26: n -= 26
        encrypted += letters[n]

    return encrypted

def encrypt2(message):
    message = message.encode('utf-8')
    puk = ""
    with open('public4.key', 'rb') as f:
        puk = f.read()

    puk = rsa.PublicKey.load_pkcs1(puk)

    # Generate a random symmetric encryption key
    symmetric_key = rsa.randnum.read_random_bits(256)

    # Encrypt the plaintext using AES
    aes_cipher = Cipher(algorithms.AES(symmetric_key), modes.CBC(b'\x00' * 16), backend=default_backend())
    aes_encryptor = aes_cipher.encryptor()
    padder = padding.PKCS7(algorithms.AES.block_size).padder()
    padded_plaintext = padder.update(message) + padder.finalize()
    ciphertext = aes_encryptor.update(padded_plaintext) + aes_encryptor.finalize()

    # Encrypt the symmetric key using RSA
    encrypted_symmetric_key = rsa.encrypt(symmetric_key, puk)

    ct = f"!!Key::{encrypted_symmetric_key}::yeK!!{ciphertext}"
    return ct

def encrypt(message):
    size = 245
    # with open('keys/public4.key', 'rb') as f:
    #     public_key_pem = f.read()

    public_key_pem = """-----BEGIN RSA PUBLIC KEY-----
MIIBCgKCAQEAzRPwZAw/ihl5uNOMFrGeZyU2jhHXmBtwunHQA7xXHBv8w0iqtyo9
oSxLyjh069a2vKxicQL9rqvQejUpfJfXQeqsex8IdRoBzUfCJ0N5yw7jjNCESdz0
s95wa56sLMY5+LWDPM1EnYgRbuZrM0rZaxuA9v+HsPwiLUB8KOFe/MWrz3roo0c1
TtUhkJ4gDu0mQ8iv9NdhtpHiq6s6G2rLVSUujSU45VaS75hYIGoDRdux1D5WPUGB
2f0u46GZixms9zQqMItRHdAzq7cO2cN0/iig74zlGUY88dd57cBti64k9ehgFage
jJt+kuRDYH7Hg/5iTzj4wTHhrwib2TpbIwIDAQAB
-----END RSA PUBLIC KEY-----
"""
    public_key = rsa.PublicKey.load_pkcs1(public_key_pem)

    blocks = []
    toenc = []

    done = False
    current = message
    while done is False:
        if len(current) < size:
            toenc.append(current)
            break
        toenc.append(current[:size])
        current = current[size:]

    for ptext in toenc:
        ctext = rsa.encrypt(ptext.encode('utf-8'), public_key)
        blocks.append(ctext.hex())

    return "!!".join(blocks)