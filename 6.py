import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import random
import string
from datetime import datetime

# Auto-generate unique credentials
def generate_unique_credentials():
    """Generate unique credentials that meet all requirements"""
    
    # Generate timestamp for uniqueness
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    random_suffix = ''.join(random.choices(string.digits, k=4))
    
    # Generate Full Name (first name + last name)
    first_names = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles",
                   "Mary", "Patricia", "Jennifer", "Linda", "Elizabeth", "Barbara", "Susan", "Jessica", "Sarah", "Karen"]
    last_names = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez",
                  "Wilson", "Anderson", "Taylor", "Thomas", "Moore", "Jackson", "Martin", "Lee", "Thompson", "White"]
    
    full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
    
    # Generate Email (unique with timestamp)
    email_prefix = f"user{timestamp}{random_suffix}"
    email_domains = ["gmail.com", "yahoo.com", "outlook.com", "hotmail.com", "protonmail.com"]
    email = f"{email_prefix}@{random.choice(email_domains)}"
    
    # Generate Username (3-50 chars, lowercase letters and numbers only)
    username = f"user{timestamp}{random_suffix}".lower()
    
    # Generate Password (8-32 chars, 1 lowercase, 1 uppercase, 1 number, 1 special char)
    password_length = random.randint(12, 20)
    
    # Ensure we have at least one of each required character type
    password_chars = [
        random.choice(string.ascii_lowercase),  # At least 1 lowercase
        random.choice(string.ascii_uppercase),  # At least 1 uppercase
        random.choice(string.digits),           # At least 1 number
        random.choice("!@#$%^&*()_+-=[]{}|;:,.<>?")  # At least 1 special char
    ]
    
    # Fill the rest randomly
    all_chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?"
    password_chars += [random.choice(all_chars) for _ in range(password_length - 4)]
    
    # Shuffle to make it random
    random.shuffle(password_chars)
    password = ''.join(password_chars)
    
    return {
        'full_name': full_name,
        'email': email,
        'username': username,
        'password': password
    }

# Configuration
REGISTRATION_URL = "https://app.ecox.network/register?refCode=AWAISLAYYAH05"

# Generate unique credentials
credentials = generate_unique_credentials()
FULL_NAME = credentials['full_name']
EMAIL = credentials['email']
USERNAME = credentials['username']
PASSWORD = credentials['password']

# Print generated credentials for reference
print("\n" + "="*60)
print("GENERATED CREDENTIALS (SAVE THESE!):")
print("="*60)
print(f"Full Name: {FULL_NAME}")
print(f"Email: {EMAIL}")
print(f"Username: {USERNAME}")
print(f"Password: {PASSWORD}")
print("="*60 + "\n")

def setup_driver():
    """Setup undetected Chrome driver to bypass Cloudflare"""
    print("Setting up undetected Chrome driver...")
    options = uc.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-blink-features=AutomationControlled")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-web-security")
    options.add_argument("--disable-features=IsolateOrigins,site-per-process")
    
    # Add user agent to appear more legitimate
    options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
    
    # options.add_argument("--headless=new")  # Uncomment for headless mode (not recommended for Cloudflare)
    
    # Create driver with undetected-chromedriver
    driver = uc.Chrome(options=options, version_main=None, use_subprocess=True)
    
    # Additional stealth configurations
    driver.execute_cdp_cmd("Network.setUserAgentOverride", {
        "userAgent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    })
    
    driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
        "source": """
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
            Object.defineProperty(navigator, 'plugins', {
                get: () => [1, 2, 3, 4, 5]
            });
            Object.defineProperty(navigator, 'languages', {
                get: () => ['en-US', 'en']
            });
        """
    })
    
    print("✅ Driver setup complete with anti-detection features")
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

def save_credentials_to_file(creds):
    """Save credentials to a text file"""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open("ecox_accounts.txt", "a", encoding="utf-8") as f:
            f.write(f"\n{'='*60}\n")
            f.write(f"Registration Date: {timestamp}\n")
            f.write(f"Full Name: {creds['full_name']}\n")
            f.write(f"Email: {creds['email']}\n")
            f.write(f"Username: {creds['username']}\n")
            f.write(f"Password: {creds['password']}\n")
            f.write(f"Referral Code: AWAISLAYYAH05\n")
            f.write(f"{'='*60}\n")
        print(f"\n💾 Credentials saved to 'ecox_accounts.txt'")
    except Exception as e:
        print(f"⚠️ Could not save credentials to file: {e}")

def handle_cloudflare(driver, max_wait=60):
    """Wait for Cloudflare to auto-solve with undetected-chromedriver"""
    print("Checking for Cloudflare verification...")
    
    start_time = time.time()
    cloudflare_detected = False
    last_check_time = 0
    
    while time.time() - start_time < max_wait:
        try:
            current_time = time.time()
            
            # Only check every 2 seconds to avoid overwhelming the page
            if current_time - last_check_time < 2:
                time.sleep(0.5)
                continue
            
            last_check_time = current_time
            
            page_source = driver.page_source.lower()
            
            # Check for Cloudflare challenge indicators
            cloudflare_indicators = [
                "just a moment" in page_source,
                "checking your browser" in page_source,
                "verify you are human" in page_source,
                "challenge" in driver.current_url.lower(),
                "cloudflare" in page_source and "ray id" in page_source
            ]
            
            if any(cloudflare_indicators):
                if not cloudflare_detected:
                    print("⏳ Cloudflare challenge detected! Waiting for bypass...")
                    print("   This may take 10-30 seconds. Please wait...")
                    cloudflare_detected = True
                
                # Print progress dots
                elapsed = int(time.time() - start_time)
                print(f"   Waiting... {elapsed}s", end='\r')
                
                # Check for iframes (Turnstile)
                try:
                    iframes = driver.find_elements(By.TAG_NAME, "iframe")
                    for iframe in iframes:
                        iframe_src = iframe.get_attribute("src") or ""
                        if "cloudflare" in iframe_src or "turnstile" in iframe_src:
                            # Don't interact, just wait for auto-solve
                            time.sleep(2)
                            break
                except:
                    pass
                
                time.sleep(2)
                continue
            
            # Check if we've successfully passed Cloudflare
            if cloudflare_detected:
                # Verify we're really past it
                time.sleep(2)
                page_source_recheck = driver.page_source.lower()
                
                if not any([
                    "just a moment" in page_source_recheck,
                    "checking your browser" in page_source_recheck,
                    "verify you are human" in page_source_recheck
                ]):
                    print("\n✅ Cloudflare bypass successful!")
                    time.sleep(2)  # Extra wait to ensure page is stable
                    return True
            else:
                # No Cloudflare detected at all
                print("✅ No Cloudflare challenge detected")
                return True
            
            time.sleep(1)
            
        except Exception as e:
            driver.switch_to.default_content()
            time.sleep(1)
    
    print(f"\n⚠️ Waited {max_wait} seconds. Attempting to continue...")
    print("   If registration fails, Cloudflare may require manual intervention")
    return False

def automate_ecox_registration():
    """Main automation function"""
    driver = setup_driver()
    
    try:
        print("Starting ECOX registration automation...")
        
        # Step 1: Navigate to the registration page
        print(f"Navigating to: {REGISTRATION_URL}")
        driver.get(REGISTRATION_URL)
        print("Page loaded, waiting for stability...")
        time.sleep(3)
        
        # Step 2: Wait for Cloudflare to auto-bypass (increased timeout)
        cloudflare_passed = handle_cloudflare(driver, max_wait=60)
        
        if not cloudflare_passed:
            print("\n⚠️ MANUAL INTERVENTION NEEDED:")
            print("   Please complete the Cloudflare challenge manually if you see one.")
            print("   The script will wait 30 seconds for you to complete it...")
            time.sleep(30)
        
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
                    print("ℹ️ Registration submitted, checking next page...")
                
            else:
                print("⚠️ Could not find Register button automatically")
                print("Please click it manually")
        
        except Exception as e:
            print(f"Error clicking Register button: {e}")
            print("Please click it manually")
        
        # Step 9: Handle Username Selection Page
        print("\n" + "="*50)
        print("Checking for Username Selection page...")
        try:
            # Wait for username page to load
            time.sleep(3)
            
            # Check if we're on the username selection page
            if "username" in driver.page_source.lower() or "choose username" in driver.page_source.lower():
                print("✅ Username selection page detected!")
                
                # Find the username input field
                print("Looking for username input field...")
                username_input = None
                
                try:
                    # Try to find by placeholder
                    username_input = wait_and_send_keys(driver, By.XPATH, "//input[@placeholder='@username' or contains(@placeholder, 'username')]", USERNAME, timeout=5)
                    print(f"✅ Entered username: {USERNAME}")
                except:
                    pass
                
                # Try alternative methods if first didn't work
                if not username_input:
                    try:
                        # Find input with user icon or in username section
                        inputs = driver.find_elements(By.TAG_NAME, "input")
                        for inp in inputs:
                            placeholder = inp.get_attribute('placeholder') or ''
                            if 'username' in placeholder.lower() or '@' in placeholder:
                                inp.clear()
                                inp.send_keys(USERNAME)
                                print(f"✅ Entered username: {USERNAME}")
                                username_input = inp
                                break
                    except:
                        pass
                
                if username_input:
                    print("Username entered successfully!")
                    time.sleep(2)
                    
                    # Click the Register button on username page
                    print("Looking for Register button on username page...")
                    try:
                        # Try to find the register button with same class
                        register_btn = None
                        
                        # Method 1: By type submit and text
                        try:
                            register_btn = wait_and_click(driver, By.XPATH, "//button[@type='submit' and text()='Register']", timeout=5)
                            print("✅ Clicked Register button on username page!")
                        except:
                            pass
                        
                        # Method 2: By class
                        if not register_btn:
                            try:
                                register_btn = wait_and_click(driver, By.XPATH, "//button[@type='submit' and contains(@class, 'bg-custom-gradient')]", timeout=5)
                                print("✅ Clicked Register button on username page!")
                            except:
                                pass
                        
                        # Method 3: Any submit button
                        if not register_btn:
                            try:
                                register_btn = wait_and_click(driver, By.XPATH, "//button[@type='submit']", timeout=5)
                                print("✅ Clicked Register button on username page!")
                            except:
                                pass
                        
                        if register_btn:
                            print("\n🎉🎉 REGISTRATION COMPLETED! 🎉🎉")
                            print("Waiting for final confirmation...")
                            time.sleep(5)
                            
                            final_url = driver.current_url
                            print(f"Final URL: {final_url}")
                            
                            if "dashboard" in final_url or "home" in final_url or "account" in final_url:
                                print("✅✅ Successfully registered and logged in!")
                                
                                # Save credentials to file
                                save_credentials_to_file(credentials)
                            else:
                                print("ℹ️ Please check the browser for final status")
                                save_credentials_to_file(credentials)
                        else:
                            print("⚠️ Could not find Register button on username page")
                            print("Please click it manually")
                            
                    except Exception as e:
                        print(f"Error clicking username Register button: {e}")
                        print("Please complete manually")
                else:
                    print("⚠️ Could not enter username automatically")
                    print("Please enter it manually")
            else:
                print("ℹ️ No username selection page detected - registration may be complete!")
                
        except Exception as e:
            print(f"Note: {e}")
            print("Username page may not be present")
        
        print("\nKeeping browser open for 30 seconds for you to review...")
        time.sleep(30)
        
    except Exception as e:
        print(f"An error occurred: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        print("Closing browser...")
        driver.quit()

if __name__ == "__main__":
    automate_ecox_registration()