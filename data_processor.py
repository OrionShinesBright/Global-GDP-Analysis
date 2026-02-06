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
    # Returning newly modified row as a list
    return list(
        map(
            # mapping
            lambda y: {
                "country": country,
                "region": region,
                "year": int(y),
                "gdp": float(row[y]),
            },
            # filtering + appending
            filter(lambda k: k.isdigit() and row[k] != "", row.keys()),
        )
    )

