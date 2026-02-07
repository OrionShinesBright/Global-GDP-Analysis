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
from helpers.prompt_handler import prompt


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
# Function to Display Dashboard Header
#
# Displays the reults of the computations, as well as information
# About the provided configuration in config.json
#
# ARG: data_scope (list), config (list), result (int)
# RET:
def dashboard_info(data_scope, config, result):
    # dashboard visualization (TUI based)
    print(f"\t\033[0;90m╭────────────────────────────────────┬─────────────╮")
    print(f"\t\033[0;90m│ \033[0;34mDASHBOARD FOR WORLD BANK ANALYTICS \033[0;90m│ \033[0;31m1970 ─ 2020 \033[0;90m│")
    print(f"\t\033[0;90m╰────────────────────────────────────┴─────────────╯")
    print(f"\t\033[0;90m────────────┬───────────────────────────────────────")
    print(f"\t\033[0;90m  \033[0;92mScope     \033[0;90m│\t\033[0;93m{data_scope}")
    print(f"\t\033[0;90m  \033[0;92mRegion    \033[0;90m│\t\033[0;93m{config['region']}")
    print(f"\t\033[0;90m  \033[0;92mYear      \033[0;90m│\t\033[0;93m{config['year']}")
    print(f"\t\033[0;90m  \033[0;92mOperation \033[0;90m│\t\033[0;93m{config['operation']}")
    # Handle 'not found' error
    if result is None:
        print(f"\t\033[0;90m  \033[0;0mNo data available for this configuration.")
        print(f"\t\033[0;90m────────────────────────────────────────────────────")
        return
    # Print result of computation
    print(f"\t\033[0;90m  \033[0;92mResult    \033[0;90m│\t\033[0;93m{result:,.2f}")
    print(f"\t\033[0;90m────────────┴───────────────────────────────────────")


###############################################################################
# Dashboard Presentation Function
#
# Visualizes the processed computations
# Very primitive dashboard
#
# ARG: config (list), filtered_data (list), result (int)
# RET: json stream
def show_dashboard(config, filtered_data, result, data_scope, reshaped):
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

    for _ in repeat(None):
        clear_screen()
        dashboard_info(data_scope, config, result)
        prompt(names, gdps, data_scope, yearly_data, years, yearly_gdp, year_slice, config, reshaped)
