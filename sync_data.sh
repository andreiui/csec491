#!/bin/bash

#
# Script for syncing the "data/countries" folder
# into the "code" directory.
# --------------------------------------------------
# Created on 03/30/2023. Last updated on 03/30/2023.
# Written by Andrei Pascu, Yale College '23.
# --------------------------------------------------
#

# Recursively remove all contents in "code/countries"
rm -r ./code/countries

# Recursively copy the "countries" subfolder from "data" into "code"
cp -r ./data/countries ./code
