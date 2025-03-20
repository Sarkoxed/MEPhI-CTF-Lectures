import json
import os
import pprint
import eth_account
import eth_abi
from eth_abi import encode

from utils import create_transaction, get_abi, web3, myaddr, private_key
from sha3 import keccak_256

if not os.path.exists("abi.json"):
    get_abi("dao.sol")

abi = json.load(open("abi.json", encoding="ascii"))
abi_checkowner = abi["dao.sol:OffchainCheckOwner"]["abi"]
abi_dao = abi["dao.sol:DAO"]["abi"]

contract_address = "0x1DeAab462C2146A3EaB78337a14B679b68B8630f"

dao_ctr = web3.eth.contract(address=contract_address, abi=abi_dao)
pprint.pprint([x for x in dir(dao_ctr.functions) if "__" not in x])


def register():
    print(dao_ctr.functions.register().call())


def get_owner():
    return dao_ctr.functions.owner().call()


def change_dao_owner(v: int, r: bytes, s: bytes, salt: bytes, new_owner: str):
    func = dao_ctr.functions.changeDAOowner(v, r, s, salt, new_owner)
    create_transaction(func)


print("Owner: ", get_owner())
#
#
#def parse_owners():
#    tx_hash = "0x56bc2af1e01f707e613fc6d9bfaee1ed0b020a6105d24c0bdc6b0f1a4b59b07b"
#    tx = web3.eth.get_transaction(tx_hash).input.hex()[10:]
#    tmp = [tx[i : i + 64] for i in range(0, len(tx), 64)][3:]
#    print(len(tmp))
#    vals = tmp[: 16 * 60]
#    vals = [int(x, 16) for x in vals]
#    owners = tmp[16 * 60 + 1 :]
#    assert len(owners) == 60
#    res_dick = {}
#    for i in range(0, len(vals), 16):
#        owner = owners[i // 16]
#        vals1 = list(
#            zip(
#                vals[i : i + 4],
#                vals[i + 4 : i + 8],
#                vals[i + 8 : i + 12],
#                vals[i + 12 : i + 16],
#            )
#        )
#        res_dick[owner] = vals1
#    return res_dick
#
#
#all_owners = parse_owners()
#
#
#cur_owner = [
#    (
#        em.args.v,
#        int.from_bytes(em.args.r, "big"),
#        int.from_bytes(em.args.s, "big"),
#        int.from_bytes(em.args.hash, "big"),
#    )
#    for em in dao_ctr.events.Signed().get_logs(fromBlock=7437751)
#]
#
#
##pprint.pprint(all_owners[get_owner().lower()[2:].zfill(64)])
#pprint.pprint(cur_owner)
#


#n = 115792089237316195423570985008687907852837564279074904382605163141518161494337
#print(n)
#print(cur_owner)

ds = (67680355535899468608424342199345503336219138300059011448414238556164317524682, 41238211154220600516470729144023878506965877124816775514328554270754368322607)
ds = (67680355535899468608424342199345503336219138300059011448414238556164317524682, 41238211154220600516470729144023878506965877124816775514328554270754368322607)

ds = [68786574691016430472744193541595946432796574499288350939775154080095194390223, 10810645280651107768414247596738948469892304680748292138431614875023945369863]

ds = [(104546331485828494346076483596644144759490059654879220102145839803594825013207,
  1),
 (30349525136353709735154458868052654224659516527312993639400967974752780307560,
  1),
 (1176779771253890295203617246283166210812699361079578336319900559891576507022, 1)
  ]
ds = [x[0] for x in ds]


for d  in ds:
    acc1 = eth_account.Account.from_key(d)
    print(acc1.address)



# r = int.from_bytes(r1, 'big')
# s1 = int.from_bytes(s1, 'big')
# s2 = int.from_bytes(s2, 'big')
# h1 = int.from_bytes(h1, 'big')
# h2 = int.from_bytes(h2, 'big')
# k = (h1 - h2) * pow(s1 - s2, -1, n) % n
# d = (s1 * k - h1) * pow(r, -1, n) % n
# print(d)
# d2 = (s2 * k - h2) * pow(r, -1, n) % n
# assert d2 == d
#
# acc = eth_account.Account.from_key(hex(d)[2:].zfill(64))
#
# value = 17329992840538346
# uint8_value = 0x1
# salt = os.urandom(32)
#
#
# encoded_data = encode(['uint8', 'uint256', 'bytes32'], [uint8_value, value, salt])
# hash_result = keccak_256(encoded_data).digest()
#
# from eth_account._utils.signing import sign_message_hash
# key_obj = eth_account.Account._parsePrivateKey(d)
# print(key_obj, type(key_obj))
# v, r, s, _ = sign_message_hash(key_obj, hash_result)
#
# change_dao_owner(v, r.to_bytes(32, 'big'), s.to_bytes(32, 'big'), salt, myaddr)
# print(get_owner(), myaddr)
