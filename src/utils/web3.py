from web3 import Web3
import sys
from src.utils.logging import *

def connect_web3(rpc_url: str):
    try:
        w3 = Web3(Web3.HTTPProvider(rpc_url))
        if not w3.is_connected():
            log_warning(f"Failed to connect to RPC")
            sys.exit(1)
        log_success(f"Connected to RPC with Chain ID: {w3.eth.chain_id}")
        return w3
    except Exception as e:
        log_error(f"Web3 connection failed: {str(e)}")
        sys.exit(1)

def get_random_address(w3: Web3):
    random_account = w3.eth.account.create()
    return random_account.address

def check_balance(w3: Web3, address: str) -> float:
    try:
        balance = w3.eth.get_balance(address)
        return float(w3.from_wei(balance, 'ether'))
    except Exception as e:
        log_error(f"Error {str(e)}")
        return -1

def display_balances(w3_sepolia: Web3, w3_t1: Web3, address: str):
    sepolia_balance = check_balance(w3_sepolia, address)
    t1_balance = check_balance(w3_t1, address)
    log_info(f"Balance ETH: {sepolia_balance:.6f} Sepolia - {t1_balance:.6f} T1")