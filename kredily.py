from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def run_task():

    chrome_options = Options()
    
    # --- FIX FOR GITHUB ACTIONS ---
    chrome_options.add_argument("--headless")  # old headless (more stable)
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=chrome_options)

    print("Opening login page...")
    driver.get("https://app.kredily.com/login")

    # --- FIX: WAIT FOR FULL PAGE RENDER ---
    time.sleep(5)

    # --- FIX: USE PLACEHOLDER SELECTORS ---
    email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@placeholder='Email Address / Mobile Number']"))
    )
    email.send_keys("YOUR_MOBILE_OR_EMAIL")

    password = driver.find_element(By.XPATH, "//input[@placeholder='Password']")
    password.send_keys("YOUR_PASSWORD")

    login_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Sign In')]")
    login_btn.click()

    print("Login submitted, waiting...")
    time.sleep(6)

    # --- HANDLE POP-UPS ---
    for xpath in [
        "//button[contains(text(),'Yes')]",
        "//button[contains(text(),'No')]",
        "//button[contains(@class,'close')]",
    ]:
        try:
            btn = WebDriverWait(driver, 5).until(
                EC.element_to_be_clickable((By.XPATH, xpath))
            )
            btn.click()
            time.sleep(1)
        except:
            pass

    print("Looking for Clock-In button...")

    clockin_btn = WebDriverWait(driver, 25).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'WEB CLOCK-IN')]"))
    )
    clockin_btn.click()

    print("Clock-in Done Successfully ✔")

    driver.quit()


if __name__ == "__main__":
    run_task()
