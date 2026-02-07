# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> main.py

> Entry Point
> Controller for all operations
"""

# Internal Dependancies
from src.data_loader import (
        load_gdp_data,
        load_config
    )
from src.data_processor import (
        reshape_data,
        filter_data,
        compute_stat,
        split_by_type,
        is_country
    )
from src.dashboard import (
        show_dashboard
    )
# Dataset path
DATA_FILE = "assets/World_Bank_Dataset.csv"


###############################################################################
# Main
#
# Abandon all hope, ye who enter here..
#
# ARG:
# RET:
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
