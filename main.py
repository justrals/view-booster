import json
import requests
import time
import os
from pathlib import Path
from playwright.sync_api import sync_playwright

COOKIES_FILE = "cookies.json"
REFRESH_INTERVAL = 60 * 30

def grabCookies():
    MS_EMAIL = os.getenv("MS_EMAIL")
    MS_PASSWORD = os.getenv("MS_PASSWORD")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto("https://nbvhs-nbed.brightspace.com/d2l/lp/auth/saml/login?...")

            page.wait_for_selector("#i0116", timeout=20000)
            page.fill("#i0116", MS_EMAIL)
            page.click("#idSIButton9")

            page.wait_for_selector("#i0118", timeout=20000)
            page.fill("#i0118", MS_PASSWORD)
            page.click("#idSIButton9")

            try:
                page.wait_for_selector("#idSIButton9", timeout=5000)
                page.click("#idSIButton9")
            except:
                pass

            page.wait_for_load_state("domcontentloaded")
            time.sleep(5)

            cookies = {c["name"]: c["value"] for c in context.cookies()}
            with open(COOKIES_FILE, "w") as f:
                json.dump({"cookies": cookies}, f, indent=2)

            print("[ ✓ ] Successfully refreshed cookies.")
            return cookies

        finally:
            browser.close()

def loadCookies():
    if Path(COOKIES_FILE).exists():
        with open(COOKIES_FILE, "r") as f:
            return json.load(f).get("cookies", {})
    return {}

cookies = loadCookies()
last_refresh = 0

url = "https://nbvhs-nbed.brightspace.com/d2l/le/98982/discussions/threads/448574/ViewPartial?inContentTool=true&_d2l_prc%24headingLevel=2&_d2l_prc%24scope=&_d2l_prc%24hasActiveForm=false&isXhr=true&requestId=4"
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux aarch64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/139.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Referer": "https://nbvhs-nbed.brightspace.com/"
}

while True:
    if time.time() - last_refresh > REFRESH_INTERVAL or not cookies:
        print("[ ⟳ ] Refreshing cookies...")
        cookies = grabCookies()
        last_refresh = time.time()

    resp = requests.get(url, headers=headers, cookies=cookies)
    raw = resp.text
    if raw.startswith("while(1);"):
        raw = raw[len("while(1);"):]
    try:
        data = json.loads(raw)
    except json.JSONDecodeError:
        print("[ ✗ ] Failed to decode JSON, response:", raw)