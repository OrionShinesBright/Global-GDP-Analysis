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

# External Dependencies
from itertools import repeat
import os

# Internal Dependencies
from .prompt_handler import prompt


###############################################################################
# Function to Clear the Screen
#
# Made to be OS-agnostic
#
# ARG:
# RET:
def clear_screen():
    try:
        print("\033[2J\033[H", end="")
    except:
        os.system("cls" if os.name == "nt" else "clear")



###############################################################################
# Dashboard Presentation Function
#
# Visualizes the processed computations
# Very primitive dashboard
#
# ARG: config (list), filtered_data (list), result (int)
# RET: json stream
def show_dashboard(config, filtered_data, result,reshaped,data_scope = None):
    names = list(map(lambda d: d["name"], filtered_data))
    gdps = list(map(lambda d: d["gdp"], filtered_data))
    yearly_data = list(
        filter(
            lambda d:
                d["type"] == "country"
                and (
                    d["region"] == config["region"]
                    or d["name"] == config["region"]
                ),
            reshaped
        )
    )
    years = sorted(set(map(lambda d: d["year"], yearly_data)))
    yearly_gdp = list(
        map(
            lambda y: sum(
                map(
                    lambda d: d["gdp"],
                    filter(lambda r: r["year"] == y, yearly_data)
                )
            ),
            years
        )
    )
    year_slice = list(
        filter(
            lambda d: d["year"] == config["year"] and d["type"] == "country",
            reshaped
        )
    )

    clear_screen()
    prompt(names, gdps, data_scope, yearly_data, years, yearly_gdp, year_slice, config, reshaped)
