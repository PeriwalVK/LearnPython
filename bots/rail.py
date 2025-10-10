from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time

class IRCTCAutomationDemo:
    """
    Educational demo to understand web automation concepts
    This will help you understand the workflow, even though
    it won't complete due to CAPTCHA and anti-bot measures
    """
    
    def __init__(self):
        # Setup Chrome driver
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')  # Run without GUI
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options
        )
        self.wait = WebDriverWait(self.driver, 15)
        self.driver.maximize_window()
    
    def navigate_to_irctc(self):
        """Step 1: Navigate to IRCTC"""
        print("📍 Navigating to IRCTC...")
        self.driver.get("https://www.irctc.co.in/nget/train-search")
        time.sleep(3)
        print("✅ Page loaded")
    
    def close_popups(self):
        """Step 2: Close any popups"""
        print("🔍 Checking for popups...")
        try:
            # Often there's a popup when you first visit
            close_button = self.wait.until(
                EC.element_to_be_clickable((By.CLASS_NAME, "close"))
            )
            close_button.click()
            print("✅ Popup closed")
        except:
            print("ℹ️ No popup found or already closed")
    
    def attempt_login(self, username, password):
        """
        Step 3: Attempt login (will fail at CAPTCHA)
        This demonstrates the process
        """
        print("\n🔐 Attempting login process...")
        try:
            # Click on login link
            login_link = self.wait.until(
                EC.element_to_be_clickable((By.LINK_TEXT, "LOGIN"))
            )
            login_link.click()
            time.sleep(2)
            
            # Enter username
            username_field = self.wait.until(
                EC.presence_of_element_located((By.ID, "userId"))
            )
            username_field.clear()
            username_field.send_keys(username)
            print(f"✅ Username entered: {username}")
            
            # Enter password
            password_field = self.driver.find_element(By.ID, "pwd")
            password_field.clear()
            password_field.send_keys(password)
            print("✅ Password entered")
            
            # Here's where CAPTCHA stops us
            print("\n⚠️ CAPTCHA detected - Manual intervention required")
            print("This is where automation stops on real IRCTC")
            input("Press Enter after you manually solve CAPTCHA...")
            
            # Click login
            login_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'SIGN IN')]")
            login_button.click()
            time.sleep(3)
            print("✅ Login button clicked")
            
        except Exception as e:
            print(f"❌ Error during login: {e}")
    
    def search_trains(self, from_station, to_station, journey_date):
        """
        Step 4: Search for trains
        This part might work as it's public information
        """
        print(f"\n🔍 Searching trains from {from_station} to {to_station}...")
        try:
            # From station
            from_input = self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//input[@placeholder='From*']"))
            )
            from_input.click()
            from_input.send_keys(from_station)
            time.sleep(1)
            from_input.send_keys(Keys.ARROW_DOWN)
            from_input.send_keys(Keys.ENTER)
            print(f"✅ From station: {from_station}")
            
            # To station
            to_input = self.driver.find_element(By.XPATH, "//input[@placeholder='To*']")
            to_input.click()
            to_input.send_keys(to_station)
            time.sleep(1)
            to_input.send_keys(Keys.ARROW_DOWN)
            to_input.send_keys(Keys.ENTER)
            print(f"✅ To station: {to_station}")
            
            # Date selection
            date_input = self.driver.find_element(By.XPATH, "//input[@placeholder='Journey Date(DD-MM-YYYY)*']")
            date_input.click()
            # You'd need to navigate the date picker here
            print(f"ℹ️ Date picker opened for: {journey_date}")
            
            # Search button
            time.sleep(2)
            search_button = self.driver.find_element(By.XPATH, "//button[contains(text(),'Search')]")
            search_button.click()
            print("✅ Search initiated")
            
            time.sleep(5)
            
        except Exception as e:
            print(f"❌ Error during search: {e}")
    
    def check_availability(self):
        """
        Step 5: Check seat availability
        """
        print("\n💺 Checking seat availability...")
        try:
            # Wait for results to load
            train_list = self.wait.until(
                EC.presence_of_all_elements_located((By.CLASS_NAME, "train-heading"))
            )
            
            print(f"✅ Found {len(train_list)} trains")
            
            # Check availability for each train
            availability_buttons = self.driver.find_elements(
                By.XPATH, 
                "//button[contains(text(),'Check Availability')]"
            )
            
            if availability_buttons:
                print(f"Found {len(availability_buttons)} trains to check")
                availability_buttons[0].click()  # Check first train
                time.sleep(2)
                print("✅ Availability checked for first train")
            
        except Exception as e:
            print(f"❌ Error checking availability: {e}")
    
    def book_ticket(self, passenger_details):
        """
        Step 6: Book ticket (won't work without login)
        This is just to show the flow
        """
        print("\n🎫 Attempting to book ticket...")
        print("⚠️ This requires authentication and will fail")
        try:
            # Click book now
            book_button = self.driver.find_element(
                By.XPATH, 
                "//button[contains(text(),'Book Now')]"
            )
            book_button.click()
            time.sleep(3)
            
            # Fill passenger details (pseudocode)
            print("📝 Would fill passenger details here:")
            for i, passenger in enumerate(passenger_details):
                print(f"   Passenger {i+1}: {passenger['name']}, Age: {passenger['age']}")
            
            print("⚠️ Payment gateway would appear here")
            
        except Exception as e:
            print(f"❌ Error during booking: {e}")
    
    def inspect_page_structure(self):
        """
        Utility: Inspect page structure for learning
        """
        print("\n🔎 Page Structure Analysis:")
        print(f"Title: {self.driver.title}")
        print(f"URL: {self.driver.current_url}")
        
        # Find all input fields
        inputs = self.driver.find_elements(By.TAG_NAME, "input")
        print(f"\n📋 Found {len(inputs)} input fields:")
        for inp in inputs[:5]:  # Show first 5
            print(f"  - Type: {inp.get_attribute('type')}, "
                  f"Placeholder: {inp.get_attribute('placeholder')}, "
                  f"ID: {inp.get_attribute('id')}")
    
    def close(self):
        """Close the browser"""
        print("\n👋 Closing browser...")
        input("Press Enter to close...")
        self.driver.quit()


# ============================================
# MAIN DEMO
# ============================================
def main():
    print("="*60)
    print("🎓 IRCTC Web Automation Educational Demo")
    print("="*60)
    print("Purpose: Learn how web automation works")
    print("Note: Will stop at CAPTCHA and authentication barriers")
    print("="*60)
    
    bot = IRCTCAutomationDemo()
    
    try:
        # Demo workflow
        bot.navigate_to_irctc()
        bot.close_popups()
        bot.inspect_page_structure()
        
        # Uncomment to try login (you'll need to solve CAPTCHA manually)
        bot.attempt_login("your_username", "your_password")
        
        # Search for trains (this might work as it's public)
        bot.search_trains("NDLS", "BCT", "15-12-2024")  # Delhi to Mumbai
        bot.check_availability()
        
        # Booking demo (won't actually work)
        passenger_info = [
            {"name": "John Doe", "age": 30, "gender": "M"},
            {"name": "Jane Doe", "age": 28, "gender": "F"}
        ]
        # bot.book_ticket(passenger_info)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    finally:
        bot.close()


if __name__ == "__main__":
    main()