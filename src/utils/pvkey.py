import sys, os
from colorama import Fore, init

init(autoreset=True)

def is_valid_private_key(key: str) -> bool:
    key = key.strip()
    if not key.startswith('0x'):
        key = '0x' + key
    try:
        bytes.fromhex(key.replace('0x', ''))
        return len(key) == 66
    except ValueError:
        return False

def load_private_keys(file_path: str = "pivate_key.txt") -> list:
    try:
        if not os.path.exists(file_path):
            print(f"{Fore.RED}  ✖ pvkey.txt file not found")
            with open(file_path, 'w') as f:
                f.write("# Add private keys here, one per line\n# Example: 0x1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef\n")
            sys.exit(1)
        
        valid_keys = []
        with open(file_path, 'r') as f:
            for i, line in enumerate(f, 1):
                key = line.strip()
                if key and not key.startswith('#'):
                    if is_valid_private_key(key):
                        if not key.startswith('0x'):
                            key = '0x' + key
                        valid_keys.append((i, key))
                    else:
                        print(f"{Fore.YELLOW}  ⚠ Warning: Line {i} is invalid, skipped: {key}")
        
        if not valid_keys:
            print(f"{Fore.RED}  ✖ No valid private keys found")
            sys.exit(1)
        
        return valid_keys
    except Exception as e:
        print(f"{Fore.RED}  ✖ Failed to read pvkey.txt: {str(e)}")
        sys.exit(1)