from eth_account import Account
from eth_account.messages import encode_defunct
from fastecdsa.curve import Curve, secp256k1
from fastecdsa.ecdsa import sign, verify
from fastecdsa.keys import gen_keypair, import_key
from fastecdsa.point import Point
from sha3 import keccak_256

# Define your custom curve parameters here
a = 0
b = 7
q = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
gx = 55066263022277343669578718895168534326250603453777594175500187360389116729240
gy = 32670510020758816978083085130507043184471273380659243275938904335757337482424
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337  # e.order
h = 1

custom_curve = Curve(
    name="custom_curve",
    p=q,
    a=a,
    b=b,
    q=n,
    gx=gx,
    gy=gy,
)

custom_curve = secp256k1
G = custom_curve.G


def pad(message):
    message_prefix = f"\x19Ethereum Signed Message:\n{len(message)}"
    return message_prefix.encode() + message.encode()


def get_hash(message):
    return keccak_256(pad(message)).digest()


def ethereum_sign(message, private_key, curve):
    r, s = sign(message, private_key, curve=curve, hashfunc=keccak_256)
    return r, s


def ethereum_verify(message, r, s, v, public_key, curve=custom_curve):
    # Prefix the message
    msg = pad(message)
    # Verify the signature
    return verify((r, s), msg, public_key, curve, hashfunc=keccak_256)

def test():
    key = "0ababa".zfill(64)
    # acc = Account.from_key(key)
    msg = "Pidoras"
    msgHash = encode_defunct(text=msg)
    signed = Account.sign_message(msgHash, key)

    message_hash = get_hash(msg)
    assert message_hash == signed.messageHash
    print(message_hash)

    r, s = ethereum_sign(pad(msg), int(key, 16), custom_curve)
    print("My")
    print(r, s, sep="\n")
    print("Them")
    print(signed.r, signed.s, signed.v, signed.signature, sep="\n")

    print(ethereum_verify(msg, signed.r, signed.s, signed.v, int(key, 16) *G, custom_curve))
    
    print(ethereum_verify(msg, r, s, signed.v, int(key, 16) *G, custom_curve))

#test()
