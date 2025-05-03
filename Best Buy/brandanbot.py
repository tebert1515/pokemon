from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from fake_useragent import UserAgent
import time
import random
import requests

# Generate a randomized User-Agent
ua = UserAgent()
user_agent = ua.random

# Set up Chrome options
options = Options()
options.add_argument("--start-maximized")
options.add_argument("--disable-blink-features=AutomationControlled")  # Prevent bot detection
options.add_argument(f"user-agent={user_agent}")  # Randomized User-Agent
options.add_argument("--user-data-dir=C:/Users/brand/AppData/Local/Google/Chrome/User Data/Default") # chrome://version/ 
#options.add_argument("--user-data-dir=C:/Users/teber/AppData/Local/Google/Chrome/User Data/SeleniumProfile") # chrome://version/ 
options.add_argument("--profile-directory=Default")
options.add_argument("--disable-features=MetricsReporting")
options.add_experimental_option("excludeSwitches", ["enable-automation"])  
options.add_experimental_option("useAutomationExtension", False) 

# Enable headless mode
#options.add_argument("--headless=new")
#options.add_argument("window-size=1920,1080")
#options.add_argument("--disable-gpu")  # Disable GPU hardware acceleration (may improve stability in headless mode)

# Use WebDriver Manager to automatically install/update ChromeDriver
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")

# Open Best Buy and login manually
driver.get("https://www.bestbuy.com/")
input("Log in manually if needed, then press Enter to continue...")

# Navigate to the correct product page
#correct_product_url = "https://www.bestbuy.com/site/pokemon-trading-card-game-scarlet-violet-prismatic-evolutions-super-premium-collection/6621081.p?skuId=6621081"
#correct_sku = "6621081"
correct_product_url = "https://www.bestbuy.com/site/pokemon-trading-card-game-cynthias-garchomp-ex-premium-collection/6625124.p?skuId=6625124"
correct_sku = "6625124"
#correct_product_url = "https://www.bestbuy.com/site/pokemon-trading-card-game-melmetal-ex-or-houndoom-ex-battle-deck/6569164.p?skuId=6569164"
#correct_sku = "6569164"
driver.get(correct_product_url)

DISCORD_WEBHOOK_URL = "https://discord.com/api/webhooks/1356292796528721990/K5ppOOK8NcUzaWPyXK4oBCOsMDQhfBZBgczFm8BrpAmsIq5QsonAa-UBdvrrmJybx6Ax"

# Function to send Discord alert via webhook
def send_discord_alert():
    payload = {
        "content": f"**OMG! You caught a Pokemon in your shopping cart! You're on your way to becoming a Pokemon master!!**\n\n"
                   f"**Product:** {product_name}\n"
                   f"**Link:** {correct_product_url}\n\n"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=payload)
    if response.status_code == 204:
        print("Discord notification sent!")
    else:
        print(f"Failed to send Discord notification: {response.text}")

def get_current_ip():
    try:
        response = requests.get("https://api64.ipify.org?format=json", timeout=5)
        if response.status_code == 200:
            ip = response.json().get("ip", "Unknown")
            print(f"Current IP Address: {ip}")
        else:
            print("Failed to retrieve IP address.")
    except Exception as e:
        print(f"Error fetching IP: {e}")

# Function to perform a human-like click
def human_like_click(element):
    actions = ActionChains(driver)
    actions.move_to_element(element).pause(random.uniform(0.5, 2)).click().perform()

# Function to simulate scrolling
def human_like_scroll():
    for _ in range(random.randint(1, 3)):  # Random scroll actions
        driver.execute_script("window.scrollBy(0, arguments[0]);", random.randint(100, 500))
        time.sleep(random.uniform(1, 2))  # Random delay between scrolls

# Function to check for 'Add to Cart' or 'Coming Soon' button state
def check_button_state():
    try:
        # First, check if "Coming Soon" button is present (product NOT available)
        coming_soon = driver.find_elements(By.CSS_SELECTOR, "button[data-test-id='coming-soon']")
        if coming_soon:
            print("Detected 'Coming Soon' button - product not available.")
            return None

        # Then, check for active "Add to Cart" button (product available)
        add_to_cart_button = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "button[data-test-id='add-to-cart']"))
        )
        return add_to_cart_button

    except Exception as e:
        print(f"Error checking button state: {e}")
        return None

# Function to perform a click and confirm navigation
def click_and_confirm_navigation(element, expected_url_keyword, timeout=10):
    # Clicks element and verifies that navigation occurs.
    initial_url = driver.current_url  # Store current URL before click
    
    try:
        WebDriverWait(driver, timeout).until(EC.element_to_be_clickable(element))
        ActionChains(driver).move_to_element(element).pause(random.uniform(0.5, 2)).click().perform()
        print("Clicked button, waiting for navigation...")

        # Wait for URL to change or new page content to appear
        WebDriverWait(driver, timeout).until(lambda d: expected_url_keyword in d.current_url or d.current_url != initial_url)
        
        print(f"Successfully navigated to the next page: {driver.current_url}")
        return True
    
    except Exception as e:
        print(f"Click detected but no navigation happened: {e}. Trying JavaScript click...")

        # Try JavaScript Click
        try:
            driver.execute_script("arguments[0].click();", element)
            WebDriverWait(driver, timeout).until(lambda d: expected_url_keyword in d.current_url or d.current_url != initial_url)
            print(f"Successfully navigated via JavaScript click: {driver.current_url}")
            return True
        except Exception as js_e:
            print(f"JavaScript click also failed: {js_e}. Refreshing page and retrying...")

            # Refresh and retry as a last resort
            driver.refresh()
            time.sleep(3)  # Allow time for page reload
            return False

# Monitor product availability                                                                
print("Monitoring product availability...")
while True:
    get_current_ip() # Retrieve and print current IP Address
    human_like_scroll()  # Scroll before interacting
    add_to_cart_btn = check_button_state()
    if add_to_cart_btn:
        print("Product is now available! Adding to cart...")
        if click_and_confirm_navigation(add_to_cart_btn, "cart"):
            print("Successfully added to cart!")
            break
        else:
            print("Failed to add product to cart. Retrying...")
    else:
        print("Product still unavailable (Coming Soon). Retrying...")
        time.sleep(random.uniform(5, 12))  # Random delay between refreshes
        if random.randint(1, 10) == 5:  # 10% chance to fully reload
            driver.get(correct_product_url)  # This will trigger an IP change (Server-side reload -- Selenium)
            print("Full Reload")
        else:
            driver.execute_script("location.reload()")  # Lighter refresh (Client-side reload -- JS)
            print("Light Refresh")

# Wait for navigation to Cart page (Best Buy auto-redirects)
print("Waiting for cart page to load...")

# Wait for the cart URL to confirm the page redirection (since Best Buy auto-redirects to cart)
WebDriverWait(driver, 20).until(
    EC.url_contains("cart")
)

print("Successfully navigated to the Cart page!")

try:
    # Extract the product name from the cart page
    product_name_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "h2.cart-item__title-heading"))
    )
    product_name = product_name_element.text.strip()
except Exception as e:
    print(f"Failed to retrieve product name: {e}")
    product_name = "Unknown Product"

# Select the radio button for shipping
print("Selecting shipping option...")
try:
    shipping_options = WebDriverWait(driver, 10).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, "input[type='radio']"))
    )
    
    if len(shipping_options) > 1:
        human_like_click(shipping_options[1])  # Click the second radio button
        print("Shipping option selected!")
        
        # Wait for any potential UI updates to settle
        time.sleep(5)  # Adjust if necessary

        # Ensure the "Checkout" button is clickable after selecting shipping
        print("Proceeding to checkout...")
        checkout_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Checkout')]"))
        )
        if click_and_confirm_navigation(checkout_btn, "checkout"):
            print("Successfully proceeded to checkout!")
        else:
            print("Failed to proceed to checkout. Retrying...")
    else:
        print("Shipping option not found!")
except Exception as e:
    print(f"Error selecting shipping or proceeding to checkout: {e}")

# Send Discord alert via Server Webhook
send_discord_alert()

# Pause for 5 minutes to allow manual intervention
print("Waiting 5 minutes before proceeding to checkout...")
time.sleep(300)  # 5-minute delay

print("Checking for CVV input field...")

try:
    # Wait for the CVV input field to be present
    cvv_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.NAME, "cvv"))
    )
    
    # If the field is found, enter the CVV number
    cvv_input.send_keys("123")  # Replace with actual CVV
    print("CVV entered successfully!")
except:
    print("CVV input field not found, proceeding without entering CVV.")

print("Attempting to place the order...")

try:
    # Try locating the button using the `data-track` attribute
    place_order_btn = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@data-track='Place your Order - In-line']"))
    )
except:
    try:
        # Fallback: Locate button using text inside the <span> tag
        place_order_btn = WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(),'Place your order')]]"))
        )
    except:
        print("Failed to locate the 'Place Your Order' button.")

if click_and_confirm_navigation(place_order_btn, "orderConfirmation"):
    print("Order placed successfully!")
else:
    print("Order placement failed. Retrying...")

# Keep browser open for debugging
input("Press Enter to exit...")
driver.quit()
