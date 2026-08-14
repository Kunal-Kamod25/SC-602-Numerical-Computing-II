# utilities.py
#
# Why this file exists:
# There are some small helper things we need in many places, like
# getting the current date/time, or printing a nice separator line.
# Instead of repeating this code again and again, we keep it here.
#
# This is NOT a class because these are just small independent
# helper functions, no need for OOP here.

import datetime
import time


def get_current_datetime_string():
    # Returns the current date and time as a readable string.
    # Example: 2025-01-15 10:30:45
    now = datetime.datetime.now()
    return now.strftime("%Y-%m-%d %H:%M:%S")


def print_separator():
    # Just prints a line of "=" signs, used to make the menu
    # and outputs look neat.
    print("=" * 40)


def start_timer():
    # Returns the current time, we will use this later to find
    # out how long the program took to run.
    return time.time()


def stop_timer(start_time):
    # Subtracts start time from current time to get the
    # time taken in seconds. We round it to 6 decimal places.
    end_time = time.time()
    time_taken = end_time - start_time
    return round(time_taken, 6)


def format_number(value):
    # Helper to print numbers nicely, rounding off long
    # decimals so the output file does not look messy.
    return round(value, 6)
