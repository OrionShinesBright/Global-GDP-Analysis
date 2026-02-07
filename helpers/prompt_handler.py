# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> helpers/prompt_handler.py

> Called by dashboard as a helper module
> Handles all user input, and maps the selected value onto a function
> The function is a graph/chart/plot renderer from helpers/chart_implementations.py
"""

# External Dependencies
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

# Internal Dependencies
from helpers.chart_implementations import *


########################################
# Function to break out of Prompt loop #
########################################
def exit_prompt():
    print("\n\n\033[0;35m\tThank you for analysing the dataset with us.\n\033[0;33m\tGood bye!\n")
    exit(1)


###############################################################################
# Prompt for the dashboard
#
# Displays a selectable menu after displaying initial dashboard
#
# ARG: names (list), gdps (list), data_scope (list), yearly_data (list),
#      years (list), yearly_gdp (list), year_slice (list), config (list),
#      reshaped (list)
# RET:
def prompt(names, gdps, data_scope, yearly_data, years,
           yearly_gdp, year_slice, config, reshaped):
    print("\n")
    action = inquirer.select(
        message="  Choose Type of Graph to Display:",
        choices=[
            Separator(""),
            Separator("󰕖    Region-Wise GDP Plots"),
            "Bar Chart",
            "Pie Chart",
            "Dot Plot",
            "Lollipop Plot",
            Separator(""),
            Separator("󰕖    Year-Wise GDP Plots"),
            "Line Plot",
            "Slope Chart",
            Separator(""),
            Separator("󰕖    Global GDP Plots"),
            "Tree Map",
            "Word Cloud",
            Separator(""),
            "Exit"
        ],
        default=None,
    ).execute()

    # Map action names to functions
    plot_actions = {
        "Bar Chart":        lambda: bar_chart(names, gdps, data_scope),
        "Pie Chart":        lambda: pie_chart(names, gdps, data_scope),
        "Line Plot":        lambda: line_plot(years, yearly_gdp),
        "Lollipop Plot":    lambda: lollipop_plot(names, gdps, config, data_scope),
        "Dot Plot":         lambda: dot_plot(names, gdps, config, data_scope),
        "Tree Map":         lambda: tree_map(year_slice, config),
        "Word Cloud":       lambda: word_cloud(year_slice, config),
        "Slope Chart":      lambda: slope_chart(config, reshaped, year_slice),
        "Exit":             lambda: exit_prompt()
    }

    # Call the selected action
    if action in plot_actions:
        plot_actions[action]()
    else:
        print(f"Unknown action: {action}")
