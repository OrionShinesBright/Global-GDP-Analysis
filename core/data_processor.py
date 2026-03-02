# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> data_processor.py

> Second logical part of the program
> Obtains csv formatted data from the data_loader function.
> Filters and aligns data from the given columns as required.
"""

# To separately handle regions vs countries
import pycountry

###############################################################################
# Country vs Region Checking Function
#
# Helper function to be used in separation of data
#
# ARG: name (str)
# RET: is_country (bool)
def is_country(name):
    try:
        pycountry.countries.lookup(name)
        return True
    except LookupError:
        return False


###############################################################################
# Row Consolidation Function - Called in reshape_data() for each row individually
#
# The years in the dataset are all displayed as separate columns, which is hard to work with
# Therefore this function integrates them as one column, by grouping their respective
# GDPs into a list.
#
# ARG: row (list)
# RET: row (list)
def expand_row(row):
    # Holding names of dataset columns
    country = row["Country Name"]
    region = row["Continent"]
    # Figuring out the type for the region
    row_type = "country" if is_country(country) else "region"
    # Returning newly modified row as a list
    return list(
        map(
            # mapping
            lambda y: {
                "name": country,
                "region": region,
                "year": int(y),
                "gdp": float(row[y]),
                "type": row_type,
            },
            # filtering + appending
            filter(lambda k: k.isdigit() and row[k] != "", row.keys()),
        )
    )


###############################################################################
# Data Realignment Function
#
# Convert wide-year columns into:
# Country | Region | Year | GDP
#
# ARG: rows (list)
# RET: rows (list)
def reshape_data(rows):
    return [item for row in rows for item in expand_row(row)]


###############################################################################
# Filtration Function
#
# This function creates a subset of the dataset that only contains
# the modified rows that we require, i.e:
#       1. Region
#       2. Year
#
# ARG: data (list), region (str), year (int), row_type (str)
# RET: filtered_data (list)
def filter_data(data, target, year, row_type=None):
    is_target_country = is_country(target)

    return list(
        filter(
            lambda d:
                (
                    # Country-wise query
                    (is_target_country and d["type"] == "country" and d["name"] == target)
                    or
                    # Region-wise query
                    (not is_target_country and
                     (
                        (d["type"] == "region" and d["name"] == target) or
                        (d["type"] == "country" and d["region"] == target)
                     ))
                )
                and d["year"] == year
                and (row_type is None or d["type"] == row_type),
            data
        )
    )



###############################################################################
# Computation Function
#
# This function calculates the required statistic on the required chunk of data
# Supported operations are:
#       1. average
#       2. sum
#
# ARG: data (list), operation (str)
# RET: result (int)
def compute_stat(data, operation):
    # obtain the gdp field from data chunk
    values = list(map(lambda d: d["gdp"], data))
    # Handle 'not found' error
    if not values:
        return None

    # Computational part
    if operation == "average":
        return sum(values) / len(values)
    elif operation == "sum":
        return sum(values)
    # Handle 'incorrect operation error'
    else:
        raise ValueError("Invalid operation (must be 'average' or 'sum')")

###############################################################################
# Split by region type
#
# Two types are acceptable:
#    1. country
#    2. region
#
# ARG: data (list)
# RET: regions (list), countries (list)
def split_by_type(data):
    regions = list(filter(lambda d: d["type"] == "region", data))
    countries = list(filter(lambda d: d["type"] == "country", data))
    return regions, countries
