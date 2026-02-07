# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> prompt_handler.py

> Called by dashboard as a helper module
> Handles all user input, and maps the selected value onto a function
> The function is a graph/chart/plot renderer from chart_implementations.py
"""

# External Dependencies
from InquirerPy import inquirer
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

# Internal Dependencies
from chart_implementations import *


###############################################################################
# Prompt for the dashboard
#
# Displays a selectable menu after displaying initial dashboard
#
# ARG: names (list), gdps (list), data_scope (list), yearly_data (list),
#      years (list), yearly_gdp (list), year_slice (list), config (list),
#      reshaped (list)
# RET:
def prompt(names, gdps, data_scope, yearly_data, years, yearly_gdp, year_slice, config, reshaped):
    action = inquirer.select(
        message="Select an action:",
        choices=[
            "Bar Chart",
            "Pie Chart",
            "Line Plot",
            "Lollipop Plot",
            "Dot Plot",
            "Tree Map",
            "Word Cloud",
            "Slope Chart",
            Choice(value=None, name="Exit"),
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
        "Slope Chart":      lambda: slope_chart(config, reshaped, year_slice)
    }

    # Call the selected action
    if action in plot_actions:
        plot_actions[action]()
    else:
        print(f"Unknown action: {action}")
