#!/usr/bin/env python3

"""
TBD
--------------------------------------------------
Created on 02/28/2023. Last updated on 02/28/2023.
Written by Andrei Pascu, Yale College '23.
--------------------------------------------------
"""

from sys import stderr
from csv import reader, writer

""" Console helper functions """
console_info  = lambda msg: print(f"\033[34mINFO:\033[00m  {msg}", file=stderr)
console_warn  = lambda msg: print(f"\033[93mWARN:\033[00m  {msg}", file=stderr)
console_fatal = lambda msg: print(f"\033[31mFATAL:\033[00m {msg}", file=stderr)

""" Translation for JHU raw data files to Carribean processed data """
RAW_TO_PROC_FNS: dict[str, str] = {
    "raw/time_series_covid19_confirmed_global.csv": "proc/time_series_covid19_confirmed_caribbean.csv",
    "raw/time_series_covid19_deaths_global.csv":    "proc/time_series_covid19_deaths_caribbean.csv",
    "raw/time_series_covid19_recovered_global.csv": "proc/time_series_covid19_recovered_caribbean.csv",
}

""" List of Caribbean countries to filter; should match names in JHU raw files """
CARIBBEAN_COUNTRIES: set[str] = {
    "Antigua and Barbuda",
}

""" Iterate through JHU raw files and rows of countries and write Caribbean data """
if __name__ == "__main__":
    for raw_fn, proc_fn in RAW_TO_PROC_FNS.items():
        # Maintain list of countries
        global_countries: set[str] = set()

        # Open input and output .csv files
        with open(raw_fn, "r") as file_in, open(proc_fn, "w+") as file_out:
            out = writer(file_out)
            for i, row in enumerate(reader(file_in, delimiter=",")):
                if i == 0 or row[1] in CARIBBEAN_COUNTRIES:
                    out.writerow(row)
                    if i != 0:
                        global_countries.add(row[1])

            # Output warning if any specified countries are not in JHU time series
            for caribbean_country in CARIBBEAN_COUNTRIES.difference(global_countries):
                console_warn(f"\"{raw_fn}\": \"{caribbean_country}\" country name not found.")
        
        # Output completion of global to Caribbean filtering
        console_info(f"\"{raw_fn}\": completed export to \"{proc_fn}\"")
        