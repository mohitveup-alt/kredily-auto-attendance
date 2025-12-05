from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time

def run_task():

    chrome_options = Options()
    chrome_options.add_argument("--headless=new")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)

    driver.get("https://app.kredily.com/login")

    # --- LOGIN ---
    email = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='username']"))
    )
    email.send_keys("YOUR_MOBILE_OR_EMAIL")

    password = driver.find_element(By.XPATH, "//input[@id='password']")
    password.send_keys("YOUR_PASSWORD")

    login_btn = driver.find_element(By.XPATH, "//button[contains(text(),'Sign In')]")
    login_btn.click()

    time.sleep(3)

    # --- HANDLE RANDOM POP-UP ---
    try:
        close_popup = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(@class,'close')]"))
        )
        close_popup.click()
    except:
        pass

    try:
        yes_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Yes')]"))
        )
        yes_btn.click()
    except:
        pass

    # --- CLOCK-IN ---
    clockin_btn = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'WEB CLOCK-IN')]"))
    )
    clockin_btn.click()

    print("Clock-in Done Successfully ✔")

    driver.quit()

if __name__ == "__main__":
    run_task()
