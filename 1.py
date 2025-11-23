from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import time

# Configuration
REGISTRATION_URL = "https://app.ecox.network/register?refCode=AWAISLAYYAH05"
FULL_NAME = "Your Full Name"
EMAIL = "your.email@example.com"
PASSWORD = "YourP@ssw0rd123!"  # Must meet all password requirements

def setup_driver():
    """Setup Chrome driver with options"""
    chrome_options = Options()
    # chrome_options.add_argument("--headless")  # Uncomment for headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--start-maximized")
    
    driver = webdriver.Chrome(options=chrome_options)
    return driver

def wait_and_click(driver, by, value, timeout=10):
    """Wait for element and click it"""
    element = WebDriverWait(driver, timeout).until(
        EC.element_to_be_clickable((by, value))
    )
    element.click()
    return element

def wait_and_send_keys(driver, by, value, text, timeout=10):
    """Wait for element and send keys"""
    element = WebDriverWait(driver, timeout).until(
        EC.presence_of_element_located((by, value))
    )
    element.clear()
    element.send_keys(text)
    return element

def debug_page_elements(driver):
    """Print all input fields on the page for debugging"""
    print("\n=== DEBUG: Available input fields ===")
    inputs = driver.find_elements(By.TAG_NAME, "input")
    for i, inp in enumerate(inputs):
        print(f"Input {i}: type='{inp.get_attribute('type')}', "
              f"placeholder='{inp.get_attribute('placeholder')}', "
              f"name='{inp.get_attribute('name')}'")
    print("===================================\n")

def automate_ecox_registration():
    """Main automation function"""
    driver = setup_driver()
    
    try:
        print("Starting ECOX registration automation...")
        
        # Step 1: Navigate to the registration page
        print(f"Navigating to: {REGISTRATION_URL}")
        driver.get(REGISTRATION_URL)
        time.sleep(2)
        
        # Step 2: Click "Skip" button on welcome page
        print("Looking for Skip button...")
        try:
            skip_button = wait_and_click(driver, By.XPATH, "//button[text()='Skip']", timeout=10)
            print("Clicked Skip button")
            time.sleep(3)
        except Exception as e:
            print(f"Skip button not found or already on registration page: {e}")
        
        # Step 3: Fill in Full Name
        print("Filling in Full Name...")
        # Wait for registration form to load
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Register')] | //h2[contains(text(), 'Register')]"))
        )
        time.sleep(1)
        
        # Debug: Show all input fields
        debug_page_elements(driver)
        
        name_input = wait_and_send_keys(
            driver, 
            By.XPATH, 
            "//input[@type='text' and contains(@class, 'form') or @placeholder='Full Name']",
            FULL_NAME
        )
        print(f"Entered name: {FULL_NAME}")
        
        # Step 4: Fill in Email
        print("Filling in Email...")
        email_input = wait_and_send_keys(
            driver,
            By.XPATH,
            "//input[@type='email' or @type='text'][contains(@placeholder, 'mail') or contains(@class, 'mail')]",
            EMAIL
        )
        print(f"Entered email: {EMAIL}")
        
        # Step 5: Fill in Password
        print("Filling in Password...")
        password_inputs = driver.find_elements(By.XPATH, "//input[@type='password']")
        if len(password_inputs) >= 1:
            password_inputs[0].clear()
            password_inputs[0].send_keys(PASSWORD)
            print("Entered password")
        
        # Step 6: Fill in Re-enter Password
        print("Re-entering Password...")
        if len(password_inputs) >= 2:
            password_inputs[1].clear()
            password_inputs[1].send_keys(PASSWORD)
            print("Re-entered password")
        else:
            # Try alternative method
            reenter_password_input = wait_and_send_keys(
                driver,
                By.XPATH,
                "//input[@type='password'][2]",
                PASSWORD
            )
            print("Re-entered password")
        
        # Step 7: Verify password requirements are met
        print("Waiting for password validation...")
        time.sleep(1)
        
        # The referral code should already be filled
        print("Referral code should be pre-filled: AWAISLAYYAH05")
        
        print("\n=== Form filled successfully! ===")
        print("You can now manually review and click 'Register' button")
        print("Keeping browser open for 30 seconds...")
        time.sleep(30)
        
        # Uncomment to auto-submit:
        # register_button = wait_and_click(driver, By.XPATH, "//button[text()='Register']")
        # print("Clicked Register button")
        # time.sleep(5)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    automate_ecox_registration()