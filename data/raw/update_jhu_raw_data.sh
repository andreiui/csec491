#!/bin/bash

#
# Script for downloading and updating the raw time
# series for VOID-19 from the JHU GitHub repository
# available at github.com/CSSEGISandData/COVID-19.
#
# When running this script, manually update the
# sources file snapshot date and time.
# --------------------------------------------------
# Created on 03/01/2023. Last updated on 03/01/2023.
# Written by Andrei Pascu, Yale College '23.
# --------------------------------------------------
#

# URL to fetch raw COVID-19 data
url="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series"

# Filenames definition for raw data
fns=("time_series_covid19_confirmed_US.csv"      \
     "time_series_covid19_confirmed_global.csv"  \
     "time_series_covid19_deaths_US.csv"         \
     "time_series_covid19_deaths_global.csv"     \
     "time_series_covid19_recovered_global.csv")

# Download each raw file into directory
for fn in ${fns[@]}; do
    curl "${url}/${fn}" --output $fn --silent && echo "fetched \"$fn\""
done
