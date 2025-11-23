import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Configuration
REGISTRATION_URL = "https://app.ecox.network/register?refCode=AWAISLAYYAH05"
FULL_NAME = "Your Full Name"
EMAIL = "your.email@example.com"
PASSWORD = "YourP@ssw0rd123!"  # Must meet all password requirements

def setup_driver():
    """Setup undetected Chrome driver to bypass Cloudflare"""
    print("Setting up undetected Chrome driver...")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    # options.add_argument("--headless")  # Uncomment for headless mode
    
    driver = uc.Chrome(options=options, version_main=None)
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

def handle_cloudflare(driver):
    """Wait for Cloudflare to auto-solve with undetected-chromedriver"""
    print("Waiting for Cloudflare verification (if present)...")
    time.sleep(5)  # Give Cloudflare time to appear and auto-solve
    
    # Check if we're on a Cloudflare challenge page
    try:
        # Look for Cloudflare elements
        if "challenge" in driver.current_url.lower() or "cloudflare" in driver.page_source.lower():
            print("Cloudflare challenge detected, waiting for auto-bypass...")
            time.sleep(10)  # Wait longer for auto-bypass
    except:
        pass
    
    print("Cloudflare check complete")

def automate_ecox_registration():
    """Main automation function"""
    driver = setup_driver()
    
    try:
        print("Starting ECOX registration automation...")
        
        # Step 1: Navigate to the registration page
        print(f"Navigating to: {REGISTRATION_URL}")
        driver.get(REGISTRATION_URL)
        
        # Step 2: Wait for Cloudflare to auto-bypass
        handle_cloudflare(driver)
        time.sleep(3)
        
        # Step 3: Click "Skip" button on welcome page
        print("Looking for Skip button...")
        try:
            skip_button = wait_and_click(driver, By.XPATH, "//button[text()='Skip']", timeout=10)
            print("Clicked Skip button")
            time.sleep(3)
        except Exception as e:
            print(f"Skip button not found or already on registration page")
        
        # Step 4: Wait for registration form to load
        print("Waiting for registration form...")
        WebDriverWait(driver, 15).until(
            EC.presence_of_element_located((By.XPATH, "//h1[contains(text(), 'Register')] | //h2[contains(text(), 'Register')] | //input"))
        )
        time.sleep(2)
        
        # Debug: Show all input fields
        debug_page_elements(driver)
        
        # Step 5: Fill in Full Name
        print("Filling in Full Name...")
        all_inputs = driver.find_elements(By.TAG_NAME, "input")
        text_inputs = [inp for inp in all_inputs if inp.get_attribute('type') in ['text', None]]
        
        if text_inputs:
            text_inputs[0].clear()
            text_inputs[0].send_keys(FULL_NAME)
            print(f"Entered name: {FULL_NAME}")
        
        # Step 6: Fill in Email
        print("Filling in Email...")
        email_inputs = [inp for inp in all_inputs if inp.get_attribute('type') == 'email' or 'mail' in (inp.get_attribute('placeholder') or '').lower()]
        
        if email_inputs:
            email_inputs[0].clear()
            email_inputs[0].send_keys(EMAIL)
            print(f"Entered email: {EMAIL}")
        
        # Step 7: Fill in Password fields
        print("Filling in Password fields...")
        password_inputs = [inp for inp in all_inputs if inp.get_attribute('type') == 'password']
        
        if len(password_inputs) >= 2:
            password_inputs[0].clear()
            password_inputs[0].send_keys(PASSWORD)
            print("Entered password")
            
            password_inputs[1].clear()
            password_inputs[1].send_keys(PASSWORD)
            print("Re-entered password")
        
        # The referral code should already be filled
        print("Referral code should be pre-filled: AWAISLAYYAH05")
        
        print("\n=== Form filled successfully! ===")
        print("You can now manually review and click 'Register' button")
        print("Keeping browser open for 30 seconds...")
        time.sleep(30)
        
        # Uncomment to auto-submit:
        # print("Looking for Register button...")
        # register_button = wait_and_click(driver, By.XPATH, "//button[text()='Register' or contains(text(), 'Register')]")
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