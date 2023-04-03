#!/bin/bash

#
# Script for syncing the "data/countries" folder
# into the "code" directory.
# --------------------------------------------------
# Created on 03/30/2023. Last updated on 04/03/2023.
# Written by Andrei Pascu, Yale College '23.
# --------------------------------------------------
#

# Iterate through each Excel file
for pathname in ./data/countries/*.xlsx; do
    # Remove .xslx and path
    country=${pathname%.xlsx}
    country=${country##*/}
    # Create directory if it does not exist
    mkdir -p "./code/$country"
    # Convert Excel file to .csv
    ssconvert --export-file-per-sheet --export-options "sheet=Data" $pathname "./code/analysis/$country/%s.csv"
    echo "Converted to .csv file: $country.xlsx"
done
