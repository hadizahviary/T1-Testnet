import sys, asyncio, random
from web3 import Web3
from eth_account import Account
from colorama import init, Fore

from src.utils.utils import load_addresseserc20
from src.utils.pvkey import load_private_keys
from src.utils.logging import *
from src.utils.web3 import connect_web3
from src.constant.constant import SEND_TOKEN_ABI
from config.config import settings

init(autoreset=True)

def connect_web3():
    for url in settings['RPC_URL_T1']:
        try:
            w3 = Web3(Web3.HTTPProvider(url))
            if w3.is_connected():
                print(f"Success: Connected to T1 Testnet | Chain ID: {w3.eth.chain_id} | RPC: {url}")
                return w3
            else:
                print(f"Failed to connect to RPC at {url}")
        except Exception as e:
            print(f"Web3 connection failed at {url}: {str(e)}")

    print(f"Failed to connect to any default RPC endpoint")
    print(f"{'Please obtain an RPC from https://alchemy.com and enter it below'}")
    custom_rpc = input(f"> {'Enter custom RPC'}: ").strip()

    if not custom_rpc:
        print(f"{'No RPC provided, exiting program'}")
        sys.exit(1)
    try:
        w3 = Web3(Web3.HTTPProvider(custom_rpc))
        if w3.is_connected():
            print(f"Success: Connected to T1 Testnet | Chain ID: {w3.eth.chain_id} | RPC: {custom_rpc}")
            return w3
        else:
            print(f"Failed to connect to RPC at {custom_rpc}")
            sys.exit(1)
    except Exception as e:
        print(f"Connection failed at {custom_rpc}: {str(e)}")
        sys.exit(1)

async def send_token(w3: Web3, private_key: str, wallet_index: int, contract_address: str, destination: str, amount: float, ):
    account = Account.from_key(private_key)
    sender_address = account.address

    try:
        contract = w3.eth.contract(address=Web3.to_checksum_address(contract_address), abi=SEND_TOKEN_ABI)
        decimals = contract.functions.decimals().call()
        amount_wei = int(amount * 10 ** decimals)

        balance = w3.from_wei(w3.eth.get_balance(sender_address), 'ether')
        print(f"- Số dư hiện tại: {balance:.6f} ETH")

        print(f"> Preparing transaction...")
        nonce = w3.eth.get_transaction_count(sender_address)
        gas_price = w3.eth.gas_price
        gas_price = int(gas_price * 1.2)

        try:
            estimated_gas = contract.functions.sendToken(Web3.to_checksum_address(destination), amount_wei).estimate_gas({
                'from': sender_address
            })
            gas_limit = int(estimated_gas * 1.2)
            print(f"Gas ước lượng: {estimated_gas} | Gas limit sử dụng: {gas_limit}")
        except Exception as e:
            print(f"Không thể ước lượng gas: {str(e)}. Dùng gas mặc định: 200000")
            gas_limit = 200000

        required_balance = w3.from_wei(gas_limit * gas_price, 'ether')
        if balance < required_balance:
            print(f"Insufficient balance for gas (Need: {required_balance:.6f} ETH)")
            return False

        tx = contract.functions.sendToken(Web3.to_checksum_address(destination), amount_wei).build_transaction({
            'from': sender_address,
            'nonce': nonce,
            'chainId': int(settings['CHAIN_ID_T1']),
            'gas': gas_limit,
            'gasPrice': gas_price
        })

        print(f"Sending transaction, please wait...")
        signed_tx = w3.eth.account.sign_transaction(tx, private_key)
        tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_link = f"{settings['EXPLORER_URL_T1']}/tx/0x{tx_hash.hex()}"

        receipt = await asyncio.get_event_loop().run_in_executor(None, lambda: w3.eth.wait_for_transaction_receipt(tx_hash, timeout=180))
        print(f"address: {sender_address}")
        print(f"destination: {destination}")
        print(f"amount: {amount:.4f} Token")
        print(f"gas: {receipt['gasUsed']}")
        print(f"block: {receipt['blockNumber']}")
        if receipt.status == 1:
            print(f"Token sent successfully!")
            print(f"Tx: {tx_link}")
            return True
        else:
            print(f"Token sending failed │ Tx: {tx_link}")
            return False
    except Exception as e:
        print(f"{'Thất bại / Failed'}: {str(e)}")
        return False

async def run_sendtoken():
    private_keys = load_private_keys('private_key.txt')
    print(f"Info: found {len(private_keys)} wallets")
    w3 = connect_web3()

    print(f"Enter ERC20 contract address (contractERC20.txt): ", end="")
    contract_address = input().strip()
    print(f"Enter token amount to send: ", end="")
    amount_input = input().strip()

    try:
        amount = float(amount_input)
        if amount <= 0:
            raise ValueError
    except ValueError:
        print(f"Error: Please enter a valid number")
        return
    
    print(f"Choose token sending method:")
    print(f"├─ 1. Send randomly")
    print(f"└─ 2. Send from addressERC20.txt")

    print(f"Enter your choice (1 or 2): ", end="")
    choice = input().strip()

    destinations = []
    if choice == '1':
        for _ in range(len(private_keys)):
            new_account = w3.eth.account.create()
            destinations.append(new_account.address)
    elif choice == '2':
        destinations = load_addresseserc20('addressERC20.txt')
        if not destinations:
            return
    else:
        print(f"Invalid choice")
        return

    successful_sends = 0
    total_wallets = len(private_keys)

    for i, (profile_num, private_key) in enumerate(private_keys, 1):
    
        print(f"Processing wallet {profile_num} ({i}/{len(private_keys)})", Fore.MAGENTA)
    
        destination = destinations[i-1] if i-1 < len(destinations) else random.choice(destinations)
        if await send_token(w3, private_key, profile_num, contract_address, destination, amount):
            successful_sends += 1
        
        if i < len(private_keys):
            delay = random.uniform(10, 30)
            print(f"Pausing {delay:.2f} seconds")
            await asyncio.sleep(delay)
    log_debug(f"Completing {profile_num} / {total_wallets}")

if __name__ == "__main__":
    asyncio.run(run_sendtoken) 