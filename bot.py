import os
import sys
import asyncio
import random
import aiohttp
import inquirer
from aiohttp_socks import ProxyConnector
from colorama import init, Fore, Style
from datetime import datetime, timedelta

# Initialize colorama
init(autoreset=True)

BORDER_WIDTH = 80
API_BASE_URL = "https://be.nexira.ai/api/web-game-air-drop-token"
IP_CHECK_URL = "https://api.ipify.org?format=json"

# --- STEALTH FINGERPRINTING ---
def get_random_user_agent():
    os_versions = ["Windows NT 10.0; Win64; x64", "Macintosh; Intel Mac OS X 10_15_7", "X11; Linux x86_64"]
    chrome_versions = [f"131.0.0.{random.randint(0, 99)}", f"130.0.6723.{random.randint(0, 99)}"]
    return f"Mozilla/5.0 ({random.choice(os_versions)}) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/{random.choice(chrome_versions)} Safari/537.36"

def get_base_headers():
    return {
        "User-Agent": get_random_user_agent(),
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Origin": "https://www.nexira.ai",
        "Referer": "https://www.nexira.ai/",
        "Sec-Ch-Ua-Mobile": "?0",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "same-site",
    }

# --- UI COMPONENTS ---
def _clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_border(text: str, color=Fore.CYAN):
    padded_text = f" {text} ".center(BORDER_WIDTH - 2)
    print(f"{color}┌{'─' * (BORDER_WIDTH - 2)}┐")
    print(f"{color}│{padded_text}│")
    print(f"{color}└{'─' * (BORDER_WIDTH - 2)}┘{Style.RESET_ALL}")

def _banner():
    banner = r"""
███╗░░██╗███████╗░░░░░░██╗██████╗░██╗░█████╗░██████╗░
████╗░██║██╔════╝░░░░░░██║██╔══██╗██║██╔══██╗╚════██╗
██╔██╗██║█████╗░░░░░░░░██║██████╔╝██║██║░░██║░░███╔═╝
██║╚████║██╔══╝░░░██╗░░██║██╔══██╗██║██║░░██║██╔══╝░░
██║░╚███║███████╗░╚█████╔╝██║░░██║██║╚█████╔╝███████╗
╚═╝░░╚══╝╚══════╝░░╚════╝░╚═╝░░╚═╝╚═╝░╚════╝░╚══════╝
    """
    print(f"{Fore.CYAN}{banner}")
    print(f"{Fore.CYAN}{'═' * BORDER_WIDTH}")
    print_border("AUTOPILOT MODE: SS1 & SS2 - BY MEJRI02", Fore.GREEN)

# --- CORE UTILITIES ---
async def get_proxy_ip(proxy: str = None) -> str:
    try:
        connector = ProxyConnector.from_url(proxy) if proxy else None
        async with aiohttp.ClientSession(connector=connector, timeout=aiohttp.ClientTimeout(total=10)) as session:
            async with session.get(IP_CHECK_URL) as resp:
                data = await resp.json()
                return data.get('ip', 'Unknown')
    except: return 'Connection Error'

async def process_wallet(token: str, idx: int, proxy: str):
    headers = get_base_headers()
    headers["authorization"] = f"Bearer {token}"
    ip = await get_proxy_ip(proxy)
    
    print(f"{Fore.WHITE}[Acc {idx}] IP: {Fore.YELLOW}{ip}")

    for season in [1, 2]:
        try:
            connector = ProxyConnector.from_url(proxy) if proxy else None
            async with aiohttp.ClientSession(connector=connector) as session:
                async with session.post(f"{API_BASE_URL}/daily-checkin", json={"season": season}, headers=headers) as resp:
                    if resp.status == 201:
                        print(f"  {Fore.GREEN}Season {season}: Check-in Successful!")
                    elif resp.status == 500:
                        print(f"  {Fore.YELLOW}Season {season}: Already done/Limit reached.")
                    else:
                        print(f"  {Fore.RED}Season {season}: Failed (HTTP {resp.status})")
                
                await asyncio.sleep(random.uniform(2, 4))
        except Exception as e:
            print(f"  {Fore.RED}Season {season}: Error {str(e)[:30]}")

# --- MAIN RUNNER ---
async def start_bot(use_proxies: bool):
    while True:
        _clear()
        _banner()
        
        if not os.path.exists("token.txt"):
            print(f"{Fore.RED}Error: token.txt not found!")
            return

        with open("token.txt", "r") as f:
            tokens = [line.strip() for line in f if line.strip()]
        
        proxies = []
        if use_proxies:
            if os.path.exists("proxies.txt"):
                with open("proxies.txt", "r") as f:
                    proxies = [line.strip() for line in f if line.strip()]
            if not proxies:
                print(f"{Fore.RED}Warning: proxies.txt is empty! Running without proxies.")
                use_proxies = False

        print(f"{Fore.CYAN}Processing {len(tokens)} wallets for Season 1 & 2...")
        print(f"{Fore.MAGENTA}{'═' * BORDER_WIDTH}")

        indexed_tokens = list(enumerate(tokens, 1))
        random.shuffle(indexed_tokens)

        for i, token in indexed_tokens:
            proxy = proxies[i % len(proxies)] if use_proxies else None
            await process_wallet(token, i, proxy)
            wait = random.uniform(10, 20)
            print(f"{Fore.BLACK}{Style.BRIGHT}Cooldown: Waiting {wait:.1f}s...")
            await asyncio.sleep(wait)

        # Timer logic
        now = datetime.now()
        next_run = (now + timedelta(days=1)).replace(hour=0, minute=5, second=0)
        sleep_seconds = (next_run - now).total_seconds()
        
        print(f"\n{Fore.CYAN}{'═' * BORDER_WIDTH}")
        print(f"{Fore.GREEN}ALL ACCOUNTS FINISHED FOR TODAY.")
        print(f"{Fore.WHITE}Next run scheduled for: {next_run.strftime('%H:%M:%S')} Tomorrow")
        
        while sleep_seconds > 0:
            timer = str(timedelta(seconds=int(sleep_seconds)))
            print(f"\r{Fore.YELLOW}Sleeping... Time remaining until next cycle: {timer} ", end="")
            await asyncio.sleep(1)
            sleep_seconds -= 1

def main():
    _clear()
    _banner()
    
    # Prompt for Proxy usage at startup
    questions = [
        inquirer.List('use_proxy',
                      message=f"{Fore.CYAN}Do you want to use proxies?{Style.RESET_ALL}",
                      choices=[('Yes (Load from proxies.txt)', True), ('No (Local IP)', False)],
                      )
    ]
    answers = inquirer.prompt(questions)
    
    if answers:
        asyncio.run(start_bot(answers['use_proxy']))

if __name__ == "__main__":
    main()
