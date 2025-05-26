# T1-Testnet-bot# T1 Testnet Scripts

This repository contains a collection of Python scripts designed to interact with the **T1 Testnet**, a blockchain test network for cross-chain bridging. These scripts allow users to bridge ETH between the Sepolia Testnet and T1 Testnet, facilitating deposits (Sepolia → T1) and withdrawals (T1 → Sepolia) using the T1 bridge router contracts. Each script is built with the `web3.py` library and offers bilingual support (English and Vietnamese) for user interaction.

Faucet: [Sepolia Faucet](https://sepoliafaucet.com/)  
Bridge: [T1 Devnet Bridge](https://devnet.t1protocol.com/bridge)

## General Features

- **Multi-Account Support**: Reads private keys from `private_key.txt` to perform bridging actions across multiple accounts.
- **Colorful CLI**: Uses `colorama` for visually appealing output with colored text, borders, and separators.
- **Asynchronous Execution**: Built with `asyncio` for efficient blockchain interactions.
- **Error Handling**: Comprehensive error catching for blockchain transactions, balance checks, and RPC issues.
- **Bilingual Support**: Supports both English and Vietnamese output based on user selection.

### Included Scripts

1. **deposit.py**: Bridge ETH from Sepolia Testnet to T1 Devnet using the T1 bridge router contract.
2. **withdraw.py**: Bridge ETH from T1 Devnet back to Sepolia Testnet using the T1 bridge router contract.
3. **sendtx.py**: Send random ETH transactions or to addresses from address.txt on T1 Testnet.
4. **deploytoken.py**: Deploy an ERC20 token smart contract on T1 Testnet.
5. **sendtoken.py**: Send ERC20 tokens to random addresses or from addressERC20.txt on T1 Testnet.
6. **nftcollection.py**: Deploy and manage an NFT smart contract (Create, Mint, Burn) on T1 Testnet.

## Prerequisites

Before running the scripts, ensure you have the following installed:

- Python 3.8+
- `pip` (Python package manager)
- **Dependencies**: Install via `pip install -r requirements.txt` (ensure `web3.py`, `colorama`, `asyncio`, `eth-account`).
- **pvkey.txt**: Add private keys (one per line) for wallet automation.
- Access to the Sepolia Testnet RPC (e.g., `https://ethereum-sepolia-rpc.publicnode.com`).
- Access to the T1 Devnet RPC (`https://rpc.v006.t1protocol.com`).

## Installation

1. **Clone this repository:**
- Open cmd or Shell, then run the command:
```sh
git clone https://github.com/FckTestnet/T1-Testnet-bot.git
```
```sh
cd T1-Testnet-bot
```
2. **Install Dependencies:**
- Open cmd or Shell, then run the command:
```sh
pip install -r requirements.txt
```
3. **Prepare Input Files:**
- Open the `private_key.txt`: Add your private keys (one per line) in the root directory.
```sh
nano private_key.txt 
```
4. **Change env file**
Rename `Example.env` to `.env`: mandatory to replace this file

- Open the `address.txt`(optional): Add recipient addresses (one per line) for `sendtx.py`, `deploytoken.py`, `sendtoken.py`,`nftcollection.py`.
```sh
nano address.txt 
```
```sh
nano addressERC20.txt
```
```sh
nano contractERC20.txt
```
```sh
nano contractNFT.txt
```
4. **Run:**
- Open cmd or Shell, then run command:
```sh
python main.py
```


