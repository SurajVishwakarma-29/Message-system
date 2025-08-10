from Crypto.Cipher import AES
import base64
import os

key = os.environ.get('SECRET_KEY', b'\x14\x94m\xe4>K\xc6\x8ec\xac\x1e\x06\xf4\xa1a\x93')  # 16 bytes for AES-128

def encrypt_message(msg):
    cipher = AES.new(key, AES.MODE_EAX)
    nonce = cipher.nonce
    ciphertext, tag = cipher.encrypt_and_digest(msg.encode('utf-8'))
    return base64.b64encode(nonce + ciphertext).decode('utf-8')

def decrypt_message(enc_msg):
    enc = base64.b64decode(enc_msg)
    nonce = enc[:16]
    ciphertext = enc[16:]
    cipher = AES.new(key, AES.MODE_EAX, nonce=nonce)
    return cipher.decrypt(ciphertext).decode('utf-8')
