from camoufox.sync_api import Camoufox

with Camoufox(headless=False) as browser:
    page = browser.new_page()
    page.goto("https://pixelscan.net/bot-check")
    page.wait_for_timeout(5000)
