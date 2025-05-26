import time
from colorama import Fore, Style
from datetime import datetime

def get_timestamp():
    return datetime.now().strftime('%Y-%m-%d %H:%M:%S')

def format_log(level, color, message, style=Style.NORMAL):
    timestamp = get_timestamp()
    padded_level = f"{level:<7}"
    return f"{Fore.LIGHTBLACK_EX}{timestamp} {color}| {style}{padded_level} |{Style.RESET_ALL} {message}"

def log_info(message):
    print(format_log("INFO", Fore.CYAN, message))

def log_success(message):
    print(format_log("SUCCESS", Fore.GREEN, message))

def log_warning(message):
    print(format_log("WARNING", Fore.YELLOW, message))

def log_error(message):
    print(format_log("ERROR", Fore.RED, message))

def log_debug(message):
    print(format_log("DEBUG", Fore.MAGENTA, message))

def log_critical(message):
    print(format_log("CRITICAL", Fore.RED, message, style=Style.BRIGHT))

def log_trace(message):
    print(format_log("TRACE", Fore.CYAN, message, style=Style.DIM))

def log_fatal(message):
    print(format_log("FATAL", Fore.BLACK, message, style=Style.BRIGHT))

def log_ask(message):
    print(format_log("ASK", Fore.BLUE, message))

def log_update(message):
    print(format_log("UPDATE", Fore.YELLOW, message))

def countdown_timer(seconds, message=None):
    while seconds:
        m, s = divmod(seconds, 60)
        h, m = divmod(m, 60)
        h = str(h).zfill(2)
        m = str(m).zfill(2)
        s = str(s).zfill(2)
        print(f"please wait until {h}:{m}:{s} {message if message else ''}", flush=True, end="\r")
        seconds -= 1
        time.sleep(1)
    print(f"please wait until {h}:{m}:{s} {message if message else ''}", flush=True, end="\r")

def logger(self, message, log_type="info"):
    address = self.item_data['address']
    masked_address = f"{address[:6]}...{address[-6:]}"

    colors = [
        "\033[91m", "\033[92m", "\033[93m", "\033[94m", "\033[95m",
        "\033[96m", "\033[90m", "\033[97m", "\033[35m", "\033[36m"
    ]
    reset = "\033[0m"
    color = colors[self.account_index % len(colors)]

    account_index_str = f"{self.account_index + 1}".rjust(2)
    address_str = masked_address.ljust(13) 

    prefix = Fore.LIGHTBLACK_EX + f"[{get_timestamp}][{address_str}]{reset}"
    log_message = f"{prefix}{color}[{account_index_str}]{reset} {message}"
    print(log_message)
