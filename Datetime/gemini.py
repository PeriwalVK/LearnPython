# -*- coding: utf-8 -*-
"""
Python Datetime Library Tutorial

This file serves as a comprehensive tutorial for Python's built-in `datetime` module.
It covers the most important concepts and provides practical examples to help you
understand and effectively use dates and times in your Python programs.

The `datetime` module provides classes for working with dates and times.
The main classes are:

- `date`: For working with dates (year, month, day).
- `time`: For working with times (hour, minute, second, microsecond).
- `datetime`: For working with both dates and times.
- `timedelta`: For representing the difference between two dates or times.
- `tzinfo`: Abstract base class for time zone information objects.
- `timezone`: Concrete implementation of `tzinfo` for fixed offset time zones.

Let's dive into each of these.
"""

# 1. Importing the datetime module
import datetime as dt

# # from datetime import date, time, datetime, timedelta, timezone
# print("Successfully imported datetime, date, time, datetime, timedelta, and timezone.")
# print("-" * 30)


def separator(title):
    """Helper function to create section separators"""
    print(f"\n\n{'='*60}")
    print(f" {title.upper()}")
    print("=" * 60)


def _2_():

    # 2. Working with `date` objects

    separator("--- 2. Working with `date` objects ---")

    # Getting today's date
    today = dt.date.today()
    print(f"Today's date: {today}")

    # Creating a specific date
    my_birthday = dt.date(1990, 5, 15)
    print(f"My birthday: {my_birthday}")
    print(
        f"my birthday - Year: {my_birthday.year}, month: {my_birthday.month}, day: {my_birthday.day}"
    )

    # Comparing dates
    if my_birthday < today:
        print("My birthday has already passed this year.")
    elif my_birthday == today:
        print("Happy birthday to me!")
    else:
        print("My birthday is yet to come this year.")

    # Getting the weekday and day of the year
    # Monday is 0 and Sunday is 6
    print(f"Weekday of my birthday: {my_birthday.weekday()}")
    print("here Monday is 0 and Sunday is 6")
    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]
    print(f"Hence the Weekday of my birthday: {weekdays[my_birthday.weekday()]}")
    # Day of the year (1-365 or 366)
    print(f"Day of the year for 1st jan: {dt.date(2025,1,1).timetuple().tm_yday}")  # 1
    print(f"Day of the year for my birthday: {my_birthday.timetuple().tm_yday}")
    print(f"timetuple for my birthday: {my_birthday.timetuple()}")
    print("-" * 30)


def _3_():
    # 3. Working with `time` objects
    separator("--- 3. Working with `time` objects ---")

    # Creating a specific time
    meeting_time = dt.time(14, 30, 0)  # 2:30 PM
    print(f"Meeting time: {meeting_time}")

    # Creating a time with microseconds
    precise_time = dt.time(9, 15, 45, 123456)
    print(f"Precise time: {precise_time}")

    # Accessing time components
    print(
        f"meeting time - hour: {meeting_time.hour}, minute: {meeting_time.minute},"
        + f" second: {meeting_time.second}, microsecond: {meeting_time.microsecond}"
    )
    print(
        f"precise time - hour: {precise_time.hour}, minute: {precise_time.minute},"
        + f" second: {precise_time.second}, microsecond: {precise_time.microsecond}"
    )

    # Note: `time` objects do not have a `today()` method as they don't inherently
    # relate to a specific date.print("-" * 30)


def _4_():
    # 4. Working with `datetime` objects
    separator("--- 4. Working with `datetime` objects ---")

    my_birthday = dt.date(1990, 5, 15)
    meeting_time = dt.time(14, 30, 0)  # 2:30 PM

    # Getting the current date and time
    now = dt.datetime.now()
    print(f"Current date and time: {now}")
    print(f"Current local time - hr: {now.hour}, min: {now.minute}")

    # Getting the current date and time with timezone information (UTC)
    # now_utc = dt.datetime.utcnow() --> (Now deprecated)
    # now_utc = dt.datetime.now(dt.timezone.utc)
    now_utc = dt.datetime.now(
        dt.UTC
    )  # same thing bcz in definition ==> dt.UTC = dt.timezone.utc
    print(f"Current date and time (UTC): {now_utc}")
    print(f"Current UTC time - hr: {now_utc.hour}, min: {now_utc.minute}")

    print(f"diff : {(now_utc - now.astimezone(dt.timezone.utc)).total_seconds()}")
    # because error isthrown when we subtract a timezone-aware datetime (one that has timezone info)
    # from a timezone-naive datetime (one that doesn’t).
    # Hence ensured everything in UTC

    # Creating a specific datetime
    event_datetime = dt.datetime(2024, 12, 25, 10, 0, 0)
    print(f"Specific event datetime: {event_datetime}")

    # Creating a datetime from date and time objects
    my_birth_datetime = dt.datetime.combine(my_birthday, meeting_time)
    print(f"My birth datetime: {my_birth_datetime}")

    # Accessing datetime components
    print(f"Year of current datetime: {now.year}")
    print(f"Hour of current datetime: {now.hour}")
    print(f"Date part of current datetime: {now.date()}")
    print(f"Time part of current datetime: {now.time()}")
    print("-" * 30)


def _5_():
    # 5. Working with `timedelta` objects
    separator("--- 5. Working with `timedelta` objects ---")

    # A timedelta object represents a duration, the difference between two dates or times.
    # It can be used for date arithmetic.

    today = dt.date.today()
    my_birthday = dt.date(1990, 5, 15)
    event_datetime = dt.datetime(2024, 12, 25, 10, 0, 0)
    now = dt.datetime.now()

    # Creating a timedelta
    print(f"One day timedelta: {dt.timedelta(days=1)}")
    print(f"Two weeks timedelta: {dt.timedelta(weeks=2)}")

    # Adding and subtracting timedeltas from dates/datetimes
    print(f"Tomorrow's date: {today + dt.timedelta(days=1)}")
    print(f"Date two weeks ago: {today - dt.timedelta(weeks=2)}")

    # Calculating the difference between two dates
    time_difference: dt.timedelta = today - my_birthday
    print(f"Time difference between today and my birthday: {time_difference}")
    print(f"This difference is {time_difference.days} days.")

    # You can also use timedeltas with datetime objects
    future_event: dt.timedelta = event_datetime - now
    print(f"Time until the event: {future_event}")
    # VKP_NOTE: check the below once
    print(f"This is {future_event.total_seconds()} seconds away.")
    print(f"This is {future_event.seconds} seconds away.")

    # Arithmetic with negative timedeltas
    print(f"Date 5 days before today: {today - dt.timedelta(days=5)}")
    print("-" * 30)


def _6_():
    # 6. Formatting Dates and Times (strftime)
    separator("--- 6. Formatting Dates and Times (strftime) ---")

    # The `strftime()` method formats a datetime object into a string according to a format code.
    # Common format codes:
    # %Y: Year with century (e.g., 2023)
    # %y: Year without century (00-99)
    # %m: Month as a zero-padded decimal number (01-12)# %d: Day of the month as a zero-padded decimal number (01-31)
    # %H: Hour (24-hour clock) as a zero-padded decimal number (00-23)# %I: Hour (12-hour clock) as a zero-padded decimal number (01-12)
    # %M: Minute as a zero-padded decimal number (00-59)
    # %S: Second as a zero-padded decimal number (00-61) - 60/61 for leap seconds
    # %p: Locale's equivalent of either AM or PM.
    # %A: Locale's full weekday name (e.g., Monday)
    # %a: Locale's abbreviated weekday name (e.g., Mon)
    # %B: Locale's full month name (e.g., January)
    # %b: Locale's abbreviated month name (e.g., Jan)
    # %c: Locale's appropriate date and time representation
    # %x: Locale's appropriate date representation
    # %X: Locale's appropriate time representation
    # %Z: Time zone name (if time zone is determined)
    # %z: UTC offset in the form +HHMM or -HHMM (if the object is aware)

    now = dt.datetime.now()

    formatted_date = now.strftime("%Y-%m-%d")  # Str from time
    print(f"Formatted date (YYYY-MM-DD): {formatted_date}")

    formatted_time = now.strftime("%H:%M:%S")
    print(f"Formatted time (HH:MM:SS): {formatted_time}")

    formatted_datetime = now.strftime("%A, %B %d, %Y at %I:%M %p")
    print(f"Formatted datetime (Full): {formatted_datetime}")

    # Example with a specific date
    specific_dt = dt.datetime(2025, 1, 1, 12, 0, 0)
    print(f"Specific datetime formatted: {specific_dt.strftime('%d/%m/%Y %H:%M')}")
    print("-" * 30)


def _7_():
    # 7. Parsing Dates and Times (strptime)
    separator("--- 7. Parsing Dates and Times (strptime) ---")

    # The `strptime()` class method parses a string representing a date and time
    # according to a format. The format string must match the input string exactly.

    date_string1 = "2023-10-27 10:30:00"
    format_string1 = "%Y-%m-%d %H:%M:%S"
    parsed_datetime1 = dt.datetime.strptime(date_string1, format_string1) # string parsed to timne
    print(f"Parsed datetime from '{date_string1}': {parsed_datetime1}")

    date_string2 = "October 27, 2023"
    format_string2 = "%B %d, %Y"
    parsed_date2 = dt.datetime.strptime(
        date_string2, format_string2
    ).date()  # Get only the date part
    print(f"Parsed date from '{date_string2}': {parsed_date2}")

    # Example of a mismatch in format string and date string
    try:
        invalid_string = "27/10/2023"
        invalid_format = "%Y-%m-%d"
        dt.datetime.strptime(invalid_string, invalid_format)
    except ValueError as e:
        print(f"Error parsing '{invalid_string}' with format '{invalid_format}': {e}")
    print("-" * 30)


def _8_():
    # 8. Time Zones
    separator("--- 8. Time Zones ---")

    # Handling time zones is crucial for applications dealing with users or data
    # from different geographical locations.
    # Python's `datetime` module has limited built-in time zone support.
    # For robust time zone handling, the `pytz` library is highly recommended.
    # However, we'll cover the basic `timezone` object here.

    # UTC (Coordinated Universal Time) is the primary time standard.
    utc_now = dt.datetime.now(dt.timezone.utc)
    print(f"Current time in UTC: {utc_now}")

    # Creating a timezone object for a fixed offset
    # For example, EST (Eastern Standard Time) is UTC-5
    est_offset = dt.timedelta(hours=-5)
    est_timezone = dt.timezone(est_offset, name="EST")  # Name is optional

    # Creating a datetime object aware of a specific timezone
    # Note: `datetime.now(tz)` gets the current time in the specified timezone.
    # If you want to convert an existing naive datetime, you need more steps.
    now_in_est = dt.datetime.now(est_timezone)
    print(f"Current time in EST (UTC-5): {now_in_est}")

    # Converting between timezones (using aware objects)
    # To convert, you need to make the original datetime timezone-aware first.
    # Example: Let's assume `now` (which is naive) represents a time in EST.
    # We need to make it aware before converting to UTC.

    # First, make 'now' timezone-aware (assuming it's EST)# This is a bit complex with naive datetimes. It's better to start with aware datetimes.
    # For demonstration, let's create an aware datetime directly.
    aware_est_time = dt.datetime(2023, 10, 27, 10, 30, 0, tzinfo=est_timezone)
    print(f"Aware EST time: {aware_est_time}")

    # Convert this EST time to UTC
    utc_equivalent = aware_est_time.astimezone(dt.timezone.utc)
    print(f"UTC equivalent: {utc_equivalent}")

    # Convert UTC time to another timezone (e.g., PST, UTC-8)
    pst_offset = dt.timedelta(hours=-8)
    pst_timezone = dt.timezone(pst_offset, name="PST")
    pst_equivalent = utc_equivalent.astimezone(pst_timezone)
    print(f"PST equivalent: {pst_equivalent}")

    # The `pytz` library is recommended for handling complex time zones,
    # including daylight saving time.
    # Example with pytz (requires `pip install pytz`):
    # import pytz
    # eastern = pytz.timezone('US/Eastern')
    # utc_now_pytz = datetime.now(pytz.utc)
    # eastern_now = utc_now_pytz.astimezone(eastern)
    # print(f"Current time in US/Eastern (using pytz): {eastern_now}")

    print("Note: For production, use `pytz` for robust time zone handling.")
    print("-" * 30)


def _9_():
    # 9. Handling Naive vs. Aware Datetimes
    separator("--- 9. Handling Naive vs. Aware Datetimes ---")

    # Naive datetime objects do not have any timezone information.
    naive_dt = dt.datetime(2023, 10, 27, 15, 0, 0)
    print(f"Naive datetime: {naive_dt}, Is aware? {naive_dt.tzinfo is not None}")

    # Aware datetime objects have timezone information.
    aware_dt = dt.datetime(2023, 10, 27, 15, 0, 0, tzinfo=dt.timezone.utc)
    print(f"Aware datetime (UTC): {aware_dt}, Is aware? {aware_dt.tzinfo is not None}")

    # Operations between naive and aware datetimes can lead to errors or unexpected results.
    # Always ensure consistency or explicitly convert between them.

    # Example of making a naive datetime aware (assuming it's in a specific timezone)
    # This is where `pytz` or explicit `replace()` with `timezone` can be used.
    # Using `replace()` for a fixed offset:
    naive_time_in_est = dt.datetime(2023, 10, 27, 10, 0, 0)
    est_offset = dt.timedelta(hours=-5)
    est_tz = dt.timezone(est_offset)
    aware_time_in_est = naive_time_in_est.replace(tzinfo=est_tz)
    print(f"Naive time made aware (EST): {aware_time_in_est}")

    # Converting an aware datetime to a different timezone
    # (demonstrated in section 8, using astimezone)
    print("-" * 30)


def _10_():
    # 10. Useful `datetime` constants and methods
    separator("--- 10. Useful `datetime` constants and methods ---")


    now = dt.datetime.now()
    today = dt.date.today()

    # `datetime.min` and `datetime.max` represent the earliest and latest possible datetime objects.
    print(f"Earliest possible datetime: {dt.datetime.min}")
    print(f"Latest possible datetime: {dt.datetime.max}")

    # `date.min`, `date.max`, `time.min`, `time.max` also exist.

    # `now()` vs `utcnow()`
    # `datetime.now()`: Returns the current local date and time. If `tz` is provided,
    # it returns the current time for that timezone.
    # `datetime.utcnow()`: Returns the current UTC date and time as a *naive* datetime object.
    # It's generally recommended to use `datetime.now(timezone.utc)` for an aware UTC object.
    print(f"datetime.now(): {dt.datetime.now()}")
    print(f"datetime.utcnow() (naive): {dt.datetime.utcnow()}")
    print(f"datetime.now(timezone.utc) (aware): {dt.datetime.now(dt.timezone.utc)}")

    # `today()` for date objects
    print(f"date.today(): {dt.date.today()}")

    # `isoformat()`: Returns a string in ISO 8601 format.
    print(f"Current datetime in ISO format: {now.isoformat()}")
    print(f"Today's date in ISO format: {today.isoformat()}")

    # `weekday()` and `isoweekday()`
    # `weekday()`: Monday is 0, Sunday is 6.# `isoweekday()`: Monday is 1, Sunday is 7.
    print(f"Today's weekday (0=Mon, 6=Sun): {today.weekday()}")
    print(f"Today's isoweekday (1=Mon, 7=Sun): {today.isoweekday()}")

    print("-" * 30)


def _conclusion():
    # 11. Common Pitfalls and Best Practices
    print("--- 11. Common Pitfalls and Best Practices ---")

    print("Pitfalls:")
    print("- Mixing naive and aware datetime objects can lead to bugs.")
    print(
        "- Assuming local time without explicit handling (e.g., using `datetime.now()` without timezone context)."
    )
    print("- Incorrectly parsing date strings without matching the format string.")
    print("- Not considering daylight saving time (DST) when dealing with timezones.")

    print("Best Practices:")
    print(
        "- Store dates and times in UTC whenever possible, especially for server-side applications or data storage."
    )
    print(
        "- Use timezone-aware datetime objects for all time-related operations if your application spans multiple timezones."
    )
    print("- Use the `pytz` library for robust timezone management.")
    print(
        "- Clearly define and use consistent formatting for `strftime` and `strptime`."
    )
    print("- Validate user input for dates and times.")
    print(
        "- Be mindful of the difference between `datetime.now()` and `datetime.utcnow()`."
    )
    print("-" * 30)

    print("--- Tutorial Complete ---")
    print("You have now covered the fundamental aspects of Python's `datetime` module.")
    print(
        "Practice with these examples and explore further to master date and time manipulation."
    )


if __name__ == "__main__":
    # _2_()
    # _3_()
    # _4_()
    # _5_()
    # _6_()
    # _7_()
    # _8_()
    # _9_()
    _10_()
    # _conclusion()
