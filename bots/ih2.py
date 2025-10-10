import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from webdriver_manager.chrome import ChromeDriverManager

# ==================================================================
# <<<---  CONFIGURE YOUR TRIP DETAILS HERE  ---<<<
# ==================================================================
# Use station codes for best results (e.g., 'NDLS' for New Delhi, 'BCT' for Mumbai Central)
FROM_STATION = "ST"
TO_STATION = "BKN"
# Format: DD-MM-YYYY
JOURNEY_DATE = "25-11-2025"
# ==================================================================


class IRCTCHelper:
    """
    A helper script to speed up manual IRCTC booking on slow internet.
    It pre-fills the search form and then hands over control to the user.
    """

    def __init__(self):
        """Initializes the browser."""
        print("🚀 Initializing browser...")
        # These options help the browser appear more like a regular user's browser
        options = webdriver.ChromeOptions()
        options.add_argument("start-maximized")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option("useAutomationExtension", False)

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )
        self.wait = WebDriverWait(self.driver, 10)

    def setup_search_form(self, from_stn, to_stn, date_str):
        """
        Navigates to IRCTC, closes popups, and fills the search form.
        """
        direct_url = "https://www.irctc.co.in/nget/train-search"
        print(f"🌍 Navigating directly to: {direct_url}")
        self.driver.get(direct_url)

        # --- Step 1: Handle the initial welcome alert/popup ---
        try:
            print("🔍 Checking for initial alert popup...")
            # IRCTC often has a welcome alert with an OK button. We wait for it and click it.
            ok_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'OK')]")
                )
            )
            ok_button.click()
            print("✅ 'OK' button on the alert was clicked.")
        except TimeoutException:
            print("ℹ️ No initial alert popup appeared, which is fine. Continuing...")

        # --- Step 2: Fill the 'From' station ---
        try:
            print(f"➡️ Filling 'From' station: {from_stn}")
            from_field = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[contains(@aria-controls, 'pr_id_1_list')]")
                )
            )
            from_field.send_keys(from_stn)
            time.sleep(1)  # Wait for autocomplete suggestions to appear
            # Select the first suggestion from the dropdown
            first_suggestion = self.wait.until(
                EC.element_to_be_clickable((By.ID, "pr_id_1_list_0"))
            )
            first_suggestion.click()

            # --- Step 3: Fill the 'To' station ---
            print(f"➡️ Filling 'To' station: {to_stn}")
            to_field = self.wait.until(
                EC.visibility_of_element_located(
                    (By.XPATH, "//input[contains(@aria-controls, 'pr_id_2_list')]")
                )
            )
            to_field.send_keys(to_stn)
            time.sleep(1)  # Wait for autocomplete
            # Select the first suggestion from the dropdown
            first_suggestion_to = self.wait.until(
                EC.element_to_be_clickable((By.ID, "pr_id_2_list_0"))
            )
            first_suggestion_to.click()

            # --- Step 4: Fill the Journey Date ---
            print(f"📅 Filling date: {date_str}")
            date_field = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//input[contains(@class, 'ng-tns-c58-8')]")
                )
            )
            date_field.click()  # Click to open calendar
            date_field.clear()  # Clear any default value
            date_field.send_keys(date_str)
            self.driver.find_element(
                By.TAG_NAME, "body"
            ).click()  # Click away to close calendar

            print("\n" + "=" * 50)
            print("✅✅✅ FORM IS READY! ✅✅✅")
            print("Your turn! Please Login, solve CAPTCHA, and click 'Search'.")
            print("=" * 50)

        except Exception as e:
            print(f"\n❌ An error occurred while filling the form: {e}")
            print("Please check your station codes and date format.")

    def close_browser(self):
        """Closes the browser window."""
        self.driver.quit()


# --- Main Execution Block ---
if __name__ == "__main__":
    bot = IRCTCHelper()
    bot.setup_search_form(FROM_STATION, TO_STATION, JOURNEY_DATE)

    # The script will leave the browser open for you.
    # When you are completely done with your booking and have closed the browser window,
    # you can come back to this terminal and press Enter to end the script.
    input(
        "\nPress Enter in this terminal to formally end the script when you're done.\n"
    )
