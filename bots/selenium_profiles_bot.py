# from selenium_profiles.webdriver import Chrome
# from selenium_profiles.profiles import profiles
# from selenium.webdriver.common.by import By

# # Create realistic profile
# profile = profiles.Windows(
#     # Optional customizations
#     # language="en-US",
#     # proxy="http://proxy:port"
# )

# driver = Chrome(profile=profile)

# # Use exactly like Selenium
# driver.get("https://pixelscan.net/bot-check")
# driver.implicitly_wait(10)

# # Your existing code works
# element = driver.find_element(By.CSS_SELECTOR, "h1")
# print(element.text)

# driver.quit()