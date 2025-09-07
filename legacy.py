# Older version, mostly relies on playwright.
# Very resource intensive.

import time, os
from playwright.sync_api import sync_playwright

D2L_INDEX = int(os.getenv("D2L_INDEX"))
MS_EMAIL = os.getenv("MS_EMAIL")
MS_PASSWORD = os.getenv("MS_PASSWORD")

if os.path.exists("ms_state.json"):
    pass
else:
    with open("ms_state.json", "w") as f:
        f.write("{}")


with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(storage_state="ms_state.json")
    page = context.new_page()

    page.goto("https://nbvhs-nbed.brightspace.com/d2l/le/enhancedSequenceViewer/98982?url=https%3A%2F%2F98cafd8c-1774-45e7-b43c-b19bfcb13758.sequences.api.brightspace.com%2F98982%2Factivity%2F3310909%3FfilterOnDatesAndDepth%3D1")

    def getPageTitle():
        try:
            return page.title()
        except:
            return ""

    def openVladThread():
        page.goto("https://nbvhs-nbed.brightspace.com/d2l/le/enhancedSequenceViewer/98982?url=https%3A%2F%2F98cafd8c-1774-45e7-b43c-b19bfcb13758.sequences.api.brightspace.com%2F98982%2Factivity%2F3310909%3FfilterOnDatesAndDepth%3D1")
        page.wait_for_load_state("domcontentloaded")

        page.wait_for_selector('iframe[src*="fullscreen/3310909/View"]', timeout=30000)
        frame = page.frame(url=lambda url: "fullscreen/3310909/View" in url)

        if not frame:
            raise Exception("Frame still not found after iframe appeared!")


        try:
            frame.wait_for_function("() => window.D2L && typeof D2L.O === 'function'", timeout=10000)
            frame.evaluate(f'D2L.O("__g1", {D2L_INDEX})()')
        except Exception as e:
            print(f"Failed to run D2L.O: {e}")
            time.sleep(10)

    def handleMicrosoftLogin():
        # Fill Email input
        page.wait_for_selector("#i0116")
        page.fill("#i0116", MS_EMAIL)
        page.click("#idSIButton9")

        # Fill Password input
        page.wait_for_selector("#i0118")
        page.fill("#i0118", MS_PASSWORD)
        page.click("#idSIButton9")

        # Handle "Stay signed in?" prompt
        try:
            page.wait_for_selector("#idSIButton9", timeout=5000)
            page.click("#idSIButton9")
        except:
            pass

    try:
        while True:
            pageTitle = getPageTitle()

            if pageTitle == "Introduce Yourself":
                openVladThread()
                time.sleep(1)
            elif pageTitle == "New Brunswick Virtual Learning Centre":
                page.goto("https://nbvhs-nbed.brightspace.com/d2l/lp/auth/saml/login?target=%2Fd2l%2Fle%2FenhancedSequenceViewer%2F98982%3Furl%3Dhttps%253a%252f%252f98cafd8c-1774-45e7-b43c-b19bfcb13758.sequences.api.brightspace.com%252f98982%252factivity%252f3310909%253ffilterOnDatesAndDepth%253d1")
                if getPageTitle() == "Sign in to your account":
                    handleMicrosoftLogin()
                    context.storage_state(path="ms_state.json")
                else:
                    time.sleep(5)
                    pass
            else:
                time.sleep(5)
                pass

    except KeyboardInterrupt:
        browser.close()