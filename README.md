# T1-Testnet-bot

This repo hosts Python scripts for seamless interaction with the T1 Testnet—a cross-chain bridge testnet. Effortlessly bridge ETH between Sepolia and T1, handling deposits and withdrawals via T1 bridge router contracts.

Faucet: [Sepolia Faucet](https://sepoliafaucet.com/)  
Bridge: [T1 Devnet Bridge](https://devnet.t1protocol.com/bridge)

## General Features

- `Multi-Account Ready`: Loads private keys from private_key.txt to bridge across many wallets effortlessly.

- `Testnet Feature`: Bridge , Withdraw, Send ETH T1, Send token on T1, Deploy Token & NFT.

- `Vibrant CLI`: Powered by colorama for colorful, clear terminal output with stylish borders and highlights.

- `Async-Powered`: Utilizes asyncio for fast, concurrent blockchain calls and smooth user experience.

- `Robust Error Handling`: Catches and reports errors in transactions, balance queries, and RPC connectivity gracefully.

## Prerequisites
Make sure you have:

1. Python 3.8 or newer

2. pip (Python package manager)

Required packages installed via:

```bash
pip install -r requirements.txt
```
(includes web3.py, colorama, asyncio, eth-account)

- A `private_key.txt` file with your wallet private keys (one key per line)

- RPC endpoints:

1. Sepolia Testnet (e.g., https://ethereum-sepolia-rpc.publicnode.com)

2. T1 Devnet (https://rpc.v006.t1protocol.com)

## Installation
Clone the repo

```bash
git clone https://github.com/FckTestnet/T1-Testnet-bot.git
cd T1-Testnet-bot
```
## Install dependencies

```bash
pip install -r requirements.txt
```
- Prepare your keys and addresses

- Add private keys to private_key.txt (one per line)

```bash
nano private_key.txt
```
- Rename Example.env to .env and configure it as needed

- (Optional) Add recipient addresses for sending scripts:

```bash
nano address.txt
nano addressERC20.txt
nano contractERC20.txt
nano contractNFT.txt
```
- Run the main script

```bash
python main.py
```

## Included Scripts

- `deposit.py` – Bridge ETH from Sepolia Testnet to T1 Devnet via the T1 bridge router.

- `withdraw.py` – Bridge ETH from T1 Devnet back to Sepolia Testnet through the T1 bridge router.

- `sendtx.py` – Send ETH on T1 Testnet either randomly or to addresses listed in address.txt.

- `deploytoken.py` – Deploy ERC20 token contracts on T1 Testnet.

- `sendtoken.py` – Transfer ERC20 tokens to random addresses or those in addressERC20.txt on T1 Testnet.

- `nftcollection.py` – Deploy and manage NFTs on T1 Testnet (Create, Mint, Burn).

## Feedback & Support
Have suggestions, questions, or issues?
Feel free to open an Issue or submit a Pull Request.
Your contributions are welcome!

## Disclaimer
This project is for educational and testing purposes only.
Use at your own risk. Always keep your private keys secure and never share them.

## License
This repository is licensed under the `MIT License`.

Made with ❤️ by the `FckTestnet community`.