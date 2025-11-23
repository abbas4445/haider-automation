import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import os

# =====================================
# CONFIGURATION
# =====================================

REGISTRATION_URL = "https://app.ecox.network/register?refCode=AWAISLAYYAH05"
BASE_FULL_NAME = "Your Full Name"
BASE_EMAIL = "your.email"  # number + @example.com will be appended
BASE_USERNAME = "yourusername"  # number appended automatically
PASSWORD = "YourP@ssw0rd123!"

ACCOUNTS_FILE = "accounts.txt"


# =====================================
# DRIVER SETUP
# =====================================

def setup_driver():
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")

    driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)

    # Make webdriver undetected
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": "Object.defineProperty(navigator, 'webdriver', {get: () => undefined});"
    })

    return driver


def wait_and_click(driver, by, value, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()
    return element


def wait_and_send_keys(driver, by, value, text, timeout=10):
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
    element.clear()
    element.send_keys(text)
    return element


# =====================================
# CLOUDFLARE HANDLER
# =====================================

def handle_cloudflare(driver, max_wait=30):
    print("Checking Cloudflare...")

    start = time.time()
    while time.time() - start < max_wait:

        # If Cloudflare screen is gone → continue
        if "Just a moment" not in driver.page_source and "Checking your browser" not in driver.page_source:
            return True

        print("Waiting for Cloudflare to auto-bypass...")
        time.sleep(2)

    print("Proceeding anyway...")
    return True


# =====================================
# REGISTRATION FUNCTION (1 ACCOUNT)
# =====================================

def create_ecox_account():
    """Creates ONE account and returns (email, username, password)"""
    
    # Generate random unique number
    num = random.randint(100000, 99999999999999999)

    FULL_NAME = BASE_FULL_NAME
    EMAIL = f"{BASE_EMAIL}{num}@gmail.com"
    USERNAME = f"{BASE_USERNAME}{num}".lower()

    driver = setup_driver()

    try:
        print(f"\n=== Creating account for {EMAIL} ===")

        driver.get(REGISTRATION_URL)
        handle_cloudflare(driver)

        # Try clicking Skip if visible
        try:
            wait_and_click(driver, By.XPATH, "//button[text()='Skip']", timeout=5)
            time.sleep(2)
        except:
            pass

        # Fill Full Name
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        text_inputs = [i for i in all_inputs if i.get_attribute("type") == "text"]

        if text_inputs:
            text_inputs[0].send_keys(FULL_NAME)

        # Fill Email
        for inp in all_inputs:
            if inp.get_attribute("type") == "email":
                inp.send_keys(EMAIL)

        # Fill Password + Confirm Password
        password_inputs = [i for i in all_inputs if i.get_attribute("type") == "password"]
        if len(password_inputs) >= 2:
            password_inputs[0].send_keys(PASSWORD)
            password_inputs[1].send_keys(PASSWORD)

        # Click Register Button
        try:
            wait_and_click(driver, By.XPATH, "//button[@type='submit']", timeout=7)
        except:
            print("Manual click required. Waiting 15 seconds...")
            time.sleep(15)

        time.sleep(5)

        # Username Page
        if "username" in driver.page_source.lower():
            print("Username page detected...")
            try:
                wait_and_send_keys(driver, By.XPATH, "//input", USERNAME, timeout=5)
                wait_and_click(driver, By.XPATH, "//button[@type='submit']", timeout=7)
            except:
                pass

        print("✔ Account created!")

        return EMAIL, USERNAME, PASSWORD

    except Exception as e:
        print("❌ Error:", e)
        return None

    finally:
        driver.quit()


# =====================================
# MULTIPLE ACCOUNT CREATION LOOP
# =====================================

def create_multiple_accounts(count):
    """Creates N emails & logs them to accounts.txt"""

    created = 0

    if not os.path.exists(ACCOUNTS_FILE):
        open(ACCOUNTS_FILE, "w").close()

    for i in range(1, count + 1):
        print(f"\n==============================")
        print(f"🌱 Creating Account {i} of {count}")
        print(f"==============================")

        result = create_ecox_account()
        if result:
            email, username, password = result

            # Save to file
            with open(ACCOUNTS_FILE, "a") as f:
                f.write(f"{email} | {username} | {password}\n")

            created += 1
            print(f"✔ Saved to accounts.txt ({created}/{count})")
        else:
            print("❌ Failed, skipping...")

        # wait between accounts (optional)
        time.sleep(3)

    print(f"\n🎉 DONE! Created {created}/{count} accounts.")
    print(f"Saved in: {ACCOUNTS_FILE}")


# =====================================
# MAIN
# =====================================

if __name__ == "__main__":
    how_many = int(input("How many accounts do you want to create? "))
    create_multiple_accounts(how_many)
