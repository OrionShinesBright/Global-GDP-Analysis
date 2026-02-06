# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> data_loader.py

> First logical part of the program
> Obtains the dataset file, and loads the data in csv format
> Works independant of the Operating System
"""

# built-in csv parser
import csv

# built-in OS abstraction library.
# using to access path in a cross-platform manner.
import os


###############################################################################
# Data loader function
#
# Takes filepath as argument
# Returns csv data
#
# ARG: filepath (str)
# RET: csv data (list)
def load_gdp_data(filepath):
    # Error handling
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"CSV file not found: {filepath}")
    # Read and return as list
    with open(filepath, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)
