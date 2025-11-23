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
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    # options.add_argument("--headless")  # Uncomment for headless mode (not recommended for Cloudflare)
    
    # Create driver with undetected-chromedriver
    driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)
    
    # Set additional properties to appear more human
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """
    })
    
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

def handle_cloudflare(driver, max_wait=30):
    """Wait for Cloudflare to auto-solve with undetected-chromedriver"""
    print("Waiting for Cloudflare verification (if present)...")
    
    start_time = time.time()
    cloudflare_detected = False
    
    while time.time() - start_time < max_wait:
        try:
            # Check for Cloudflare iframe
            iframes = driver.find_elements(By.TAG_NAME, "iframe")
            
            for iframe in iframes:
                iframe_src = iframe.get_attribute("src") or ""
                iframe_title = iframe.get_attribute("title") or ""
                
                # Check if it's a Cloudflare Turnstile iframe
                if "cloudflare" in iframe_src.lower() or "turnstile" in iframe_src.lower() or "challenges.cloudflare.com" in iframe_src:
                    if not cloudflare_detected:
                        print("⏳ Cloudflare Turnstile detected! Waiting for auto-solve...")
                        cloudflare_detected = True
                    
                    # Check if verification is complete by looking for success indicators
                    try:
                        driver.switch_to.frame(iframe)
                        # Look for success checkmark or completion
                        success_elements = driver.find_elements(By.XPATH, "//*[contains(@class, 'success') or contains(text(), 'Success')]")
                        driver.switch_to.default_content()
                        
                        if success_elements:
                            print("✅ Cloudflare verification successful!")
                            return True
                    except:
                        driver.switch_to.default_content()
                    
                    time.sleep(2)
                    break
            else:
                # No Cloudflare iframe found - might be complete or not present
                if cloudflare_detected:
                    print("✅ Cloudflare iframe disappeared - verification likely complete!")
                    return True
                else:
                    # Check if we can proceed (no Cloudflare blocking)
                    if "Just a moment" not in driver.page_source and "Checking your browser" not in driver.page_source:
                        print("✅ No Cloudflare challenge detected")
                        return True
            
            time.sleep(1)
            
        except Exception as e:
            driver.switch_to.default_content()
            time.sleep(1)
    
    print(f"⚠️ Waited {max_wait} seconds for Cloudflare. Proceeding anyway...")
    return True

def automate_ecox_registration():
    """Main automation function"""
    driver = setup_driver()
    
    try:
        print("Starting ECOX registration automation...")
        
        # Step 1: Navigate to the registration page
        print(f"Navigating to: {REGISTRATION_URL}")
        driver.get(REGISTRATION_URL)
        
        # Step 2: Wait for Cloudflare to auto-bypass
        handle_cloudflare(driver, max_wait=30)
        time.sleep(2)
        
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
        print("Waiting a moment before submitting...")
        time.sleep(2)
        
        # Step 8: Click Register button
        print("Looking for Register button...")
        try:
            register_button = None
            
            # Method 1: By type submit and text Register
            try:
                register_button = wait_and_click(driver, By.XPATH, "//button[@type='submit' and text()='Register']", timeout=5)
                print("✅ Clicked Register button (Method 1: submit + text)")
            except:
                pass
            
            # Method 2: By class and type submit
            if not register_button:
                try:
                    register_button = wait_and_click(driver, By.XPATH, "//button[@type='submit' and contains(@class, 'bg-custom-gradient')]", timeout=5)
                    print("✅ Clicked Register button (Method 2: class + submit)")
                except:
                    pass
            
            # Method 3: By type submit only
            if not register_button:
                try:
                    register_button = wait_and_click(driver, By.XPATH, "//button[@type='submit']", timeout=5)
                    print("✅ Clicked Register button (Method 3: submit type)")
                except:
                    pass
            
            # Method 4: By text Register
            if not register_button:
                try:
                    register_button = wait_and_click(driver, By.XPATH, "//button[text()='Register']", timeout=5)
                    print("✅ Clicked Register button (Method 4: by text)")
                except:
                    pass
            
            # Method 5: Find the button by its full class attributes
            if not register_button:
                try:
                    buttons = driver.find_elements(By.XPATH, "//button[contains(@class, 'w-full') and contains(@class, 'bg-custom-gradient')]")
                    for btn in buttons:
                        if 'register' in btn.text.lower():
                            btn.click()
                            print(f"✅ Clicked Register button (Method 5: by classes)")
                            register_button = btn
                            break
                except:
                    pass
            
            if register_button:
                print("\n🎉 Registration form submitted!")
                print("Waiting for response...")
                time.sleep(5)
                
                # Check for success or error messages
                page_text = driver.page_source.lower()
                current_url = driver.current_url
                
                print(f"Current URL: {current_url}")
                
                if "success" in page_text or "welcome" in page_text or "dashboard" in current_url or "verify" in page_text or "email" in page_text:
                    print("✅ Registration appears successful!")
                elif "error" in page_text or "already exist" in page_text or "invalid" in page_text:
                    print("⚠️ There might be an error. Check the browser.")
                else:
                    print("ℹ️ Please check the browser to confirm registration status")
                
            else:
                print("⚠️ Could not find Register button automatically")
                print("Please click it manually")
        
        except Exception as e:
            print(f"Error clicking Register button: {e}")
            print("Please click it manually")
        
        print("\nKeeping browser open for 20 seconds for you to review...")
        time.sleep(20)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    automate_ecox_registration()