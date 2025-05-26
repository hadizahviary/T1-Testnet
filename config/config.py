import os
import json
from dotenv import load_dotenv
from src.utils.utils import _is_array, _as_percent_array

load_dotenv()

settings = {
    "TIME_SLEEP": int(os.getenv("TIME_SLEEP", 8)),
    "MAX_THREADS": int(os.getenv("MAX_THREADS", 10)),

    "AUTO_SHOW_COUNT_DOWN_TIME_SLEEP": os.getenv("AUTO_SHOW_COUNT_DOWN_TIME_SLEEP", "false").lower() == "true",
    "ENABLE_DEBUG": os.getenv("ENABLE_DEBUG", "false").lower() == "true",

    "AUTO_SEND": os.getenv("AUTO_SEND", "false").lower() == "true",
    "IS_RANDOM_SEND": os.getenv("IS_RANDOM_SEND", "false").lower() == "true",
    "AUTO_DEPOSIT": os.getenv("AUTO_DEPOSIT", "false").lower() == "true",
    "AUTO_WITHDRAW": os.getenv("AUTO_WITHDRAW", "false").lower() == "true",
    "AUTO_DEPLOYTOKEN": os.getenv("AUTO_DEPLOYTOKEN", "false").lower() == "true",
    "AUTO_NFTCOLLECTION": os.getenv("AUTO_NFTCOLLECTION", "false").lower() == "true",
    "AUTO_SENDTOKEN": os.getenv("AUTO_SENDTOKEN", "false").lower() == "true",

    "RPC_URL_T1": os.getenv("RPC_URL_T1", "https://rpc.v03.t1protocol.com"),
    "RPC_URL_SEPOLIA": os.getenv("RPC_URL_SEPOLIA", "https://ethereum-sepolia-rpc.publicnode.com"),    
    "CHAIN_ID_T1": os.getenv("CHAIN_ID_T1", 299992),
    "CHAIN_ID_SEPOLIA": os.getenv("CHAIN_ID_SEPOLIA", 11155111),
    "EXPLORER_SEPOLIA": os.getenv("EXPLORER_SEPOLIA", "https://sepolia.etherscan.io/tx/"),
    "EXPLORER_T1": os.getenv("EXPLORER_T1", "https://explorer.v03.t1protocol.com/tx/0x"),

    'DELAY_BETWEEN_REQUESTS': json.loads(os.getenv('DELAY_BETWEEN_REQUESTS')) if _is_array(os.getenv('DELAY_BETWEEN_REQUESTS')) else [4, 10],
    'DELAY_START_BOT': json.loads(os.getenv('DELAY_START_BOT')) if _is_array(os.getenv('DELAY_START_BOT')) else [1, 15],
    'DELAY_BETWEEN_ACCOUNT': json.loads(os.getenv('DELAY_BETWEEN_ACCOUNT')) if _is_array(os.getenv('DELAY_BETWEEN_ACCOUNT')) else [10, 30],

    'AMOUNT_TO_DEPOSIT': json.loads(os.getenv('AMOUNT_DEPOSIT')) if _is_array(os.getenv('AMOUNT_DEPOSIT')) else [0.0001, 0.001],
    'AMOUNT_TO_WITHDRAW': json.loads(os.getenv('AMOUNT_WITHDRAW')) if _is_array(os.getenv('AMOUNT_WITHDRAW')) else [0.0001, 0.0003],
    'AMOUNT_TO_SEND': json.loads(os.getenv('AMOUNT_SEND')) if _is_array(os.getenv('AMOUNT_SEND')) else [0.0001, 0.0003],    

    "NUMBER_DEPOSIT": int(os.getenv("NUMBER_LIQUIDITY", 1)),
    "NUMBER_WITHDRAW": int(os.getenv("NUMBER_WITHDRAW", 1)),
    "NUMBER_SEND": int(os.getenv("NUMBER_SEND", 1)),

    "ROUTER_T1": os.getenv("ROUTER_T1", None),
    "ROUTER_SEPOLIA": os.getenv("ROUTER_SEPOLIA", None),
    'COUNTDOWN_FOR_LOOP': json.loads(os.getenv('COUNTDOWN_FOR_LOOP')) if _is_array(os.getenv('AMOUNT_SEND')) else [12, 30],    
    "SOLC_VERSION": os.getenv("SOLC_VERSION", "0.8.19"),
}
