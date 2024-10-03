import PIL
import requests
import json
import time
import random
from setproctitle import setproctitle
from colorama import Fore, Style, init
from datetime import datetime, timedelta
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import urllib.parse
import os

url = "https://notpx.app/api/v1"
WAIT = 180 * 3
DELAY = 1
WIDTH = 1000
HEIGHT = 1000
MAX_HEIGHT = 50
start_x = 920
start_y = 386

init(autoreset=True)
setproctitle("notpixel")

def get(path):
    space = ' '
    hash_sym = '#'
    dot = '.'
    star = '*'

    return [
        [space] * 15 + [hash_sym] * 10 + [space] * 15,
        [space] * 14 + [hash_sym] * 16 + [space] * 13,
        [space] * 12 + [hash_sym] * 14 + [dot] * 8 + [hash_sym] * 12 + [space] * 8,
        [space] * 10 + [hash_sym] * 10 + [dot] * 12 + [dot] * 9 + [hash_sym] * 10 + [space] * 7,
        [space] * 8  + [hash_sym] * 8  + [dot] * 18 + [hash_sym] * 8  + [space] * 8,
        [space] * 7  + [hash_sym] * 7  + [dot] * 7  + [star] * 17 + [dot] * 7  + [hash_sym] * 8  + [space] * 6,
        [space] * 6  + [hash_sym] * 6  + [dot] * 7  + [star] * 19 + [dot] * 7  + [hash_sym] * 8  + [space] * 6,
        [space] * 5  + [hash_sym] * 5  + [dot] * 8  + [star] * 3  + [dot] * 6  + [star] * 3  + [dot] * 8  + [hash_sym] * 9  + [space] * 6,
        [space] * 5  + [hash_sym] * 5  + [dot] * 8  + [star] * 3  + [dot] * 6  + [star] * 2  + [dot] * 9  + [hash_sym] * 8  + [space] * 7,
        [space] * 5  + [hash_sym] * 5  + [dot] * 9  + [star] * 3  + [dot] * 7  + [star] * 1  + [dot] * 10 + [hash_sym] * 8  + [space] * 7,
        [space] * 5  + [hash_sym] * 5  + [dot] * 9  + [star] * 3  + [dot] * 5  + [star] * 1  + [dot] * 11 + [hash_sym] * 8  + [space] * 7,
        [space] * 5  + [hash_sym] * 5  + [dot] * 11 + [star] * 1  + [dot] * 11 + [hash_sym] * 8  + [space] * 7,
        [space] * 6  + [hash_sym] * 4  + [dot] * 8  + [star] * 6  + [dot] * 7  + [hash_sym] * 10 + [space] * 7,
        [space] * 7  + [hash_sym] * 4  + [dot] * 10 + [star] * 5  + [dot] * 7  + [hash_sym] * 8  + [space] * 7,
        [space] * 9  + [hash_sym] * 4  + [dot] * 12 + [hash_sym] * 6  + [space] * 8,
        [space] * 10 + [hash_sym] * 6  + [dot] * 14 + [hash_sym] * 6  + [space] * 10,
        [space] * 12 + [hash_sym] * 4  + [dot] * 6  + [dot] * 8  + [hash_sym] * 12 + [space] * 12,
        [space] * 13 + [hash_sym] * 6  + [dot] * 8  + [hash_sym] * 10 + [space] * 15,
        [space] * 19
    ]

image = get("")

c = {
    '#': "#000000",
    '.': "#3690EA",
    '*': "#ffffff"
}

def log_message(message, color=Style.RESET_ALL):
    current_time = datetime.now().strftime("[%H:%M:%S]")
    print(f"{Fore.LIGHTBLACK_EX}{current_time}{Style.RESET_ALL} {color}{message}{Style.RESET_ALL}")

def load_proxy_from_file(filename='proxy.txt'):
    if not os.path.exists(filename):
        log_message(random.choice([
            "We couldn't even keep a simple promise like loading a proxy...",
            "It was supposed to work, but just like us, it’s broken.",
            "The proxy file is gone... like all the plans we had together.",
            "I searched for it, but the proxy file just doesn’t exist, like the connection we used to have.",
            "You wanted to use the proxy, but it’s just another thing that’s gone now.",
            "The proxy is missing... much like how things used to be between us.",
            "Couldn't find the proxy file... maybe it's a sign that some things are meant to stay lost.",
            "Another missing piece, another reminder of what we’ve lost.",
            "The file is missing. Just like the moments we’ll never get back.",
            "Nothing works anymore... not even the proxy."
        ]), Fore.RED)
        return None
    
    with open(filename, 'r') as file:
        proxy = file.readline().strip()
        return proxy

proxy = load_proxy_from_file()

def get_session_with_proxy_and_retries(proxy, retries=3, backoff_factor=0.3, status_forcelist=(500, 502, 504)):
    session = requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    if proxy:
        session.proxies = {'http': proxy, 'https': proxy}
        log_message(random.choice([
            "We're still using the same proxy... but does it even matter anymore?",
            "Proxy’s there, just like old habits we can’t seem to let go of.",
            "Using the proxy, like clinging to something that’s already broken.",
            "The proxy’s here, but does it really help fix anything?",
            "We’re still using a proxy... but we both know it’s not enough."
        ]), Fore.CYAN)
    
    return session

session = get_session_with_proxy_and_retries(proxy)

def get_color(pixel, header):
    try:
        response = session.get(f"{url}/image/get/{str(pixel)}", headers=header, timeout=10)
        if response.status_code == 401:
            return -1
        return response.json()['pixel']['color']
    except KeyError:
        return "#000000"
    except requests.exceptions.Timeout:
        log_message(random.choice([
            "It’s taking too long... just like us, running out of time.",
            "The request timed out... just like our patience with each other.",
            "Another timeout... sometimes things just don’t work out.",
            "I waited, but it seems like this too has run out of time.",
            "Timeout. I guess we’ll never really get there, will we?"
        ]), Fore.RED)
        return "#000000"
    except requests.exceptions.ConnectionError as e:
        log_message(random.choice([
            "Connection error... much like the one we used to share.",
            "It’s broken. The connection, the proxy, us.",
            "Lost the connection... and here we are again, broken.",
            "The connection failed... I wonder if it’s a sign.",
            "Another lost connection. Seems like that’s all we’re good at now."
        ]) + f" {e}", Fore.RED)
        return "#000000"
    except requests.exceptions.RequestException as e:
        log_message(random.choice([
            "Something went wrong, again. Just like it always does.",
            "Another error... it's all we seem to have left.",
            "It failed... just like everything we tried to fix.",
            "Another failure... seems like that's all we’re good at.",
            "It’s broken again... like the pieces of us we couldn’t keep together."
        ]) + f" {e}", Fore.RED)
        return "#000000"

def claim(header):
    log_message(random.choice([
        "It’s done... you’ve claimed it. But why do I still feel like we’re drifting apart?",
        "I guess this is yours now... but what did we lose along the way?",
        "You’ve claimed it, but all I can think about is what we’ve given up.",
        "Success. But why does it feel like another step away from each other?",
        "It’s yours now... but is it really enough?"
    ]), Fore.CYAN)
    try:
        session.get(f"{url}/mining/claim", headers=header, timeout=10)
    except requests.exceptions.RequestException as e:
        log_message(random.choice([
            "You couldn’t claim it... just like we couldn’t hold onto us.",
            "Failed again... it seems like we can’t get anything right.",
            "I tried, but it just didn’t work... maybe some things aren’t meant to be.",
            "You wanted to claim it, but it slipped away... just like everything else.",
            "I couldn’t make it work. And now, it’s gone."
        ]) + f" {e}", Fore.RED)

def get_pixel(x, y):
    return y * 1000 + x + 1

def get_pos(pixel, size_x):
    return pixel % size_x, pixel // size_x

def get_canvas_pos(x, y):
    return get_pixel(start_x + x - 1, start_y + y - 1)

def paint(canvas_pos, color, header):
    data = {"pixelId": canvas_pos, "newColor": color}
    try:
        response = session.post(f"{url}/repaint/start", data=json.dumps(data), headers=header, timeout=10)
        x, y = get_pos(canvas_pos, 1000)

        if response.status_code == 400:
            log_message(random.choice([
                "You’re out of energy, just like how we ran out of time for each other.",
                "No energy left... just like no more words left between us.",
                "It’s over... out of energy, out of chances.",
                "No energy to keep going. Maybe this is the end.",
                "Out of energy... like the last bit of us finally slipping away."
            ]), Fore.RED)
            return False
        if response.status_code == 401:
            return -1

        log_message(random.choice([
            f"I painted {x},{y}, but does it even matter anymore?",
            f"Another pixel placed... but it doesn’t feel the same.",
            f"It’s done... {x},{y}. But I’m left with this hollow feeling.",
            f"Another piece added... but why do I still feel empty?",
            f"It’s painted, {x},{y}, but what did we lose along the way?"
        ]), Fore.GREEN)
        return True
    except requests.exceptions.RequestException as e:
        log_message(random.choice([
            "Failed to paint... just like we failed to keep everything together.",
            "It didn’t work, again. I guess some things are just meant to stay broken.",
            "Another failure... seems like that’s all we do now.",
            "We couldn’t paint it... just like we couldn’t make this work.",
            "It didn’t go through... maybe it was never meant to."
        ]) + f" {e}", Fore.RED)
        return False

def extract_username_from_initdata(init_data):
    decoded_data = urllib.parse.unquote(init_data)
    username_start = decoded_data.find('"username":"') + len('"username":"')
    username_end = decoded_data.find('"', username_start)
    
    if username_start != -1 and username_end != -1:
        return decoded_data[username_start:username_end]
    
    return "Unknown"

def load_accounts_from_file(filename):
    with open(filename, 'r') as file:
        accounts = [f"initData {line.strip()}" for line in file if line.strip()]
    return accounts

def fetch_mining_data(header):
    try:
        response = session.get(f"https://notpx.app/api/v1/mining/status", headers=header, timeout=10)
        if response.status_code == 200:
            data = response.json()
            user_balance = data.get('userBalance', 'Unknown')
            log_message(random.choice([
                f"You’ve got a balance of {user_balance}, but why does it still feel like we’re not enough?",
                f"Your balance is {user_balance}, but what have we really gained?",
                f"Balance: {user_balance}. Yet all I feel is this emptiness inside.",
                f"You have {user_balance}, but why does it feel like we’re still losing?",
                f"Your balance is {user_balance}, but what did we give up along the way?"
            ]), Fore.MAGENTA)
        else:
            log_message(random.choice([
                "We couldn’t even get your mining data... maybe some things are better left unknown.",
                "Failed to fetch the data... just like we couldn’t fix us.",
                "I tried, but the mining data is out of reach... just like everything else now.",
                "Mining data isn’t available... it’s like the future we never had.",
                "It didn’t work... just like everything else we tried."
            ]), Fore.RED)
    except requests.exceptions.RequestException as e:
        log_message(random.choice([
            "We couldn’t get it... the mining data, the future, us.",
            "Error fetching data... seems like everything’s a struggle now.",
            "Another failure to connect... we keep trying but nothing changes.",
            "We couldn’t fetch the mining data... maybe it’s not worth it anymore.",
            "It’s all broken, including the mining data we can’t even get."
        ]) + f" {e}", Fore.RED)

def main(auth, account):
    headers = {'authorization': auth}
    try:
        fetch_mining_data(headers)
        claim(headers)

        size = len(image) * len(image[0])
        order = [i for i in range(size)]
        random.shuffle(order)

        for pos_image in order:
            x, y = get_pos(pos_image, len(image[0]))
            time.sleep(0.05 + random.uniform(0.01, 0.1))
            try:
                color = get_color(get_canvas_pos(x, y), headers)
                if color == -1:
                    log_message(random.choice([
                        "I guess it’s over... the authorization failed.",
                        "Authorization’s dead... just like what we had.",
                        "I thought we could keep going, but it seems like this is the end.",
                        "Authorization failed... I should have known it wouldn’t last.",
                        "We’ve reached the end... the authorization is no longer valid."
                    ]), Fore.RED)
                    print(headers["authorization"])
                    break
                if image[y][x] == ' ' or color == c[image[y][x]]:
                    log_message(random.choice([
                        f"I skipped {start_x + x - 1},{start_y + y - 1}. It doesn’t even feel like skipping anymore.",
                        f"Another skip... {start_x + x - 1},{start_y + y - 1}. But we’re not skipping the pain, are we?",
                        f"Skipping {start_x + x - 1},{start_y + y - 1}, but the memories remain.",
                        f"Another one skipped... {start_x + x - 1},{start_y + y - 1}. But can we skip the hurt?",
                        f"It’s skipped {start_x + x - 1},{start_y + y - 1}. But what about the rest of us?"
                    ]), Fore.RED)
                    continue

                result = paint(get_canvas_pos(x, y), c[image[y][x]], headers)
                if result == -1:
                    log_message(random.choice([
                        "Authorization failed... we can’t go on like this.",
                        "Authorization’s broken... I guess it’s over.",
                        "We tried, but the authorization just isn’t there anymore.",
                        "Failed to keep going... authorization is gone, like us.",
                        "Authorization failure... it feels like a final goodbye."
                    ]), Fore.RED)
                    print(headers["authorization"])
                    break
                elif result:
                    continue
                else:
                    break

            except IndexError:
                log_message(random.choice([
                    "Something went wrong... I guess we weren’t careful enough.",
                    "IndexError... just another thing we couldn’t handle.",
                    "We missed something... maybe we’re always missing things now.",
                    "Another error... it seems like that’s all we’re left with.",
                    "IndexError... maybe it was inevitable."
                ]), Fore.RED)
    except requests.exceptions.RequestException as e:
        log_message(random.choice([
            f"Network error... even the connection in account {account} couldn’t last.",
            f"We tried, but the network failed for {account}. Maybe we’re just cursed.",
            f"Network issues with {account}... another connection lost.",
            f"Failed to connect for {account}... seems like that’s all we do now.",
            f"The network couldn’t hold for {account}. It’s just another broken thing."
        ]) + f" {e}", Fore.RED)

def process_accounts(accounts):
    first_account_start_time = datetime.now()
    for account in accounts:
        username = extract_username_from_initdata(account)
        log_message(random.choice([
            f"Starting again for {username}... but we both know how this ends.",
            f"We’re back, {username}, but it doesn’t feel the same anymore.",
            f"It’s {username}’s turn... but is this really what we want?",
            f"Another round for {username}, but it feels like we’re just going through the motions.",
            f"It’s {username} again... but why do I feel like we’re further apart than ever?"
        ]), Fore.BLUE)
        main(account, account)

    time_elapsed = datetime.now() - first_account_start_time
    time_to_wait = timedelta(hours=1) - time_elapsed

    if time_to_wait.total_seconds() > 0:
        log_message(random.choice([
            f"Waiting {int(time_to_wait.total_seconds() //60)} minutes... it feels like I’ve been waiting forever.",
            f"SLEEPING for {int(time_to_wait.total_seconds() // 60)} minutes. But some things can’t be fixed by waiting.",
            f"It’s time to wait... {int(time_to_wait.total_seconds() // 60)} minutes, like waiting for something that’ll never come.",
            f"{int(time_to_wait.total_seconds() // 60)} minutes of waiting... but does waiting ever really help?",
            f"Another wait, {int(time_to_wait.total_seconds() // 60)} minutes... but no amount of time can fix what’s broken."
        ]), Fore.YELLOW)
        time.sleep(time_to_wait.total_seconds())
    else:
        log_message(random.choice([
            "No need to wait... but it feels like we’ve already waited too long.",
            "It’s over an hour... no sleep needed, but what have we lost along the way?",
            "No sleep needed, but it still feels like we’re out of time.",
            "The time’s up, and we don’t need to wait. But why do I still feel so tired?",
            "No waiting needed... but that doesn’t mean everything’s okay now."
        ]), Fore.YELLOW)

if __name__ == "__main__":
    accounts = load_accounts_from_file('data.txt')
    while True:
        process_accounts(accounts)
