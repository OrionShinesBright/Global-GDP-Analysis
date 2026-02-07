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

from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

from itertools import repeat

# Internal Imports
from data_loader import load_gdp_data
from data_processor import (
        reshape_data,
        filter_data,
        compute_stat,
        split_by_type,
        is_country
    )
from chart_implementations import *

# Defining the folder structure. Good for visual separation of data and code
DATA_FILE = "data/gdp.csv"
CONFIG_FILE = "config.json"


def clear_screen():
    try:
        print("\033[2J\033[H", end="")
    except:
        import os
        os.system("cls" if os.name == "nt" else "clear")

###############################################################################
# Prompt for the dashboard
#
# Displays a selectable menu after displaying initial dashboard
#
# ARG:
# RET:
def prompt(names, gdps, data_scope, yearly_data, years, yearly_gdp, year_slice, config, reshaped):
    action = inquirer.select(
        message="Select an action:",
        choices=[
            Separator(),
            Separator("# Region-Wise GDP Plots:"),
            Separator(),

            "Bar Chart",
            "Pie Chart",
            "Dot Plot",
            "Lollipop Plot",

            Separator(),
            Separator("# Year-Wise GDP Plots:"),
            Separator(),

            "Line Plot",
            "Slope Chart",

            Separator(),
            Separator("# Extra GDP Plots:"),
            Separator(),

            "Tree Map",
            "Word Cloud",

            Separator(),
            Separator("# Exit:"),
            Separator(),

            "Exit"
        ],
        default=None,
    ).execute()

    # Map action names to functions
    plot_actions = {
        "Bar Chart":        lambda: bar_chart(names, gdps, data_scope),
        "Pie Chart":        lambda: pie_chart(names, gdps, data_scope),
        "Line Plot":        lambda: line_plot(years, yearly_gdp),
        "Lollipop Plot":    lambda: lollipop_plot(names, gdps, config),
        "Dot Plot":         lambda: dot_plot(names, gdps, config),
        "Tree Map":         lambda: tree_map(year_slice, config),
        "Word Cloud":       lambda: word_cloud(year_slice, config),
        "Slope Chart":      lambda: slope_chart(config, reshaped, year_slice),
        "Exit":             lambda: exit_prompt()
    }

    # Call the selected action
    if action in plot_actions:
        plot_actions[action]()  # call the function
    else:
        print(f"Unknown action: {action}")



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

def exit_prompt():
    print("Dying, bye!")
    exit(1)

def dashboard_info(data_scope, config, result):
    # dashboard visualization (TUI based)
    print("\n===== GDP ANALYSIS DASHBOARD =====")
    print(f"Scope     : {data_scope}")
    print(f"Region    : {config['region']}")
    print(f"Year      : {config['year']}")
    print(f"Operation : {config['operation']}")
    print("---------------------------------")
    # Handle 'not found' error
    if result is None:
        print("No data available for this configuration.")
        return
    # Print result of computation according to user's config.json
    print(f"Result    : {result:,.2f}\n")


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
        print("--------------------------------------------\n")
        dashboard_info(data_scope, config, result)
        print("--------------------------------------------\n")
        prompt(names, gdps, data_scope, yearly_data, years, yearly_gdp, year_slice, config, reshaped)




###############################################################################
# Main - Entry point
#
# Is the logical controller for the entire program
#
def main():
    try:
        # 0.    FETCH
        config = load_config()

        # 1.    LOAD
        raw_data = load_gdp_data(DATA_FILE)

        # 2(a). SANITIZE
        reshaped = reshape_data(raw_data)

        # 2(b). FILTER
        target = config["region"]
        year = config["year"]

        if is_country(target):
            filtered = filter_data(reshaped, target, year, row_type="country")
            data_scope = "Country-wise"
        else:
            filtered = filter_data(reshaped, target, year)
            data_scope = "Region-wise"

        # 2. COMPUTE
        result = compute_stat(filtered, config["operation"])
        active_data = filtered


        # 4.    VISUALIZE
        show_dashboard(config, active_data, result, data_scope, reshaped)

    except Exception as e:
        print("ERROR:", e)


#######
# Run #
#######
if __name__ == "__main__":
    main()
