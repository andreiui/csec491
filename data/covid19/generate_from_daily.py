#!/usr/bin/env python3

"""
Python script for converting daily COVID-19
cases and deaths to monthly and yearly statistics.
--------------------------------------------------
Created on 03/27/2023. Last updated on 03/28/2023.
Written by Andrei Pascu, Yale College '23.
--------------------------------------------------
"""

from sys import stderr
from csv import reader, writer

# Console helper methods
console_info = lambda msg: print(f"\033[34mINFO:\033[00m {msg}", file=stderr)
console_warn = lambda msg: print(f"\033[93mWARN:\033[00m {msg}", file=stderr)
console_done = lambda msg: print(f"\033[96mDONE:\033[00m {msg}", file=stderr)

# Input daily stats file to output monthly and yearly files
FILENAMES: dict[str, list[str, str]] = {
    "time_series_covid19_cases.csv": [
        "cases_monthly.csv",
        "cases_yearly.csv",
    ],
    "time_series_covid19_deaths.csv": [
        "deaths_monthly.csv",
        "deaths_yearly.csv",
    ],
}

# Read data from the per-day files and generate the monthly and yearly files
if __name__ == "__main__":
    for in_d_fn, (out_m_fn, out_y_fn) in FILENAMES.items():
        monthly_str: list[str] = []
        monthly_idx: list[int] = []
        yearly_str:  list[str] = []
        yearly_idx:  list[int] = []

        with open(in_d_fn, "r") as file_in, open(out_m_fn, "w+") as file_out_mo, open(out_y_fn, "w+") as file_out_yr:
            out_mo, out_yr = writer(file_out_mo), writer(file_out_yr)

            # Output start of file generation process
            console_info(f"\"{in_d_fn}\": started generation of \"{out_m_fn}\", \"{out_y_fn}\"...")

            for i, row in enumerate(reader(file_in, delimiter=",")):
                # Create the new header for monthly and yearly
                if i == 0:
                    # Start on year 2020 and increment month
                    yr = 20
                    in_range = True

                    # Keep updating header while dates are valid
                    while in_range:
                        for mo in range(1, 13):
                            date = f"{mo}/1/{yr}"

                            # COVID-19 data starts on 1/22/20
                            if date == "1/1/20":
                                continue

                            monthly_str.append(f"{12 if mo == 1 else mo - 1}/{yr - 1 if mo == 1 else yr}")
                            if date in row:
                                # If date is within bounds, add info to monthly and yearly headers
                                monthly_idx.append(row.index(date) - 1)
                                if mo == 1:
                                    yearly_str.append(f"20{yr - 1}")
                                    yearly_idx.append(row.index(date) - 1)
                            else:
                                # Otherwise, break out of loop
                                monthly_idx.append(len(row) - 1)
                                if row[-1] == f"12/31/{yr - 1}":
                                    yearly_str.append(f"20{yr - 1}")
                                    yearly_idx.append(len(row) - 1)
                                in_range = False
                                break

                            if mo == 12:
                                yr += 1

                    # Output date information about monthly and yearly files
                    console_info(f"\"{out_m_fn}\": compiling daily data into {len(monthly_str)} months from {monthly_str[0]} to {monthly_str[-1]} (inclusive)...")
                    console_info(f"\"{out_y_fn}\": compiling daily data into {len(yearly_str)} years from {yearly_str[0]} to {yearly_str[-1]} (inclusive)...")

                    out_mo.writerow(row[:4] + monthly_str)
                    out_yr.writerow(row[:4] + yearly_str)

                # For each row, compute monthly and yearly data using the corresponding index list
                else:
                    for lst_idx, out in ((monthly_idx, out_mo), (yearly_idx, out_yr)):
                        new_row = list(row[:4])
                        prev_val = 0
                        for idx in lst_idx:
                            new_row.append(int(row[idx]) - prev_val)
                            prev_val = int(row[idx])
                        out.writerow(new_row)

            # Output completion of file generation
            console_done(f"\"{out_m_fn}\": done compiling")
            console_done(f"\"{out_y_fn}\": done compiling")