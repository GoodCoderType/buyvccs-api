import requests
import json
from colorama import Fore, Style, init
from datetime import datetime
import pytz

init(autoreset=True)

print(Fore.LIGHTBLUE_EX + Style.BRIGHT + "/buyvccs | Auto Vcc Purchaser")
print(Fore.LIGHTGREEN_EX + Style.BRIGHT + "- Developer - @goodgamerhere | discord.gg/buyvccs")
with open("config.json") as f:
    config = json.load(f)
userid = config['discord_id']
token = config['token']

def convert_unix_to_local(unix_timestamp):
    local_time = datetime.fromtimestamp(unix_timestamp, pytz.timezone('UTC')).astimezone()
    return local_time.strftime('%Y-%m-%d %H:%M:%S %Z%z')

def buy_vccs():
    amount = input("Enter the number of VCCs to purchase: ")
    response = requests.post(f"http://162.243.165.237:6969/purchase/{amount}/{userid}/{token}")
    if 'vccs' in response.json():
        data = response.json()
        formated_vccs = "\n".join(data['vccs'])
        print(Fore.LIGHTGREEN_EX + f"Purchased VCCs: \n{formated_vccs}")
        with open("vccs.txt",'a') as f:
            f.write("\n".join(data['vccs']))
            f.write("\n")
    else:
        print(Fore.LIGHTRED_EX + response.text)

def check_stock():
    response = requests.get("http://162.243.165.237:6969/stock")
    if response.status_code == 200:
        data = response.json()
        expiry = convert_unix_to_local(int(data['expiry']))
        print(Fore.LIGHTGREEN_EX + f"Stock: {data['stock']}, Expiry: {expiry}")
    else:
        print(Fore.LIGHTRED_EX + "Failed to fetch stock data.")

def check_expiry():
    response = requests.get("http://162.243.165.237:6969/next_stock")
    if response.status_code == 200:
        data = response.json()
        expiry = convert_unix_to_local(int(data['next_stock']))
        print(Fore.LIGHTGREEN_EX + f"Next Stock Expiry: {expiry}")
    else:
        print(Fore.LIGHTRED_EX + "Failed to fetch expiry data.")

def check_credits():
    response = requests.get(f"http://162.243.165.237:6969/credits/{userid}")
    if response.status_code == 200:
        data = response.json()
        print(Fore.LIGHTGREEN_EX + f"Credits: {data['credits']}, Purchase Count: {data['purchased']}, Used Credits: {data['used_credits']}")
    else:
        print(Fore.LIGHTRED_EX + "Failed to fetch credit data.")

while True:
    module = input(f"""
------------------------------------
{Fore.LIGHTYELLOW_EX} (1) - Buy Vccs
{Fore.LIGHTCYAN_EX} (2) - Check Current Stock
{Fore.LIGHTBLUE_EX} (3) - Check Vcc Expiry
{Fore.LIGHTYELLOW_EX} (4) - Check your credits
------------------------------------
{Fore.LIGHTWHITE_EX} Select Module: """)

    if module == "1":
        buy_vccs()
    elif module == "2":
        check_stock()
    elif module == "3":
        check_expiry()
    elif module == "4":
        check_credits()
    else:
        print(Fore.LIGHTRED_EX + "Invalid option. Please try again.")