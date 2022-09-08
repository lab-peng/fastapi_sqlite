import base64
from aes_pkcs5.algorithms.aes_ecb_pkcs5_padding import AESECBPKCS5Padding
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from Crypto.PublicKey import RSA
from config import settings

aeskey = settings.aeskey
cipher = AESECBPKCS5Padding(aeskey, 'b64')
pubkey = RSA.import_key(settings.pubkey)
privkey = RSA.import_key(settings.privkey)


# 加密
def encrypt(data: str) -> str:
    return cipher.encrypt(data)


# 解密
def decrypt(data: str) -> str:
    return cipher.decrypt(data)


# 签名
def sign(encrypted_data: str) -> str:
    signer = PKCS1_v1_5.new(privkey)
    hashed_data = SHA256.new(encrypted_data.encode())
    signature = base64.b64encode(signer.sign(hashed_data))
    return signature.decode('ascii')


# 验签
def sign_verify(signature, encrypted_data):
    hashed_data = SHA256.new(encrypted_data.encode())
    verifier = PKCS1_v1_5.new(pubkey)
    return verifier.verify(hashed_data, base64.b64decode(signature.encode('ascii')))


# print(encrypt(query_json))

# print(decrypt(encrypt(query_json)))


# print(sign(encrypt(query_json)))

# print(sign_verify(sign(encrypt(query_json)), encrypt(query_json)))

x = {
    "data": "oqD1E0EIneoWz2efgFbgOfPkIBj8d0ACyM3f8AsB5M6p2Mf3YjCx4v6aKJJ3HzDUrK51oiRLxvs7EVYVhmobaZQOI+PV22fgUcfn3duyYg3zZLkxAFjt31XA9FWN4BzMoBeeCdr5ThaZ737oLxTOl2OX4T8koJQqeJdxgmiRd7IBlFchGrhxzcmNCBOFcGs7H8nqSzZ1AcUs9VwyUYmBG0hZmFpVcRHh5zP5KVE5KNiQzbNPGgCiOXstOnOXn0xU5kChVZG",
    "sign": "/DALwfeluoEQ9IJ6WxIGCBCXP4JKsTSmglPqSQojoErqZEwu2lZ4wyxmQMkPz+F8ekMPC0pRFeN+o7KLJDUDgkwrNk6Xer+Q6hCf3C3/x3ZrN0dkxTiy578ojQCqymWlzB/VP26sja5sI56/ruYuSCEmjbTortqxBvFb+OsVbAU4TRBVHA9VJGJgF2WydRG/ZYqTVFdXHTGOQ3NuM9BN1JduKZwYiu4wXX2z8QpEipdZlS6LS86pLOySdtjsJX7CSjOoNrQQdtbkizaoR7dGMVGKevrz629w8TCvXN1Nco9pXCCPb0wstmIureTPghnkIztKQaibCaPVmXQ=="
}

# print(decrypt(x['data']))
# print(sign_verify(x['sign'], x['data']))





