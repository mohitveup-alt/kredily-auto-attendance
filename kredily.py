# kredily.py
# Cloud-run Selenium + Telegram notifier for Kredily (designed for GitHub Actions)

import time
import os
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options

EMAIL = os.getenv("KREDILY_EMAIL")
PASSWORD = os.getenv("KREDILY_PASSWORD")
LOGIN_URL = os.getenv("KREDILY_URL")
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

# XPaths based on your screenshot - adjust only if site changes
EMAIL_XPATH = "//input[@placeholder='Email Address / Mobile Number']"
PASSWORD_XPATH = "//input[@placeholder='Password']"
LOGIN_BTN_XPATH = "//button[contains(text(),'Sign In')]"
CLOCKIN_XPATH = "//button[contains(text(),'WEB CLOCK-IN')]"
CLOCKOUT_XPATH = "//button[contains(text(),'WEB CLOCK-OUT')]"

def notify(msg):
    # simple Telegram notify
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
        data = {"chat_id": CHAT_ID, "text": msg, "parse_mode": "Markdown"}
        requests.post(url, data=data, timeout=20)
    except Exception as e:
        print("Telegram notification failed:", e)

def run_task():
    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    try:
        driver.get(LOGIN_URL)
        time.sleep(3)

        # Login
        driver.find_element(By.XPATH, EMAIL_XPATH).send_keys(EMAIL)
        driver.find_element(By.XPATH, PASSWORD_XPATH).send_keys(PASSWORD)
        driver.find_element(By.XPATH, LOGIN_BTN_XPATH).click()
        time.sleep(6)

        # Try Clock-In
        try:
            btn = driver.find_element(By.XPATH, CLOCKIN_XPATH)
            btn.click()
            notify("🟢 *Clock-In Successful* at your Kredily account.")
            print("Clock-In clicked")
        except Exception:
            print("Clock-in button not present")

        # Try Clock-Out
        try:
            btn = driver.find_element(By.XPATH, CLOCKOUT_XPATH)
            btn.click()
            notify("🔵 *Clock-Out Successful* at your Kredily account.")
            print("Clock-Out clicked")
        except Exception:
            print("Clock-out button not present")

    except Exception as e:
        notify(f"⚠️ Kredily automation failed: {e}")
        print("Error:", e)
    finally:
        driver.quit()

if __name__ == "__main__":
    run_task()
