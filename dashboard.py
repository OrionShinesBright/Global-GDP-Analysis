# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> dashboard.py

> Final logical part of the program
> Obtains the sanitized data and the results of the computations
> Creates the graphs/charts, and prints out the results for the dashboard part
> Handles all visualizations modularly
"""

# External Dependancies
import json
import matplotlib.pyplot as plt

# Internal Imports
from data_loader import load_gdp_data
from data_processor import reshape_data, filter_data, compute_stat

# Defining the folder structure. Good for visual separation of data and code
DATA_FILE = "data/gdp.csv"
CONFIG_FILE = "config.json"


###############################################################################
# Configuration Loader Function
#
# Handles the file descriptors, loads contents into memory after parsing as json
#
# ARG:
# RET: json stream
def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)


