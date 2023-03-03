#!/usr/bin/env python3

"""
Python script for generating Caribbean COVID-19
confirmed cases and deaths from the JHU raw files.
--------------------------------------------------
Created on 02/28/2023. Last updated on 03/02/2023.
Written by Andrei Pascu, Yale College '23.
--------------------------------------------------
"""

from sys import stderr
from csv import reader, writer

# Console helper methods
console_info = lambda msg: print(f"\033[34mINFO:\033[00m {msg}", file=stderr)
console_warn = lambda msg: print(f"\033[93mWARN:\033[00m {msg}", file=stderr)
console_done = lambda msg: print(f"\033[96mDONE:\033[00m {msg}", file=stderr)

# Translation for JHU raw data files to Carribean generated data
FILENAMES: dict[str, tuple[str, str]] = {
    "gen/time_series_covid19_confirmed_caribbean.csv": (
        "raw/time_series_covid19_confirmed_global.csv",
        "raw/time_series_covid19_confirmed_US.csv",
    ),
    "gen/time_series_covid19_deaths_caribbean.csv": (
        "raw/time_series_covid19_deaths_global.csv",
        "raw/time_series_covid19_deaths_US.csv",
    ),
}

# List of Caribbean countries, states and territories to filter;
# should match names in JHU raw files
GLOBAL_CARIBBEAN: set[str] = set([
    "Antigua and Barbuda",
    "Bahamas",
    "British Virgin Islands", # UK
    "Cayman Islands", # UK
    "Guadeloupe", # FR
    "Saint Vincent and the Grenadines",
    "Turks and Caicos Islands", # UK
])
US_TERRITORIES: set[str] = set([
    "American Samoa",
    "Guam",
    "Northern Mariana Islands",
    "Puerto Rico",
    "Virgin Islands",
])

# Iterate through JHU raw files and write generated Caribbean data
# following the *_global.csv format
if __name__ == "__main__":
    for gen_fn, (raw_global_fn, raw_us_fn) in FILENAMES.items():
        all_regions: set[str] = set()

        # Open input and output .csv files
        # First, open global files and filter for Carribean countries and states
        console_info(f"\"{raw_global_fn}\": started processing...")

        # Read through input global file and write to output
        with open(gen_fn, "w+") as file_out, open(raw_global_fn, "r") as file_in:
            out = writer(file_out)
            for i, row in enumerate(reader(file_in, delimiter=",")):
                if i == 0 or not GLOBAL_CARIBBEAN.isdisjoint(row[0:2]):
                    out.writerow(row)
                    if i == 0:
                        num_days_global = len(row[4:])
                    else:
                        all_regions.add(row[int(row[1] in GLOBAL_CARIBBEAN)])

        # Output any warnings and completion of global .csv processing
        for country in GLOBAL_CARIBBEAN.difference(all_regions):
            console_warn(f"\"{raw_global_fn}\": country name \"{country}\" not found")
        console_info(f"\"{raw_global_fn}\": done processing")

        all_regions: set[str] = set()
        pr_raw_data: list[list[str]] = []

        # Second, open U.S. files and filter for U.S. territories, including
        # American Samoa, Guam and the Northern Mariana Islands
        console_info(f"\"{raw_us_fn}\": started processing...")
        with open(gen_fn, "a") as file_out, open(raw_us_fn, "r") as file_in:
            out = writer(file_out)
            for i, row in enumerate(reader(file_in, delimiter=",")):
                if i == 0:
                    idx = row.index("1/22/20")
                    num_days_us = len(row[idx:])
                    if num_days_global != num_days_us:
                        console_warn(f"\"{raw_us_fn}\": dates do not align")
                    continue
                if row[6] not in US_TERRITORIES:
                    continue
                
                # For Puerto Rico, combine multiple rows listed on a per-province basis
                # For the rest, write to output
                if row[6] == "Puerto Rico":
                    pr_raw_data.append(row[idx:])
                else:
                    out.writerow(row[6:10] + row[idx:])

                all_regions.add(row[6])

            # Calculate and write Puerto Rico data to output
            if "Puerto Rico" in US_TERRITORIES:
                out.writerow(
                    ["Puerto Rico", "US" , "18.2208", "-66.5901"] +
                    [sum(int(d) for d in data) for data in zip(*pr_raw_data)]
                )

        # Output any warnings and completion of U.S. .csv processing
        for country in US_TERRITORIES.difference(all_regions):
            console_warn(f"\"{raw_us_fn}\": country name \"{country}\" not found")
        console_info(f"\"{raw_us_fn}\": done processing")

        # Output completion of Caribbean .csv generation
        console_done(f"\"{gen_fn}\": done exporting")
        