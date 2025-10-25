from selenium import webdriver
from selenium_stealth import stealth
import undetected_chromedriver as uc

driver = uc.Chrome()

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win32",
    webgl_vendor="Intel Inc.",
    renderer="Intel Iris OpenGL Engine",
    fix_hairline=True,
)

driver.get("https://pixelscan.net/bot-check")

# Your existing code works here
driver.quit()