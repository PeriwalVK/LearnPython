import time
import datetime as dt
import traceback
import undetected_chromedriver as uc
import json
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from selenium import webdriver

from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import TimeoutException, WebDriverException

from webdriver_manager.chrome import ChromeDriverManager
from constants.driver_configuration import WAIT_TIMES
from constants.website_constants import DATE, QUOTA, STATIONS, JOURNEY_CLASS, URLS


# WAIT_SECONDS = 15  # seconds


def get_trip_details_from_json(file_path="trip_details.json"):
    """
    Reads trip details from a JSON file.
    Expected format in trip_details.json:
    {
        "FROM_STATION": "NDLS",
        "TO_STATION": "BCT",
        "JOURNEY_DATE": "25-12-2024"
    }
    """
    try:
        # with open(file_path, 'r') as f:
        #     data = json.load(f)
        data = {
            "FROM_STATION": "BIKANER JN - BKN (BIKANER)",
            "TO_STATION": "BCT",
            "JOURNEY_DATE": "25-12-2024",
        }
        from_station = data.get("FROM_STATION")
        to_station = data.get("TO_STATION")
        journey_date = data.get("JOURNEY_DATE")

        # Basic validation
        if not all([from_station, to_station, journey_date]):
            raise ValueError(
                "Missing one or more required fields (FROM_STATION, TO_STATION, JOURNEY_DATE) in JSON."
            )
        dt.datetime.strptime(journey_date, "%d-%m-%Y")  # Validate date format
        return from_station.strip(), to_station.strip(), journey_date.strip()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"Error: '{file_path}' not found. Please create it with trip details."
        )
    except (json.JSONDecodeError, ValueError) as e:
        raise ValueError(f"Error reading or validating JSON file: {e}")


class InteractiveIRCTCHelper:
    """
    An interactive helper using undetected-chromedriver to pre-fill the IRCTC form.
    It prompts the user for trip details before launching the browser.
    """

    def __init__(
        self,
        headless=False,
        detectable=False,
        eager=False,
        url=None,
        wait_seconds=WAIT_TIMES.DRIVER_DEFAULT,
    ):
        """Initializes the browser using undetected_chromedriver."""

        self.driver = self._initialise_driver(
            headless=headless, detectable=detectable, eager=eager
        )
        self.wait_seconds = wait_seconds
        self.wait = WebDriverWait(self.driver, wait_seconds)
        self.direct_url = url if url else URLS.IRCTC_HOME

    def _initialise_driver(self, headless: bool, detectable: bool, eager: bool):
        print(
            f"🚀 Initializing {"detectable" if detectable else "undetectable"}{" and headless" if headless else ""} browser..."
        )

        if detectable:
            options = webdriver.ChromeOptions()
            if headless:
                options.add_argument("--headless")  # Run without GUI
            options.add_argument("--disable-blink-features=AutomationControlled")
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option("useAutomationExtension", False)
            if eager:
                options.page_load_strategy = "eager"

            driver = webdriver.Chrome(
                service=Service(ChromeDriverManager().install()), options=options
            )
        else:
            options = uc.ChromeOptions()
            if headless:
                options.add_argument("--headless")
            if eager:
                options.page_load_strategy = "eager"

            # options.add_argument("start-maximized")
            driver = uc.Chrome(
                use_subprocess=False,
                options=options,
            )

        print("🖥️ Maximizing browser window...")
        driver.maximize_window()

        return driver

    def go_to_url(self, url=None):
        print(f"\n🌍 Navigating to: {url if url else self.direct_url}")
        self.driver.get(url if url else self.direct_url)
        self.driver.save_screenshot("./screenshots/url_screenshot.png")

    def handle_popups(self):
        # --- Handle the initial welcome alert/popup ---
        try:
            print("🔍 Checking for initial alert popup...")
            ok_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(text(), 'OK')]")
                )
            )
            ok_button.click()
            print("✅ Alert popup handled.")
        except TimeoutException:
            print("ℹ️ No initial alert popup appeared. Continuing...")
        finally:
            self.driver.save_screenshot("./screenshots/url_screenshot_after_popup.png")

    def _select_from_to_autocomplete(self, formcontrolname, search_text, option_text):
        """
        Select an option from a PrimeNG autocomplete field.
        - formcontrolname: 'origin' or 'destination'
        - search_text: text to type into input to trigger suggestions
        - option_text: exact option to click from the list
        """
        # Locate the autocomplete input
        print(f"➡️ Filling {formcontrolname} station: {search_text}")
        auto_input = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//p-autocomplete[@formcontrolname='{formcontrolname}']//input[@role='searchbox']",
                )
            )
        )

        # Type the text
        auto_input.clear()
        auto_input.send_keys(search_text)

        # Wait for the options panel
        options_panel = self.wait.until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    f"//p-autocomplete[@formcontrolname='{formcontrolname}']//ul[contains(@class,'ui-autocomplete-items')]",
                )
            )
        )

        # # Get all options inside this panel
        # options = options_panel.find_elements(
        #     By.XPATH, ".//li[contains(@class,'ui-autocomplete-list-item')]"
        # )
        # # Click the option that matches
        # for opt in options:
        #     if option_text in opt.text:
        #         opt.click()
        #         break
        option = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//p-autocomplete[@formcontrolname='{formcontrolname}']//li//span[contains(text(),'{option_text}')]",
                )
            )
        )
        option.click()

        time.sleep(1.5)

    def _select_calendar_date(self, date_str):
        """
        Select a date from PrimeNG calendar.
        date_str = 'DD/MM/YYYY'
        """
        print(f"📅 Filling date: {date_str}")

        day, month, year = map(int, date_str.split("/"))
        target_date = dt.datetime(year, month, day)

        # 1. Click on the calendar input to open the popup
        calendar_input = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//p-calendar[@formcontrolname='journeyDate']//input")
            )
        )
        calendar_input.click()
        time.sleep(0.5)

        # 2. Wait for the calendar popup
        calendar_panel = self.wait.until(
            EC.visibility_of_element_located(
                (By.XPATH, "//div[contains(@class,'ui-datepicker')]")
            )
        )

        while True:
            # 3. Get current month and year from calendar
            current_month_text = calendar_panel.find_element(
                By.XPATH, ".//span[contains(@class,'ui-datepicker-month')]"
            ).text
            current_year_text = calendar_panel.find_element(
                By.XPATH, ".//span[contains(@class,'ui-datepicker-year')]"
            ).text

            current_month = dt.datetime.strptime(current_month_text, "%B").month
            current_year = int(current_year_text)

            # 4. Check if we are on the correct month/year
            if current_year == year and current_month == month:
                break  # correct month/year reached

            # 5. Decide whether to click prev or next
            if (current_year, current_month) > (year, month):
                # prev_btn = calendar_panel.find_element(By.XPATH, ".//a[contains(@class,'ui-datepicker-prev')]")
                prev_btn = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, ".//a[contains(@class,'ui-datepicker-prev')]")
                    )
                )

                prev_btn.click()
                time.sleep(0.5)
            else:
                # next_btn = calendar_panel.find_element(By.XPATH, ".//a[contains(@class,'ui-datepicker-next')]")
                next_btn = self.wait.until(
                    EC.element_to_be_clickable(
                        (By.XPATH, ".//a[contains(@class,'ui-datepicker-next')]")
                    )
                )
                next_btn.click()
                time.sleep(0.5)

            # time.sleep(0.5)  # small wait for table to update

        # 6. Click the day
        day_elem = calendar_panel.find_element(By.XPATH, f".//a[text()='{day}']")
        day_elem.click()
        time.sleep(0.5)

    def _select_journey_class(self, journey_class):
        # 1. Click the label container to open the dropdown

        dropdown_label = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//p-dropdown[@formcontrolname='journeyClass']//div[contains(@class,'ui-dropdown-label-container')]",
                )
            )
        )
        dropdown_label.click()
        time.sleep(0.5)

        # 2. Wait for the options panel to appear
        options_panel = WebDriverWait(dropdown_label, self.wait_seconds).until(
            EC.visibility_of_element_located(
                (
                    By.XPATH,
                    "//div[contains(@class,'ui-dropdown-panel') and contains(@class,'ng-trigger')]",
                )
            )
        )

        # 3. Find and click the target option with a local wait
        option = WebDriverWait(options_panel, self.wait_seconds).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f".//li/span[contains(normalize-space(text()), '{journey_class}')]",
                )
            )
        )
        option.click()
        time.sleep(0.5)  # small pause for UI stability

    def _select_quota(self, quota):
        print(f"📅 Filling Quota: {quota}")

        dropdown = self.wait.until(
            EC.element_to_be_clickable(
                (By.XPATH, "//p-dropdown[@formcontrolname='journeyQuota']")
            )
        )
        dropdown.click()
        option = self.wait.until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    f"//p-dropdown[@formcontrolname='journeyQuota']//li//span[text()='{quota}']",
                )
            )
        )
        option.click()
        time.sleep(1.5)

    def setup_search_form(self, from_stn, to_stn, date_str, journey_class, quota):
        """
        Navigates to IRCTC, closes popups, and fills the search form
        with the details provided by the user.
        """

        # --- Step 2: Fill the form with user input ---
        try:

            self._select_from_to_autocomplete(
                formcontrolname="origin", search_text="BIKANER", option_text="BIKANER"
            )
            self._select_from_to_autocomplete(
                formcontrolname="destination", search_text="SURAT", option_text="SURAT"
            )
            self._select_calendar_date(date_str)
            self._select_journey_class(journey_class)
            self._select_quota(quota)

            self.driver.find_element(
                By.TAG_NAME, "body"
            ).click()  # Click away to close calendar

            print("\n" + "=" * 50)
            print("✅✅✅ FORM IS READY FOR YOU! ✅✅✅")
            print("The browser window is now under your control.")
            print("Please Login, solve CAPTCHA, and click 'Search'.")
            print("=" * 50)

        except Exception as e:
            print(f"\n❌ An error occurred while filling the form: {e}")
            print(
                "Please check the station codes you entered and ensure the page loaded correctly."
            )
            # e.traceback()
            print("Full Traceback:")
            traceback.print_exc()


    def submit_search_form(self):
        # Absolute XPath of the Search button
        search_button_xpath = "/html/body/app-root/app-home/div[3]/div/app-main-page/div/div/div[1]/div[1]/div[1]/app-jp-input/div/form/div[5]/div[1]/button"

        # Wait up to 15 seconds for the button to be clickable
        search_btn = self.wait.until(
            EC.element_to_be_clickable((By.XPATH, search_button_xpath))
        )

        # Click the button
        search_btn.click()
        time.sleep(1.5)
        print("✅ Search button clicked successfully.")

    def graceful_shutdown(self):
        """Attempts to quit the driver, but handles errors if it's already closed."""

        input(
            "\nThis script has finished its task. The browser is yours.\nPress Enter in this terminal to close this message when you are done.\n"
        )

        if self.driver:
            print("\n🧹 Performing graceful shutdown...")
            try:
                self.driver.quit()
                # time.sleep(10)
                print("✅ Browser closed successfully.")

            except (OSError, WebDriverException) as e:
                print("ℹ️ Browser was already closed by the user.")

        print("Program Ended")

    def execute(self):
        bot.go_to_url()
        bot.handle_popups()
        bot.setup_search_form(
            STATIONS.BKN,
            STATIONS.ST,
            DATE.JOURNEY_DATE,
            JOURNEY_CLASS.SLEEPER,
            QUOTA.TATKAL,
        )
        bot.submit_search_form()


# --- Main Execution Block ---
if __name__ == "__main__":

    url = None

    # url = "https://www.hapag-lloyd.com/en/home.html"
    # url = "https://bot.sannysoft.com/"
    # url = "https://www.browserscan.net/bot-detection"
    # url = "https://www.google.com"

    # # 1. Get trip details from a JSON file
    # from_stn, to_stn, date_str = get_trip_details_from_json()

    # 2. Launch the bot and set up the form
    bot = InteractiveIRCTCHelper(headless=False, detectable=False, eager=True, url=url)
    # bot = InteractiveIRCTCHelper(headless=False, detectable=False, eager=True, url=url); bot.go_to_url()

    bot.execute()



    # 3. The script will leave the browser open for the user.
    bot.graceful_shutdown()
