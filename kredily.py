# kredily.py
# Playwright script for Kredily clock-in / clock-out + Telegram notifications

import os
import time
import requests
from playwright.sync_api import sync_playwright

KREDILY_USER = os.getenv("KREDILY_USER")
KREDILY_PASS = os.getenv("KREDILY_PASS")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")   # optional
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")       # optional

LOGIN_URL = "https://app.kredily.com/login"

def telegram_notify(text):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
        requests.post(url, data={"chat_id": TELEGRAM_CHAT_ID, "text": text})
    except Exception as e:
        print("Telegram notify failed:", e)

def run_once(action="clockin"):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()

        print("Opening login page...")
        page.goto(LOGIN_URL, timeout=60000)

        # Wait for login fields
        page.wait_for_selector("input#username, input[name=username], input[placeholder]", timeout=30000)

        # fill credentials (try several selectors to be robust)
        try:
            page.fill("#username", KREDILY_USER)
        except:
            try:
                page.fill("input[name='username']", KREDILY_USER)
            except:
                page.fill("input[placeholder='Email Address / Mobile Number']", KREDILY_USER)

        try:
            page.fill("#password", KREDILY_PASS)
        except:
            page.fill("input[placeholder='Password']", KREDILY_PASS)

        # click Sign In
        page.click("button:has-text('Sign In')", timeout=10000)
        page.wait_for_timeout(3000)

        # Handle possible popups (best-effort)
        for sel in ["button:has-text('Yes')", "button:has-text('No')", "button.close", "button[aria-label='close']"]:
            try:
                page.click(sel, timeout=2000)
                page.wait_for_timeout(500)
            except:
                pass

        # Wait for dashboard to load
        page.wait_for_timeout(2000)

        # Depending on action, click relevant button
        try:
            if action == "clockin":
                page.wait_for_selector("button:has-text('WEB CLOCK-IN')", timeout=20000)
                page.click("button:has-text('WEB CLOCK-IN')")
                msg = "🟢 Clock-In Successful"
            else:
                page.wait_for_selector("button:has-text('WEB CLOCK-OUT')", timeout=20000)
                page.click("button:has-text('WEB CLOCK-OUT')")
                msg = "🔵 Clock-Out Successful"

            print(msg)
            telegram_notify(msg)
        except Exception as e:
            err = f"⚠️ Kredily {action} failed: {e}"
            print(err)
            telegram_notify(err)

        browser.close()

if __name__ == "__main__":
    # The script will be called twice by GitHub Actions with different env (see workflow)
    # Default action is clockin
    run_once(action=os.getenv("ACTION", "clockin"))
