from fastecdsa import keys, curve, ecdsa, keys
from fastecdsa.encoding.der import DEREncoder
from fastecdsa.point import Point
from fastecdsa.curve import secp256k1,P256
from web3 import Web3
import base58
import hashlib
import Rigs

key = Rigs.Key()
key.Generate()
print(key.address)
print(key.public_key)
print(key.private_key)

def Generate():
    priv_key = keys.gen_private_key(curve.P256)
    #print(type(priv_key))
    pub_key = keys.get_public_key(priv_key, curve.P256)
    return priv_key,pub_key

def Encode(key):
    encoded = DEREncoder.encode_signature(key.x,key.y)
    return encoded

def Decode(key):
    x,y = DEREncoder.decode_signature(key)
    S = Point(x,y, curve=P256)
    return S

def Sign(data,priv_key):
    r, s = ecdsa.sign(data, priv_key)
    return DEREncoder.encode_signature(r,s)

def Verify(signature,data,pub_key):
    return ecdsa.verify(DEREncoder.decode_signature(signature), data, pub_key)

def Address():
    return (base58.b58encode(hashlib.md5(Encode(pub_key)).hexdigest()).decode())


'''
G = P256.G

recv_sk = keys.gen_private_key(curve.P256)
recv_pk = keys.get_public_key(recv_sk, curve.P256)#G*recv_sk

send_sk = keys.gen_private_key(curve.P256)
send_pk = keys.get_public_key(send_sk, curve.P256)#G*send_sk

random_value = keys.gen_private_key(curve.P256)
send_addr = (recv_pk * random_value)
print(send_addr)

recv_private_key = (recv_sk * random_value)
recv_public_key = keys.get_public_key(recv_private_key, curve.P256)
print(recv_public_key)
'''
