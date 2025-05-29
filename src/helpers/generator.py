import random
from eth_account import Account as _A

def g0x993(min_value, max_value, decimals=2):
    return round(random.uniform(min_value, max_value), decimals)

def g0x994(min_value, max_value, decimals=2):
    return round(random.randint(min_value, max_value), decimals)
