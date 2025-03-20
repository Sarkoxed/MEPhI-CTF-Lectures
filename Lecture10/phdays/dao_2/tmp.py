import json
import os
import pprint
import eth_account
import eth_abi
from eth_abi import encode
from time import sleep

from utils import create_transaction, get_abi, web3, myaddr, send_transaction
from sha3 import keccak_256

abi = json.load(open("abi.json", encoding="ascii"))
abi_checkowner = abi["dao.sol:OffchainCheckOwner"]["abi"]
abi_dao = abi["dao.sol:DAO"]["abi"]

contract_address = "0x14aBcFE53C3101e271DacfAcC103a9c374379120"

dao_ctr = web3.eth.contract(address=contract_address, abi=abi_dao)
pprint.pprint([x for x in dir(dao_ctr.functions) if "__" not in x])

def register():
    print(dao_ctr.functions.register().call())

def send_transaction1(to, amount, pkey):
    transaction = {
            "to": to,
            "value": amount,
            "nonce": web3.eth.get_transaction_count(myaddr),
            "gasPrice": web3.to_wei(50, 'gwei'),
            "gas": 21000,
            "chainId": 80002
    }
    signed_txn = web3.eth.account.sign_transaction(transaction, pkey)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f'Transaction sent with hash: {txn_hash.hex()}')

#key = "0x" + str(10).zfill(64)
#acc = eth_account.Account.from_key(key)
#send_transaction1(acc.address, 10**14, "0x" + "1".zfill(64))

#print(dao_ctr.functions.owner().call())
#print(acc.address)

#for i in range(1, 11):
#    key = "0x" + str(i).zfill(64)
#    acc = eth_account.Account.from_key(key)
#    blc = web3.eth.get_balance(acc.address)
#    print(blc, i)
#    #if blc < 3 * 10**16:
#    #    send_transaction(acc.address, 3 * 10**16 - blc)
#    #    sleep(10)
#    send_transaction1(myaddr, blc - web3.eth.gas_price * 21000, key)
#
#    #try:
#    #    #func = dao_ctr.functions.register()
#    #    func = dao_ctr.functions.voteForYourself()
#    #    create_transaction(func, key, acc.address)
#    #except Exception as e:
#    #    print(e)
tax = 630959996850000 * 2
for i in range(1, 11):
    key = "0x" + str(i).zfill(64)
    acc = eth_account.Account.from_key(key)
    print(acc.address)
    blc = web3.eth.get_balance(acc.address)
    print(blc, i)

    try:
        if blc - tax > 0:
            #print(blc - web3.eth.gas_price * 30000)
            print(blc - tax)

#            send_transaction1(myaddr, blc - tax, key)
    except Exception as e:
        print(e)
