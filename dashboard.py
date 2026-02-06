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


###############################################################################
# Dashboard Presentation Function
#
# Visualizes the processed computations
# Very primitive dashboard
#
# ARG: config (list), filtered_data (list), result (int)
# RET: json stream
def show_dashboard(config, filtered_data, result):
    # dashboard visualization (TUI based)
    print("\n===== GDP ANALYSIS DASHBOARD =====")
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

    # Get the variables ready for putting into plots
    countries = list(map(lambda d: d["country"], filtered_data))
    gdps = list(map(lambda d: d["gdp"], filtered_data))

    # Bar Chart
    plt.figure()
    plt.bar(countries, gdps)
    plt.title("GDP by Country")
    plt.xlabel("Country")
    plt.ylabel("GDP")
    plt.xticks(rotation=90)
    # Pie Chart
    plt.figure()
    plt.pie(gdps, labels=countries, autopct="%1.1f%%")
    plt.title("GDP Distribution")
    # Print the prepared charts
    plt.show()


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
        filtered = filter_data(reshaped, config["region"], config["year"])

        # 3.    COMPUTE
        result = compute_stat(filtered, config["operation"])

        # 4.    VISUALIZE
        show_dashboard(config, filtered, result)

    except Exception as e:
        print("ERROR:", e)


#######
# Run #
#######
if __name__ == "__main__":
    main()
