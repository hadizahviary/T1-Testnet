from solcx import compile_source, install_solc, get_solc_version
from src.utils import load_json
from src.constant.contract_nft import CONTRACT

CONFIG = load_json("config/nft_config.json")
SOLC_VERSION = CONFIG['SOLC_VERSION']
NFT_CONTRACT_SOURCE = CONTRACT

def solc_check():
    try:
        current_version = get_solc_version()
        if current_version != SOLC_VERSION:
            raise Exception("Phiên bản solc không khớp")
    except Exception:
        print(f"  ℹ Installing solc version {SOLC_VERSION}")
        install_solc(SOLC_VERSION)
        print(f"Installed solc version {SOLC_VERSION}")

def compile_contract():
    solc_check()
    compiled_sol = compile_source(NFT_CONTRACT_SOURCE, output_values=['abi', 'bin'], solc_version=SOLC_VERSION)
    contract_id, contract_interface = compiled_sol.popitem()
    return contract_interface['abi'], contract_interface['bin']

