import asyncio
from web3 import Web3
from eth_account import Account
from colorama import init, Fore

from src.utils.logging import *
from src.utils.web3 import connect_web3
from src.utils.pvkey import load_private_keys
from src.utils.utils import load_json
from src.solc import compile_contract

init(autoreset=True)
CONFIG = load_json("config/nft_config.json")

NETWORK_URLS = CONFIG["RPC_URL_T1"]
CHAIN_ID = CONFIG["CHAIN_ID_T1"]
EXPLORER_URL = CONFIG["EXPLORER_T1"]

async def deploy_nft(w3: Web3, private_key: str, wallet_index: int, name: str, symbol: str, max_supply: int, ):
    account = Account.from_key(private_key)
    sender_address = account.address

    try:
        abi, bytecode = compile_contract()
        contract = w3.eth.contract(abi=abi, bytecode=bytecode)

        print(f"Preparing transaction...")
        nonce = w3.eth.get_transaction_count(sender_address)

        print(f"Estimating gas...")
        gas_price = int(w3.eth.gas_price * 1.2)
        print(f"  - Current gas price: {w3.from_wei(gas_price, 'gwei'):.2f} Gwei")

        tx = contract.constructor(name, symbol, max_supply).build_transaction({
            'from': sender_address,
            'nonce': nonce,
            'chainId': CHAIN_ID,
            'gasPrice': gas_price
        })

        try:
            estimated_gas = contract.constructor(name, symbol, max_supply).estimate_gas({'from': sender_address})
            gas_limit = int(estimated_gas * 1.2)
            tx['gas'] = gas_limit
            print(f"  - Gas ước lượng: {estimated_gas} | Gas limit sử dụng: {gas_limit}")
        except Exception as e:
            tx['gas'] = 4000000
            print(f"  ⚠ Không thể ước lượng gas: {str(e)}. Dùng gas mặc định: 4000000")

        balance = w3.from_wei(w3.eth.get_balance(sender_address), 'ether')
        required_balance = w3.from_wei(tx['gas'] * tx['gasPrice'], 'ether')
        if balance < required_balance:
            print(f"Insufficient balance (need at least {required_balance} ETH")
            return None

        print(f"Sending transaction...")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_link = f"{EXPLORER_URL}/tx/0x{tx_hash.hex()}"

        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=300))

        if receipt.status == 1:
            contract_address = receipt['contractAddress']
            print(f"NFT collection created successfully! | Tx: {tx_link}")
            print(f"Contract address: {contract_address}")
            print(f"Gas: {receipt['gasUsed']}")
            print(f"block: {receipt['blockNumber']}")
            return {'address': contract_address, 'abi': abi}
        else:
            print(f"Failed | Tx: {tx_link}")
            return None
    except Exception as e:
        print(f"Failed: {str(e)}")
        return None

async def mint_nft(w3: Web3, private_key: str, wallet_index: int, contract_address: str, token_id: int, token_uri: str, ):
    account = Account.from_key(private_key)
    sender_address = account.address

    try:
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=compile_contract()[0])

        print(f"Preparing transaction...")
        nonce = w3.eth.get_transaction_count(sender_address)

        gas_price = int(w3.eth.gas_price * 1.2)
        print(f"Current gas price: {w3.from_wei(gas_price, 'gwei'):.2f} Gwei")

        tx = contract.functions.mint(sender_address, token_id, token_uri).build_transaction({
            'from': sender_address,
            'nonce': nonce,
            'chainId': CHAIN_ID,
            'gasPrice': gas_price
        })

        print(f"Estimating gas...")
        try:
            estimated_gas = contract.functions.mint(sender_address, token_id, token_uri).estimate_gas({'from': sender_address})
            gas_limit = int(estimated_gas * 1.2)
            tx['gas'] = gas_limit
            print(f"Gas ước lượng: {estimated_gas} | Gas limit sử dụng: {gas_limit}")
        except Exception as e:
            tx['gas'] = 200000
            print(f"Không thể ước lượng gas: {str(e)}. Dùng gas mặc định: 200000")

        balance = w3.from_wei(w3.eth.get_balance(sender_address), 'ether')
        required_balance = w3.from_wei(tx['gas'] * tx['gasPrice'], 'ether')
        if balance < required_balance:
            print(f"Insufficient balance (need at least {required_balance} ETH")
            return False

        print(f"Sending transaction...")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_link = f"{EXPLORER_URL}/tx/0x{tx_hash.hex()}"

        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180))

        if receipt.status == 1:
            print(f"NFT minted successfully! | Tx: {tx_link}")
            print(f"Token ID: {token_id}")
            print(f"Gas: {receipt['gasUsed']}")
            print(f"block: {receipt['blockNumber']}")
            return True
        else:
            print(f"Failed | Tx: {tx_link}")
            return False
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False

async def burn_nft(w3: Web3, private_key: str, wallet_index: int, contract_address: str, token_id: int):
    account = Account.from_key(private_key)
    sender_address = account.address

    try:
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=compile_contract()[0])

        print(f"Preparing transaction...")
        nonce = w3.eth.get_transaction_count(sender_address)

        gas_price = int(w3.eth.gas_price * 1.2)
        print(f"Current gas price: {w3.from_wei(gas_price, 'gwei'):.2f} Gwei")

        tx = contract.functions.burn(token_id).build_transaction({
            'from': sender_address,
            'nonce': nonce,
            'chainId': CHAIN_ID,
            'gasPrice': gas_price
        })

        print(f"Estimating gas...")
        try:
            estimated_gas = contract.functions.burn(token_id).estimate_gas({'from': sender_address})
            gas_limit = int(estimated_gas * 1.2)
            tx['gas'] = gas_limit
            print(f"Gas ước lượng: {estimated_gas} | Gas limit sử dụng: {gas_limit}")
        except Exception as e:
            tx['gas'] = 200000
            print(f"Không thể ước lượng gas: {str(e)}. Dùng gas mặc định: 200000")

        balance = w3.from_wei(w3.eth.get_balance(sender_address), 'ether')
        required_balance = w3.from_wei(tx['gas'] * tx['gasPrice'], 'ether')
        if balance < required_balance:
            print(f"Insufficient balance (need at least {required_balance} ETH")
            return False

        print(f"Sending transaction...")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_link = f"{EXPLORER_URL}/tx/0x{tx_hash.hex()}"

        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180))

        if receipt.status == 1:
            print(f"NFT burned successfully! | Tx: {tx_link}")
            print(f"Token ID: {token_id}")
            print(f"Gas: {receipt['gasUsed']}")
            print(f"Block: {receipt['blockNumber']}")
            return True
        else:
            print(f"Failed | Tx: {tx_link}")
            return False
    except Exception as e:
        print(f"Failed: {str(e)}")
        return False

async def run():
    
    print(f"NFT MANAGEMENT - T1 DEVNET")
    private_keys = load_private_keys('private_key.txt', )
    print(f"found {len(private_keys)} wallet")
    
    if not private_keys:
        return

    w3 = connect_web3(NETWORK_URLS)
    
    print(f"Select option")
    print(f"1. Create NFT Collection (Deploy)")
    print(f"2. Mint NFT")
    print(f"3. Burn NFT")
    choice = input(f"Enter choice (1, 2, or 3):").strip()

    successful_ops = 0
    total_ops = len(private_keys)

    if choice == '1': 
        name = input(f"Enter NFT collection name (e.g., Thog NFT): ").strip()
        symbol = input(f"Enter collection symbol (e.g., THOG): ").strip() or "ETH"
        max_supply_input = input(f"Enter maximum supply (e.g., 999): ").strip()
        try:
            max_supply = int(max_supply_input)
            if max_supply <= 0:
                raise ValueError
        except ValueError:
            print(f"error: Please enter a valid number")
            return

        for i, (profile_num, private_key) in enumerate(private_keys, 1):
            print(f"Processing wallet {profile_num} ({i}/{total_ops})", Fore.MAGENTA)
            result = await deploy_nft(w3, private_key, profile_num, name, symbol, max_supply, )
            if result:
                successful_ops += 1
                with open('contractNFT.txt', 'a') as f:
                    f.write(f"{result['address']}\n")
            if i < total_ops:
                await asyncio.sleep(10)  
            
    elif choice == '2': 
        contract_address = input(f"Enter NFT contract address: ").strip()
        token_id_input = input(f"Enter Token ID: ").strip()
        token_uri = input(f"Enter Token URI (e.g., ipfs://...): ").strip()
        try:
            token_id = int(token_id_input)
            if token_id < 0:
                raise ValueError
        except ValueError:
            print(f"error: Please enter a valid number")
            return

        for i, (profile_num, private_key) in enumerate(private_keys, 1):
            print(f"Processing wallet {profile_num} ({i}/{total_ops})", Fore.MAGENTA)
            if await mint_nft(w3, private_key, profile_num, contract_address, token_id, token_uri, ):
                successful_ops += 1
            if i < total_ops:
                await asyncio.sleep(10)  
            
    elif choice == '3': 
        contract_address = input(f"Enter NFT contract address: ").strip()
        token_id_input = input(f"Enter Token ID: ").strip()
        try:
            token_id = int(token_id_input)
            if token_id < 0:
                raise ValueError
        except ValueError:
            print(f"error: Please enter a valid number")
            return

        for i, (profile_num, private_key) in enumerate(private_keys, 1):
            print(f"Processing wallet {profile_num} ({i}/{total_ops})", Fore.MAGENTA)
            if await burn_nft(w3, private_key, profile_num, contract_address, token_id, ):
                successful_ops += 1
            if i < total_ops:
                await asyncio.sleep(10)
            
    else:
        print(f"Invalid choice")
        return
    
    print(f"COMPLETED: {successful_ops}/{total_ops} transaction successfull", Fore.GREEN)
    
if __name__ == "__main__":
    asyncio.run(run())
