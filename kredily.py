import os
import time
from playwright.sync_api import sync_playwright

def run_once(action):
    print("Opening login page...")

    with sync_playwright() as p:
        browser = p.firefox.launch(headless=True)
        page = browser.new_page()

        page.goto("https://app.kredily.com/login", timeout=60000)

        # --- LOGIN ---
        page.wait_for_selector('input[placeholder="Email Address / Mobile Number"]', timeout=30000)
        page.fill('input[placeholder="Email Address / Mobile Number"]', os.getenv("KREDILY_USER"))
        page.fill('input[placeholder="Password"]', os.getenv("KREDILY_PASS"))

        page.click('button[type="submit"]')

        page.wait_for_load_state("networkidle")

        # --- CLOSE ANY POPUP ---
        try:
            page.click("button.close", timeout=3000)
        except:
            pass

        # --- CLOCK-IN / CLOCK-OUT ---
        if action == "clockin":
            btn_text = "WEB CLOCK-IN"
        else:
            btn_text = "WEB CLOCK-OUT"

        page.wait_for_selector(f"button:has-text('{btn_text}')", timeout=30000)
        page.click(f"button:has-text('{btn_text}')")

        print(f"{action.upper()} successful ✔")
        browser.close()


if __name__ == "__main__":
    action = os.getenv("ACTION")
    run_once(action)
