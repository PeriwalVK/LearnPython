#!/usr/bin/env python3
"""
Comprehensive Python datetime Library Tutorial
=============================================

This tutorial covers all important concepts in Python's datetime library,
including datetime, date, time, timedelta, timezone handling, and practical applications.

Author: Claude
Date: October 2025
"""

import datetime as dt
# from datetime import date, time, datetime as dt, timedelta, timezone
import calendar
import time
from zoneinfo import ZoneInfo  # Python 3.9+
import pytz  # Third-party library for timezone handling (older Python versions)


def separator(title):
    """Helper function to create section separators"""
    print(f"\n\n{'='*60}")
    print(f" {title.upper()}")
    print("=" * 60)


def _1_basic_date_and_time_objects():
    # =================================================================
    # 1. BASIC DATE AND TIME OBJECTS
    # =================================================================
    separator("Basic Date and Time Objects")

    # Creating date objects
    print("\n1. DATE OBJECTS:")
    today = dt.date.today()
    specific_date = dt.date(2025, 12, 25)  # Christmas 2025

    print(f"Today's date: {today}")
    print(f"Specific date: {specific_date}")
    print(
        f"Date components - Year: {today.year}, Month: {today.month}, Day: {today.day}"
    )

    # Creating time objects
    print("\n2. TIME OBJECTS:")
    current_time = time.localtime()
    specific_time = time(14, 30, 45, 123456)  # 2:30:45.123456 PM
    midnight = time()  # Default: 00:00:00

    print(f"Specific time: {specific_time}")
    print(f"Midnight: {midnight}")
    print(
        f"Time components - Hour: {specific_time.hour}, Minute: {specific_time.minute}"
    )
    print(f"Seconds: {specific_time.second}, Microseconds: {specific_time.microsecond}")

    # Creating datetime objects
    print("3. DATETIME OBJECTS:")
    now = dt.now()
    specific_datetime = dt(2025, 12, 25, 14, 30, 45)

    print(f"Current datetime: {now}")
    print(f"Specific datetime: {specific_datetime}")
    print(f"Date part: {now.date()}")
    print(f"Time part: {now.time()}")


def _2_creating_datetime_objects():
    # =================================================================
    # 2. CREATING DATETIME OBJECTS
    # =================================================================
    separator("Creating Datetime Objects")

    print("1. DIFFERENT WAYS TO CREATE DATETIME OBJECTS:")

    # From components
    dt1 = dt(2025, 10, 13, 23, 4, 30)
    print(f"From components: {dt1}")

    # Current date and time
    dt2 = dt.now()
    dt3 = dt.today()
    dt4 = dt.utcnow()  # UTC time

    print(f"dt.now(): {dt2}")
    print(f"dt.today(): {dt3}")
    print(f"dt.utcnow(): {dt4}")

    # From timestamp
    timestamp = 1697238270  # Unix timestamp
    dt5 = dt.fromtimestamp(timestamp)
    print(f"From timestamp: {dt5}")

    # From ISO format string
    iso_string = "2025-10-13T23:04:30"
    dt6 = dt.fromisoformat(iso_string)
    print(f"From ISO string: {dt6}")

    # Combining date and time objects
    my_date = date(2025, 10, 13)
    my_time = time(23, 4, 30)
    dt7 = dt.combine(my_date, my_time)
    print(f"Combined date and time: {dt7}")


def _3_formatting_and_parsing():
    # =================================================================
    # 3. FORMATTING AND PARSING
    # =================================================================
    separator("Formatting and Parsing")

    print("1. FORMATTING DATETIME TO STRING:")
    now = dt.now()

    # Common format codes
    formats = {
        "%Y-%m-%d": "YYYY-MM-DD",
        "%d/%m/%Y": "DD/MM/YYYY",
        "%B %d, %Y": "Month DD, YYYY",
        "%A, %B %d, %Y": "Weekday, Month DD, YYYY",
        "%Y-%m-%d %H:%M:%S": "YYYY-MM-DD HH:MM:SS",
        "%I:%M %p": "12-hour format with AM/PM",
        "%H:%M:%S": "24-hour format",
        "%c": "Complete date and time",
        "%x": "Date only (locale specific)",
        "%X": "Time only (locale specific)",
    }

    for format_code, description in formats.items():
        formatted = now.strftime(format_code)
        print(f"{format_code:20} ({description:25}): {formatted}")

    print("2. PARSING STRING TO DATETIME:")
    date_strings = [
        ("2025-10-13", "%Y-%m-%d"),
        ("13/10/2025", "%d/%m/%Y"),
        ("October 13, 2025", "%B %d, %Y"),
        ("2025-10-13 23:04:30", "%Y-%m-%d %H:%M:%S"),
        ("Sun Oct 13 23:04:30 2025", "%a %b %d %H:%M:%S %Y"),
    ]

    for date_string, format_string in date_strings:
        try:
            parsed_date = dt.strptime(date_string, format_string)
            print(f"'{date_string}' -> {parsed_date}")
        except ValueError as e:
            print(f"Error parsing '{date_string}': {e}")


def _4_timedelta():
    # =================================================================
    # 4. TIMEDELTA - TIME DIFFERENCES
    # =================================================================
    separator("Timedelta - Working with Time Differences")

    print("1. CREATING TIMEDELTA OBJECTS:")

    # Different ways to create timedelta
    td1 = timedelta(days=7)
    td2 = timedelta(hours=24)
    td3 = timedelta(weeks=2, days=3, hours=4, minutes=30, seconds=45)
    td4 = timedelta(milliseconds=500, microseconds=123)

    print(f"7 days: {td1}")
    print(f"24 hours: {td2}")
    print(f"Complex timedelta: {td3}")
    print(f"Sub-second precision: {td4}")

    print("2. TIMEDELTA ARITHMETIC:")
    now = dt.now()

    # Adding and subtracting timedelta
    future = now + timedelta(days=30)
    past = now - timedelta(weeks=2)

    print(f"Now: {now}")
    print(f"30 days from now: {future}")
    print(f"2 weeks ago: {past}")

    # Difference between datetime objects
    diff = future - now
    print(f"Difference: {diff}")
    print(f"Difference in days: {diff.days}")
    print(f"Total seconds: {diff.total_seconds()}")

    print("3. PRACTICAL TIMEDELTA EXAMPLES:")

    # Age calculation
    birth_date = dt(1990, 5, 15)
    age = now - birth_date
    print(f"Age: {age.days} days ({age.days // 365} years)")

    # Next Friday
    days_ahead = 4 - now.weekday()  # Friday is weekday 4
    if days_ahead <= 0:  # Target day already happened this week
        days_ahead += 7
    next_friday = now + timedelta(days=days_ahead)
    print(f"Next Friday: {next_friday.strftime('%A, %B %d, %Y')}")

    # Business days calculation (excluding weekends)
    def add_business_days(start_date, business_days):
        current_date = start_date
        while business_days > 0:
            current_date += timedelta(days=1)
            if current_date.weekday() < 5:  # Monday = 0, Sunday = 6
                business_days -= 1
        return current_date

    business_date = add_business_days(now, 10)
    print(f"10 business days from now: {business_date.strftime('%A, %B %d, %Y')}")


def _5_timezone_handling():
    # =================================================================
    # 5. TIMEZONE HANDLING
    # =================================================================
    separator("Timezone Handling")

    print("1. TIMEZONE-AWARE VS TIMEZONE-NAIVE:")

    # Naive datetime (no timezone info)
    naive_dt = dt.now()
    print(f"Naive datetime: {naive_dt}")
    print(f"Timezone info: {naive_dt.tzinfo}")

    # Timezone-aware datetime
    utc_dt = dt.now(timezone.utc)
    print(f"UTC datetime: {utc_dt}")
    print(f"Timezone info: {utc_dt.tzinfo}")

    print("2. WORKING WITH DIFFERENT TIMEZONES:")

    # Using timezone.utc
    utc_now = dt.now(timezone.utc)
    print(f"UTC: {utc_now}")

    # Using fixed offset
    est = timezone(timedelta(hours=-5))  # Eastern Standard Time
    est_now = dt.now(est)
    print(f"EST: {est_now}")

    # Using zoneinfo (Python 3.9+)
    try:
        ny_tz = ZoneInfo("America/New_York")
        tokyo_tz = ZoneInfo("Asia/Tokyo")
        london_tz = ZoneInfo("Europe/London")

        ny_time = dt.now(ny_tz)
        tokyo_time = dt.now(tokyo_tz)
        london_time = dt.now(london_tz)

        print(f"New York: {ny_time}")
        print(f"Tokyo: {tokyo_time}")
        print(f"London: {london_time}")

    except ImportError:
        print("zoneinfo not available (Python < 3.9)")

    print("3. TIMEZONE CONVERSION:")

    # Convert UTC to local timezone
    utc_dt = dt.now(timezone.utc)
    local_dt = utc_dt.astimezone()
    print(f"UTC: {utc_dt}")
    print(f"Local: {local_dt}")

    # Convert between timezones
    try:
        ny_time = dt.now(ZoneInfo("America/New_York"))
        tokyo_time = ny_time.astimezone(ZoneInfo("Asia/Tokyo"))
        print(f"NY time: {ny_time}")
        print(f"Same moment in Tokyo: {tokyo_time}")
    except:
        print("Timezone conversion example requires Python 3.9+")


def _6_calender_operations():
    # =================================================================
    # 6. CALENDAR OPERATIONS
    # =================================================================
    separator("Calendar Operations")

    print("1. CALENDAR MODULE:")

    # Calendar information
    print(f"Is 2024 a leap year? {calendar.isleap(2024)}")
    print(f"Days in February 2024: {calendar.monthrange(2024, 2)[1]}")

    # Weekday operations
    today = date.today()
    print(f"Today is: {calendar.day_name[today.weekday()]}")
    print(f"Month: {calendar.month_name[today.month]}")

    # First and last day of month
    year, month = today.year, today.month
    first_day = date(year, month, 1)
    last_day = date(year, month, calendar.monthrange(year, month)[1])
    print(f"First day of month: {first_day}")
    print(f"Last day of month: {last_day}")

    print("2. USEFUL DATE CALCULATIONS:")

    # First Monday of the month
    first_of_month = date(today.year, today.month, 1)
    days_until_monday = (7 - first_of_month.weekday()) % 7
    first_monday = first_of_month + timedelta(days=days_until_monday)
    print(f"First Monday of the month: {first_monday}")

    # Last Friday of the month
    last_of_month = date(
        today.year, today.month, calendar.monthrange(today.year, today.month)[1]
    )
    days_back_to_friday = (last_of_month.weekday() - 4) % 7
    last_friday = last_of_month - timedelta(days=days_back_to_friday)
    print(f"Last Friday of the month: {last_friday}")


def _7_performance_and_best_practices():
    # =================================================================
    # 7. PERFORMANCE AND BEST PRACTICES
    # =================================================================
    separator("Performance and Best Practices")

    print("1. PERFORMANCE CONSIDERATIONS:")

    # Measuring execution time
    start_time = time.perf_counter()

    # Some datetime operations
    dates = []
    for i in range(1000):
        dates.append(dt.now())

    end_time = time.perf_counter()
    print(f"Creating 1000 datetime objects took: {end_time - start_time:.6f} seconds")

    print("2. BEST PRACTICES:")
    best_practices = [
        "Always use timezone-aware datetimes for applications dealing with multiple timezones",
        "Store datetimes in UTC in databases and convert to local time for display",
        "Use timedelta for time arithmetic instead of manual calculations",
        "Be careful with daylight saving time transitions",
        "Use ISO format for string representations when possible",
        "Consider using libraries like pendulum or arrow for complex datetime operations",
        "Cache timezone objects instead of creating them repeatedly",
        "Use date objects for date-only operations to save memory",
    ]

    for i, practice in enumerate(best_practices, 1):
        print(f"{i}. {practice}")


def _8_common_datetime_patterns_and_recipes():
    # =================================================================
    # 8. COMMON DATETIME PATTERNS AND RECIPES
    # =================================================================
    separator("Common Patterns and Recipes")

    print("1. COMMON DATETIME RECIPES:")

    # Get start and end of day
    now = dt.now()
    start_of_day = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_day = now.replace(hour=23, minute=59, second=59, microsecond=999999)

    print(f"Start of day: {start_of_day}")
    print(f"End of day: {end_of_day}")

    # Get start and end of week
    start_of_week = now - timedelta(days=now.weekday())
    start_of_week = start_of_week.replace(hour=0, minute=0, second=0, microsecond=0)
    end_of_week = start_of_week + timedelta(
        days=6, hours=23, minutes=59, seconds=59, microseconds=999999
    )

    print(f"Start of week: {start_of_week}")
    print(f"End of week: {end_of_week}")

    # Age in years, months, days
    def calculate_age(birth_date, current_date=None):
        if current_date is None:
            current_date = date.today()

        years = current_date.year - birth_date.year
        months = current_date.month - birth_date.month
        days = current_date.day - birth_date.day

        if days < 0:
            months -= 1
            days += calendar.monthrange(current_date.year, current_date.month - 1)[1]

        if months < 0:
            years -= 1
            months += 12

        return years, months, days

    birth = date(1990, 3, 15)
    years, months, days = calculate_age(birth)
    print(f"Age: {years} years, {months} months, {days} days")

    # Working with quarters
    def get_quarter(date_obj):
        return (date_obj.month - 1) // 3 + 1

    def get_quarter_start(year, quarter):
        month = (quarter - 1) * 3 + 1
        return date(year, month, 1)

    def get_quarter_end(year, quarter):
        month = quarter * 3
        last_day = calendar.monthrange(year, month)[1]
        return date(year, month, last_day)

    today = date.today()
    current_quarter = get_quarter(today)
    quarter_start = get_quarter_start(today.year, current_quarter)
    quarter_end = get_quarter_end(today.year, current_quarter)

    print(f"Current quarter: Q{current_quarter}")
    print(f"Quarter start: {quarter_start}")
    print(f"Quarter end: {quarter_end}")


def _9_error_handling_and_edge_cases():
    # =================================================================
    # 9. ERROR HANDLING AND EDGE CASES
    # =================================================================
    separator("Error Handling and Edge Cases")

    print("1. COMMON ERRORS AND HOW TO HANDLE THEM:")

    # Invalid date
    try:
        invalid_date = date(2025, 2, 30)  # February doesn't have 30 days
    except ValueError as e:
        print(f"Invalid date error: {e}")

    # Mixing naive and aware datetimes
    try:
        naive = dt.now()
        aware = dt.now(timezone.utc)
        diff = aware - naive  # This will raise TypeError
    except TypeError as e:
        print(f"Timezone mixing error: {e}")

    # Parsing errors
    try:
        parsed = dt.strptime("invalid date", "%Y-%m-%d")
    except ValueError as e:
        print(f"Parsing error: {e}")

    print("2. SAFE DATETIME OPERATIONS:")

    def safe_date_create(year, month, day):
        """Safely create a date object"""
        try:
            return date(year, month, day)
        except ValueError as e:
            print(f"Cannot create date {year}-{month}-{day}: {e}")
            return None

    def safe_datetime_parse(date_string, format_string):
        """Safely parse a datetime string"""
        try:
            return dt.strptime(date_string, format_string)
        except ValueError as e:
            print(f"Cannot parse '{date_string}': {e}")
            return None

    # Examples
    safe_date = safe_date_create(2025, 2, 29)  # Invalid leap year date
    safe_parsed = safe_datetime_parse("2025-13-01", "%Y-%m-%d")  # Invalid month


def _conclusion():
    print("=" * 60)
    print(" TUTORIAL COMPLETE")
    print("=" * 60)
    print("This tutorial covered:")
    print("• Basic date, time, and datetime objects")
    print("• Creating datetime objects in various ways")
    print("• Formatting and parsing date strings")
    print("• Working with timedelta for time arithmetic")
    print("• Timezone handling and conversion")
    print("• Calendar operations and calculations")
    print("• Performance considerations and best practices")
    print("• Common patterns and recipes")
    print("• Error handling and edge cases")

    print("For more advanced datetime operations, consider libraries like:")
    print("• pendulum - More intuitive datetime handling")
    print("• arrow - Better datetime for Python")
    print("• dateutil - Extensions to the standard datetime module")


def main():
    """Main tutorial function demonstrating all datetime concepts"""

    _1_basic_date_and_time_objects()

    # _2_creating_datetime_objects()

    # _3_formatting_and_parsing()

    # _4_timedelta()

    # _5_timezone_handling()

    # _6_calender_operations()

    # _7_performance_and_best_practices()

    # _8_common_datetime_patterns_and_recipes()

    # _9_error_handling_and_edge_cases()

    # _conclusion()


if __name__ == "__main__":
    main()
