#!/bin/bash

#
# Script for syncing the "data/countries" folder
# into the "code" directory.
# --------------------------------------------------
# Created on 03/30/2023. Last updated on 04/16/2023.
# Written by Andrei Pascu, Yale College '23.
# --------------------------------------------------
#

# Iterate through each Excel file in "data/countries"
for pathname in ./data/countries/*.xlsx; do
    # Remove .xslx and path
    country=${pathname%.xlsx}
    country=${country##*/}
    # Create directory if it does not exist
    mkdir -p "./code/analysis/$country"
    # Convert Excel file to .csv
    ssconvert --export-file-per-sheet --export-options "sheet=Data" $pathname "./code/analysis/$country/%s.csv"
    # For Cuba, Jamaica and Puerto Rico, export monthly data
    if [ $country = "cuba" ] || [ $country = "jamaica" ] || [ $country = "puerto_rico" ]; then
        ssconvert --export-file-per-sheet --export-options "sheet=Monthly" $pathname "./code/analysis/$country/%s.csv"
    fi
    echo "Converted to .csv file: $country.xlsx"
done
