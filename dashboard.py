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
from data_processor import is_country
from data_processor import reshape_data, filter_data, compute_stat, split_by_type

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
def show_dashboard(config, filtered_data, result, data_scope, reshaped):
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

    # Region-wise plots
    names = list(map(lambda d: d["name"], filtered_data))
    gdps = list(map(lambda d: d["gdp"], filtered_data))

    # Bar Chart
    plt.figure()
    plt.bar(names, gdps)
    plt.title(f"{data_scope} GDP Comparison")
    plt.xlabel(data_scope)
    plt.ylabel("GDP")
    plt.xticks(rotation=90)

    # Pie Chart
    plt.figure()
    plt.pie(
        gdps,
        labels=names,
        autopct="%1.1f%%",
        startangle=140
    )
    plt.title(f"{data_scope} GDP Distribution")
    plt.tight_layout()

    # Year-wise plots
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

    # Line plot
    plt.figure()
    plt.plot(years, yearly_gdp)
    plt.title("Year-wise GDP Trend")
    plt.xlabel("Year")
    plt.ylabel("GDP")

    # Lollipop
    plt.figure(figsize=(12,6))
    plt.hlines(y=names, xmin=0, xmax=gdps, color='skyblue')
    plt.plot(gdps, names, "o", color="orange")
    plt.title(f"Country GDPs in {config['year']}")
    plt.xlabel("GDP (Current US$)")
    plt.ylabel("Country")
    plt.tight_layout()

    # dot plot + bubble plot
    plt.figure(figsize=(12,6))
    plt.scatter(names, gdps, color="green", s=50)  # s=size of marker
    plt.title(f"Country GDPs in {config['year']}")
    plt.xlabel("Country")
    plt.ylabel("GDP (Current US$)")
    plt.xticks(rotation=90)
    plt.tight_layout()
    sizes = [g/1e10 for g in gdps]  # scale down for marker size
    plt.scatter(names, gdps, s=sizes, alpha=0.6)
    plt.xticks(rotation=90)
    plt.ylabel("GDP (Current US$)")
    plt.title(f"Country GDPs in {config['year']}")
    plt.tight_layout()


    # treemap
    import squarify
    # Year-specific slice
    year_slice = list(
        filter(
            lambda d: d["year"] == config["year"] and d["type"] == "country",
            reshaped
        )
    )
    countries = list(map(lambda d: d["name"], year_slice))
    gdps = list(map(lambda d: d["gdp"], year_slice))

    plt.figure(figsize=(12,8))
    squarify.plot(
        sizes=gdps,
        label=countries,
        alpha=0.8,
        color=plt.cm.tab20.colors  # optional color palette
    )
    plt.title(f"Country GDP Treemap ({config['year']})")
    plt.axis('off')
    plt.tight_layout()

    # Wordcloud
    from wordcloud import WordCloud

    # Build dictionary: country → GDP
    gdp_dict = {d["name"]: d["gdp"] for d in year_slice}

    wordcloud = WordCloud(
        width=1200,
        height=600,
        background_color='white',
        colormap='tab20',
        normalize_plurals=False
    ).generate_from_frequencies(gdp_dict)

    plt.figure(figsize=(15,8))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(f"Country GDP Word Cloud ({config['year']})")

    # Slope chart
    # Pick previous year (if exists)
    prev_year = config["year"] - 1
    prev_slice = list(
        filter(
            lambda d: d["year"] == prev_year and d["type"] == "country" and d["name"] in countries,
            reshaped
        )
    )
    prev_gdp_dict = {d["name"]: d["gdp"] for d in prev_slice}
    curr_gdp_dict = {d["name"]: d["gdp"] for d in year_slice}

    plt.figure(figsize=(12,8))

    for country in countries:
        if country in prev_gdp_dict:
            plt.plot([prev_year, config["year"]],
                     [prev_gdp_dict[country], curr_gdp_dict[country]],
                     marker='o', label=country)
            
    plt.xlabel("Year")
    plt.ylabel("GDP (Current US$)")
    plt.title(f"Slope Chart: GDP Change {prev_year} → {config['year']}")
    plt.grid(True)
    plt.tight_layout()

        
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
