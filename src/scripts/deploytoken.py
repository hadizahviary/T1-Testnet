import os
import sys
import asyncio
import random
from web3 import Web3
from web3.exceptions import ContractLogicError
from eth_account import Account
from solcx import compile_source, install_solc, get_solc_version
from colorama import init, Fore

from src.utils.pvkey import load_private_keys
from src.constant.contract_nft import CONTRACT_SOURCE
from src.utils.web3 import connect_web3
from config.config import settings

init(autoreset=True)

NETWORK_URLS = settings['RPC_URL_T1']
CHAIN_ID = settings['CHAIN_ID_T1']
EXPLORER_URL = settings['EXPLORER_URL_T1']
SOLC_VERSION = settings['SOLC_VERSION']  

def ensure_solc_installed():
    try:
        current_version = get_solc_version()
        if current_version != SOLC_VERSION:
            raise Exception("solc version mismatch")
    except Exception:
        print(Fore.YELLOW + f"Installing solc version {SOLC_VERSION}... ")
        install_solc(SOLC_VERSION)
        print(Fore.GREEN + f"Installed solc version {SOLC_VERSION}...")

def compile_contract():
    ensure_solc_installed()
    compiled_sol = compile_source(CONTRACT_SOURCE, output_values=['abi', 'bin'], solc_version=SOLC_VERSION)
    contract_id, contract_interface = compiled_sol.popitem()
    return contract_interface['abi'], contract_interface['bin']

async def deploy_contract(w3: Web3, private_key: str, wallet_index: int, name: str, symbol: str, decimals: int, total_supply: int):
    account = Account.from_key(private_key)
    sender_address = account.address

    try:
        abi, bytecode = compile_contract()
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

        balance = w3.from_wei(w3.eth.get_balance(sender_address), 'ether')
        print(Fore.YELLOW + f"Current Balance: {balance:.6f} ETH")

        print(Fore.CYAN + f"Preparing transaction please wait...")
        nonce = w3.eth.get_transaction_count(sender_address)
        total_supply_wei = w3.to_wei(total_supply, 'ether')

        print(Fore.CYAN + f"Estimating gas please wait...")
        try:
            estimated_gas = contract.constructor(name, symbol, decimals, total_supply_wei).estimate_gas({
                'from': sender_address
            })
            gas_limit = int(estimated_gas * 1.2)  
            print(Fore.YELLOW + f"Estimated gas: {estimated_gas} | Gas limit used: {gas_limit}")
        except ContractLogicError as e:
            print(Fore.RED + f"Gas estimate error: {str(e)} (Contract may be invalid)")
            return None
        except Exception as e:
            print(Fore.YELLOW + f"Unable to estimate gas: {str(e)}. Using default gas: 4000000")
            gas_limit = 4000000  

        gas_price = w3.eth.gas_price
        gas_price = int(gas_price * 1.2)
        required_balance = w3.from_wei(gas_limit * gas_price, 'ether')
        if balance < required_balance:
            print(Fore.RED + f"No balance available, required {required_balance}")
            return None

        tx = contract.constructor(name, symbol, decimals, total_supply_wei).build_transaction({
            'from': sender_address,
            'nonce': nonce,
            'chainId': CHAIN_ID,
            'gas': gas_limit,
            'gasPrice': gas_price
        })

        print(Fore.CYAN + f"Sending transaction please wait...")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_link = f"{EXPLORER_URL}/tx/0x{tx_hash.hex()}"

        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300))

        if receipt.status == 1:
            contract_address = receipt['contractAddress']
            print(Fore.GREEN + f"Deploy token successful!")
            print(Fore.YELLOW + f"Tx: {tx_link}")
            print(Fore.YELLOW + f"Contract address: {contract_address}")
            print(Fore.YELLOW + f"Gas: {receipt['gasUsed']}")
            print(Fore.YELLOW + f"Block: {receipt['blockNumber']}")
            return contract_address
        else:
            print(Fore.RED + f"Deployment failed | Tx: {tx_link}")
            return None
    except Exception as e:
        print(Fore.RED + f"Failed: {str(e)}")
        print(Fore.YELLOW + f"Tx: {tx_link if 'tx_hash' in locals() else 'Not sent yet'}")
        return None

async def run_deploytoken():
    print(f"Deploy token")
    private_keys = load_private_keys('pvkey.txt')
    print(Fore.YELLOW + f"Info: Found {len(private_keys)} wallets")

    if not private_keys:
        return

    w3 = connect_web3()

    name = input(Fore.YELLOW + f"Enter token name (e.g., NONIME Token): ").strip()
    symbol = input(Fore.YELLOW + f"Enter token symbol (default NME): ").strip()
    decimals_input = input(Fore.YELLOW + f"Enter decimals (default 18): ").strip() or "18"
    total_supply_input = input(Fore.YELLOW + f"Enter total supply (e.g., 1000000): ").strip()

    try:
        decimals = int(decimals_input)
        total_supply = int(total_supply_input)
        if decimals <= 0 or total_supply <= 0:
            raise ValueError
    except ValueError:
        print(Fore.RED + f"error : Please enter a valid number")
        return

    successful_deploys = 0
    total_wallets = len(private_keys)

    random.shuffle(private_keys)

    for i, (profile_num, private_key) in enumerate(private_keys, 1):
        print(f"PROCESSING WALLET {profile_num} ({i}/{total_wallets})", Fore.MAGENTA)

        contract_address = await deploy_contract(w3, private_key, profile_num, name, symbol, decimals, total_supply)
        if contract_address:
            successful_deploys += 1
            with open('contractERC20.txt', 'a') as f:
                f.write(f"{contract_address}\n")
        
        if i < total_wallets:
            delay = random.uniform(10, 30)
            print(Fore.YELLOW + f"Pausing {delay:.2f} seconds")
            await asyncio.sleep(delay)

    print(f"Complete {successful_deploys} / {total_wallets}")

if __name__ == "__main__":
    asyncio.run(run_deploytoken)
