import os, json, sys, asyncio
from web3  import Web3
from colorama import *

init(autoreset=True)

def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def _is_array(obj):
    try:
        return isinstance(obj, list) and len(obj) > 0 or isinstance(json.loads(obj), list)
    except Exception:
        return False
    
def _as_percent_array(value: str | None, default: list[float]) -> list[float]:
    if _is_array(value):
        try:
            parsed = json.loads(value)
            return [float(v) / 100 for v in parsed]
        except Exception:
            return default
    return default

def load_json(file_path: str):
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Failed to load {file_path}: {str(e)}")
        sys.exit(1)

def load_addresseserc20(file_path: str = "data/addressERC20.txt", ) -> list:
    try:
        if not os.path.exists(file_path):
            print(f"No addresses found in addressERC20.txt. Create new file.")
            with open(file_path, 'w') as f:
                f.write("# Add token receiving addresses here, one per line\n# Example: 0x1234567890abcdef1234567890abcdef1234567890\n")
            return []
        
        addresses = []
        with open(file_path, 'r') as f:
            for line in f:
                addr = line.strip()
                if addr and not addr.startswith('#') and Web3.is_address(addr):
                    addresses.append(Web3.to_checksum_address(addr))
        
        if not addresses:
            print(f"No addresses found in addressERC20.txt")
        return addresses
    except Exception as e:
        print(f"Error: {str(e)}")
        return []

def load_addresses(file_path: str = "./data/address.txt", ) -> list:
    try:
        if not os.path.exists(file_path):
            print(f"No addresses found in addressERC20.txt. Create new file.")
            with open(file_path, 'w') as f:
                f.write("# Add the receiving addresses here, one per line\n# Example: 0x1234567890abcdef1234567890abcdef1234567890\n")
            return None
        
        addresses = []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                addr = line.strip()
                if addr and not addr.startswith('#'):
                    if Web3.is_address(addr):
                        addresses.append(Web3.to_checksum_address(addr))
                    else:
                        print(f"Warning line {i}: Invalid address - {addr}")
        
        if not addresses:
            print(f"No addresses found in address.txt")
            return None
        
        return addresses
    except Exception as e:
        print(f"Error: {str(e)}")
        return None
    


