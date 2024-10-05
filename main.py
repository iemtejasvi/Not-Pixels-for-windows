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
            "It’s gone... like everything we built together, the proxy file isn’t here anymore.",
            "We searched, but the proxy file is gone... just like the future we once talked about.",
            "Even the proxy’s missing... it’s just another thing we couldn’t hold onto.",
            "I wanted to find it, I really did, but the proxy’s just not there... like how we drifted apart.",
            "The proxy file... missing, lost, just like everything we tried to save."
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
            "We’re still using the proxy, hoping it’ll make a difference, but deep down, we know it won’t fix what’s broken.",
            "Still using the same proxy, like holding onto memories we should have let go of a long time ago.",
            "We use the proxy, thinking it'll help, but the truth is, some things just can’t be patched up.",
            "The proxy’s here... but does it really change anything between us anymore?",
            "The proxy’s active, like trying to pretend everything’s okay, but we both know it’s not."
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
            "It took too long... just like us, we waited too long, and now it’s over.",
            "The request timed out... I guess everything does in the end, doesn’t it?",
            "It couldn’t wait any longer, just like how we couldn’t wait for each other.",
            "I tried, but it timed out, and now there’s nothing left for us here.",
            "We waited too long, and now the time’s up, like all the moments we missed."
        ]), Fore.RED)
        return "#000000"
    except requests.exceptions.ConnectionError as e:
        log_message(random.choice([
            "We lost the connection... but it feels like we’ve lost more than that.",
            "Another broken connection... it’s becoming a pattern with us.",
            "The connection’s gone, just like how we lost our way.",
            "The connection failed... it reminds me of everything else that’s failed between us.",
            "We lost the connection... and now, all that’s left is the emptiness."
        ]), Fore.RED)
        return "#000000"
    except requests.exceptions.RequestException as e:
        log_message(random.choice([
            "It didn’t work... nothing’s working anymore, is it?",
            "Another failure... it seems like all we do is break things now.",
            "It failed... just like every time we tried to fix things.",
            "Something went wrong again... like everything we tried to save.",
            "It didn’t go through... just like how we never could get through to each other."
        ]), Fore.RED)
        return "#000000"

def claim(header):
    log_message(random.choice([
        "You claimed it... but why does it feel like I’ve lost something in the process?",
        "It’s done... but claiming this doesn’t bring back what we lost, does it?",
        "I handed it to you... the claim, but it feels like we’ve traded something more valuable away.",
        "You got what you wanted... but why do I feel like we’re further apart than ever?",
        "It’s all yours now... but somehow, it feels like a hollow victory."
    ]), Fore.CYAN)
    try:
        session.get(f"{url}/mining/claim", headers=header, timeout=10)
    except requests.exceptions.RequestException as e:
        log_message(random.choice([
            "You couldn’t claim it... much like how we couldn’t claim a future together.",
            "It slipped through... just like we slipped away from each other.",
            "Failed to claim... it’s like watching everything we had fall apart.",
            "The claim failed... just like everything else we tried to hold onto.",
            "I tried, but it didn’t work... maybe it was never meant to."
        ]), Fore.RED)

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
                "You’re out of energy... like how we ran out of reasons to keep going.",
                "There’s no more energy left... just like we’ve run out of hope for us.",
                "It’s empty... there’s nothing left, just like the space between us.",
                "Out of energy... just like how we ran out of ways to make it work.",
                "There’s no more left... it’s over, and we’re out of everything."
            ]), Fore.RED)
            return False
        if response.status_code == 401:
            return -1

        log_message(random.choice([
            f"Another pixel added at {x},{y}, but it still feels like something’s missing.",
            f"I painted {x},{y}, but it’s hard to feel good about it now.",
            f"It’s done... {x},{y}, but nothing feels right anymore.",
            f"I placed it at {x},{y}, but the emptiness is still there.",
            f"It’s finished at {x},{y}, but does it even matter?"
        ]), Fore.GREEN)
        return True
    except requests.exceptions.RequestException as e:
        log_message(random.choice([
            "It didn’t work... we couldn’t even finish this one thing.",
            "Another failure... just like us, falling apart with every try.",
            "It didn’t go through... I guess some things aren’t meant to be fixed.",
            "We couldn’t paint it... just like we couldn’t save what we had.",
            "It failed... like every last effort we tried to make."
        ]), Fore.RED)
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
                f"Your balance is {user_balance}, but why does it feel like we’re still losing?",
                f"You’ve got {user_balance}, but what’s the point if we’re still drifting apart?",
                f"{user_balance} is your balance, but no amount will ever fix what we lost.",
                f"Balance: {user_balance}, but no number will make this emptiness go away.",
                f"Your balance is {user_balance}, but all I feel is that we’re still not whole."
            ]), Fore.MAGENTA)
        else:
            log_message(random.choice([
                "We couldn’t get your mining data... just like we couldn’t fix what was broken.",
                "The data didn’t come... like all the promises we left behind.",
                "It failed to load... and it feels like another piece of us fading away.",
                "Mining data wasn’t retrieved... maybe some things are better left unknown.",
                "It didn’t work... just like us, it failed to show what we needed."
            ]), Fore.RED)
    except requests.exceptions.RequestException as e:
        log_message(random.choice([
            "We couldn’t get the data... it’s like everything’s falling apart now.",
            "Another error fetching data... another sign that we’re too broken to continue.",
            "We couldn’t retrieve it... like we couldn’t retrieve the parts of us we lost.",
            "The mining data is out of reach... just like everything we hoped for.",
            "It didn’t work, again... like trying to patch up something that’s too far gone."
        ]), Fore.RED)

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
                        "The authorization failed... like everything we tried to hold onto.",
                        "It’s over... the authorization’s gone, like us.",
                        "Authorization failed... I guess some things weren’t meant to last.",
                        "The end... authorization is gone, just like what we had.",
                        "It didn’t work... the authorization died, and so did everything else."
                    ]), Fore.RED)
                    print(headers["authorization"])
                    break
                if image[y][x] == ' ' or color == c[image[y][x]]:
                    log_message(random.choice([
                        f"I skipped {start_x + x - 1},{start_y + y - 1}, but it feels like I’m skipping more than just pixels.",
                        f"Skipped {start_x + x - 1},{start_y + y - 1}, but it doesn’t feel like progress anymore.",
                        f"It’s skipped... {start_x + x - 1},{start_y + y - 1}, but nothing feels right now.",
                        f"Another skip... {start_x + x - 1},{start_y + y - 1}. But we’re skipping more than just pixels, aren’t we?",
                        f"Skipped again... {start_x + x - 1},{start_y + y - 1}. It feels like I’m skipping past pieces of us."
                    ]), Fore.RED)
                    continue

                result = paint(get_canvas_pos(x, y), c[image[y][x]], headers)
                if result == -1:
                    log_message(random.choice([
                        "It’s dead... the authorization is gone, like everything we tried to save.",
                        "The authorization failed... just like everything else we couldn’t hold onto.",
                        "We tried, but the authorization is no longer valid, just like us.",
                        "It’s broken now... the authorization’s gone, and so is everything we had.",
                        "Authorization is over... and so is everything else."
                    ]), Fore.RED)
                    print(headers["authorization"])
                    break
                elif result:
                    continue
                else:
                    break

            except IndexError:
                log_message(random.choice([
                    "We missed something... and now it’s too late to fix it.",
                    "Another error... it’s becoming too much to handle.",
                    "I lost track... and now it’s all fallen apart.",
                    "IndexError... it’s just another crack in the already broken picture.",
                    "Something went wrong... and now it feels like everything is slipping away."
                ]), Fore.RED)
    except requests.exceptions.RequestException as e:
        log_message(random.choice([
            f"We couldn’t connect for {account}... it’s like nothing’s working anymore.",
            f"Network issues for {account}... even the smallest things seem to be falling apart now.",
            f"We couldn’t connect... just like how we couldn’t connect anymore.",
            f"The network failed... and so did everything else, it seems.",
            f"We lost the connection for {account}... just another thing that’s breaking down."
        ]), Fore.RED)

def process_accounts(accounts):
    first_account_start_time = datetime.now()
    for account in accounts:
        username = extract_username_from_initdata(account)
        log_message(random.choice([
            f"We’re starting again for {username}, but it feels like it’s just another step toward the end.",
            f"{username}’s up next... but I wonder if it’s even worth it anymore.",
            f"Here we go again with {username}, but why does it feel like nothing’s going to change?",
            f"{username} is up, but all I feel is this growing emptiness.",
            f"It’s {username} again, but I can’t shake this feeling that we’re just delaying the inevitable."
        ]), Fore.BLUE)
        main(account, account)

    time_elapsed = datetime.now() - first_account_start_time
    time_to_wait = timedelta(minutes=30) - time_elapsed

    if time_to_wait.total_seconds() > 0:
        log_message(random.choice([
            f"We’ll wait for {int(time_to_wait.total_seconds() // 60)} minutes... like waiting for something that’ll never come back.",
            f"It’s time to wait... {int(time_to_wait.total_seconds() // 60)} minutes, but no amount of waiting will fix what’s broken.",
            f"We’re waiting again... {int(time_to_wait.total_seconds() // 60)} minutes, but it feels like waiting for nothing.",
            f"{int(time_to_wait.total_seconds() // 60)} minutes of waiting... like waiting for the end we both know is coming.",
            f"We’re waiting, {int(time_to_wait.total_seconds() // 60)} minutes... but no amount of time can heal what’s been lost."
        ]), Fore.YELLOW)
        time.sleep(time_to_wait.total_seconds())
    else:
        log_message(random.choice([
            "No need to wait... but it feels like we’ve already waited too long for things to be okay.",
            "We’ve already been waiting too long... it’s time to move forward, even if it feels like nothing matters anymore.",
            "No more waiting... but I wonder if anything we do now will make a difference.",
            "Time’s up... no need to wait, but why does it feel like we’re running out of chances?",
            "We’re done waiting... but maybe we’re also done hoping for something to change."
        ]), Fore.YELLOW)

if __name__ == "__main__":
    accounts = load_accounts_from_file('data.txt')
    while True:
        process_accounts(accounts)
