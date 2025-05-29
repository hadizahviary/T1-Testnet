import asyncio
from colorama import init
from src.utils.logging import log_warning, log_error, log_debug, countdown_timer
from src.helpers.banner import s0x000
from src.utils.utils import _clear
from config.config import settings

init(autoreset=True)

async def run_deposit():
    from src.scripts.deposit import run_deposit as deposit_run
    await deposit_run()

async def run_withdraw():
    from src.scripts.withdraw import run_withdraw as withdraw_run
    await withdraw_run()

async def run_sendtx():
    from src.scripts.sendtx import run_sendtx as sendtx_run
    await sendtx_run()

async def run_deploytoken():
    log_warning("This feature is under maintenance until v.030 complete!")

async def run_sendtoken():
    log_warning("This feature is under maintenance until v.030 complete!")

async def run_nftcollection():
    from src.scripts.nftcollection import run as nftcollection_run
    await nftcollection_run()

def run_script(script_func, name):
    print("-" * 90)
    try:
        log_warning(f"Running: {name}")
        if asyncio.iscoroutinefunction(script_func):
            asyncio.run(script_func())
        else:
            script_func()
        log_debug(f"Finished: {name}")
        print("-" * 90)
    except Exception as e:
        log_error(f"An error occurred while running {name}: {str(e)}")
        print("-" * 90)

def main():
    _clear()
    s0x000()
    while True:
        try:

            if settings["AUTO_DEPOSIT"]:
                run_script(run_deposit, "AUTO_DEPOSIT")
            if settings["AUTO_WITHDRAW"]:
                run_script(run_withdraw, "AUTO_WITHDRAW")
            if settings["AUTO_SEND"]:
                run_script(run_sendtx, "AUTO_SEND")
            if settings["AUTO_DEPLOYTOKEN"]:
                run_script(run_deploytoken, "AUTO_DEPLOYTOKEN")
            if settings["AUTO_SENDTOKEN"]:
                run_script(run_sendtoken, "AUTO_SENDTOKEN")
            if settings["AUTO_NFTCOLLECTION"]:
                run_script(run_nftcollection, "AUTO_NFTCOLLECTION")

            countdown_timer(settings['COUNTDOWN_FOR_LOOP'][0], settings['COUNTDOWN_FOR_LOOP'][1])

        except Exception as e:
            log_error(f"An error occured on the main loop {e}")
            
if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        exit(0)
