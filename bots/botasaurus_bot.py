# Both SUCCESS




# from botasaurus.browser import Driver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC

# # Just replace your driver initialization
# driver = Driver(
#     # Optional: use real Chrome profile for better fingerprint
#     # user_data_dir="/path/to/profile",
    
#     # Optional: add proxy
#     # proxy="http://username:password@proxy:port"
# )

# try:
#     # driver.sleep(5)
#     driver.get("https://pixelscan.net/bot-check")
#     driver.sleep(5)

#     driver.get("https://pixelscan.net/bot-check")
#     driver.sleep(5)

  
#     # ALL your existing Selenium code works identically
#     # wait = WebDriverWait(driver, 10)
#     # element = driver.find_element(By.CSS_SELECTOR, "button")
#     # element.click()
    
#     # driver.save_screenshot("result.png")
    
# finally:
#     driver.close()







from botasaurus.browser import Driver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

def advanced_scraping():
    # Create driver with options
    driver = Driver(
        # reuse_driver=True,  # Reuse same browser instance
        block_images=False,  # Load images
        # proxy="http://proxy:port",  # Optional proxy
        # user_data_dir="/path/to/profile"  # Use real profile
    )
    
    try:
        # Test on pixelscan
        driver.get("https://pixelscan.net/bot-check")
        driver.sleep(5)
        driver.save_screenshot("pixelscan_result.png")
        
        # Navigate to target
        driver.get("https://example.com")
        
        # Use WebDriverWait
        wait = WebDriverWait(driver, 10)
        element = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "h1"))
        )
        
        print(f"Title: {element.text}")
        
        # All Selenium methods work
        # driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        # driver.find_elements(By.CLASS_NAME, "item")
        
        return "Success"
        
    except Exception as e:
        print(f"Error: {e}")
        driver.save_screenshot("error.png")
        
    finally:
        driver.close()

advanced_scraping()