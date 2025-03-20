import json

from solcx import compile_files, install_solc
from web3 import Web3
from web3.middleware import geth_poa_middleware
from Crypto.Hash import keccak

myaddr = "0x01e456edFD092cC4CfF396834511e11EDB8AcC01"
private_key = ""


def get_abi(solname):
    print(install_solc(version="latest"))
    result_ = compile_files(
        [solname], output_values=["abi", "bin-runtime"], solc_version="0.8.26"
    )
    with open("abi.json", "wt", encoding="ascii") as f:
        json.dump(result_, f)


def create_transaction(func, private_key=private_key, addr=myaddr):
    tr = {
        "from": addr,
        "nonce": web3.eth.get_transaction_count(addr),
    }
    transaction = func.build_transaction(tr)

    # Sign the transaction
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key=private_key)

    # Send the transaction
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)

    # Wait for the transaction to be mined
    txn_receipt = web3.eth.wait_for_transaction_receipt(txn_hash)

    print(f"Transaction successful with hash: {txn_hash.hex()}")

def send_transaction(to, amount):
    transaction = {
            "to": to,
            "value": amount,
            "nonce": web3.eth.get_transaction_count(myaddr),
            "gasPrice": web3.to_wei(50, 'gwei'),
            "gas": 21000,
            "chainId": 80002
    }
    signed_txn = web3.eth.account.sign_transaction(transaction, private_key)
    txn_hash = web3.eth.send_raw_transaction(signed_txn.rawTransaction)
    print(f'Transaction sent with hash: {txn_hash.hex()}')


def gen_hash(msg: bytes):
    tosign = b"\x19Ethereum Signed Message:\n32" + msg

    hsh = keccak.new(data=tosign, digest_bytes=16).digest()
    return hsh


def sign_(msg):
    p = 2**256 - 2**32 - 2**9 - 2**8 - 2**7 - 2**6 - 2**4 - 1
    a = 0
    b = 7


testnet_rpc = "https://rpc-amoy.polygon.technology/"
web3 = Web3(Web3.HTTPProvider(testnet_rpc))
web3.middleware_onion.inject(geth_poa_middleware, layer=0)
