# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> helpers/chart_implementations.py

> Helper Module, to be called from the dashboard
> Creates the graphs and charts, handles matplotlib internals.
> Handles all visualizations modularly
"""

# Main Graphing Library
import matplotlib.pyplot as plt
# For tree_map graph type
import squarify
# For word_cloud graph type
from wordcloud import WordCloud


#
# Bar chart - Region
#
def bar_chart(names, gdps, data_scope):
    if data_scope == "Country-wise":
        print("\n\n\t\033[0;31mChosen region is a country\n\tRegion wise bar chart is not a good statistic for this\033[0;0m\n\n")
        input("[Press Enter to Continue]")
    plt.figure(figsize=(12, 6))
    plt.bar(names, gdps, width=0.6)
    plt.ylim(0, max(gdps) * 1.25)
    plt.title(f"{data_scope} GDP Comparison")
    plt.xlabel(data_scope)
    plt.ylabel("GDP")
    plt.xticks(rotation=90, ha="right")
    plt.tight_layout()
    plt.show()


#
# Pie Chart - Region
#
def pie_chart(names, gdps, data_scope):
    if data_scope == "Country-wise":
        print("\n\n\t\033[0;31mChosen region is a country\n\tRegion wise pie chart is not a good statistic for this\033[0;0m\n\n")
        input("[Press Enter to Continue]")
    plt.figure()
    wedges, _, autotexts = plt.pie(
        gdps,
        autopct="%1.1f%%",
        startangle=140,
        pctdistance=0.8
    )
    # Hide percentage labels below threshold
    for autotext in autotexts:
        pct = float(autotext.get_text().replace('%', ''))
        if pct < 2:
            autotext.set_text("")
    plt.legend(
        wedges,
        names,
        title="Categories",
        loc="center left",
        bbox_to_anchor=(1, 0.5)
    )
    plt.title(f"{data_scope} GDP Distribution")
    plt.subplots_adjust(right=0.75)
    plt.show()


#
# Line Plot - Year
#
def line_plot(years, yearly_gdp):
    cleaned = [
        (y, g) for y, g in zip(years, yearly_gdp)
        if g is not None and g > 0
    ]
    if not cleaned:
        print("\n\n\t\033[0;31mNo valid yearly GDP data to plot\033[0;0m\n")
        input("[Press Enter to continue]")
        return
    years, yearly_gdp = zip(*sorted(cleaned))
    plt.figure(figsize=(8, 5))
    plt.plot(years, yearly_gdp, marker="o")
    plt.title("Year-wise GDP Trend")
    plt.xlabel("Year")
    plt.ylabel("GDP")
    plt.tight_layout()
    plt.show()



#
# Lollipop Chart - Region
#
def lollipop_plot(names, gdps, config, data_scope):
    if data_scope == "Country-wise":
        print("\n\n\t\033[0;31mChosen region is a country\n\tRegion wise lollipop chart is not a good statistic for this\033[0;0m\n\n")
        input("[Press Enter to Continue]")
    plt.figure(figsize=(12,6))
    plt.hlines(y=names, xmin=0, xmax=gdps, color='skyblue')
    plt.plot(gdps, names, "o", color="orange")
    plt.title(f"Country GDPs in {config['year']}")
    plt.xlabel("GDP (Current US$ [in Billions])")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.show()


#
# Dot + Bubble Plot - Region
#
def dot_plot(names, gdps, config, data_scope):
    if data_scope == "Country-wise":
        print("\n\n\t\033[0;31mChosen region is a country\n\tRegion wise dot plot is not a good statistic for this\033[0;0m\n\n")
        input("[Press Enter to Continue]")
    plt.figure(figsize=(12,6))
    plt.scatter(names, gdps, color="green", s=50)  # s=size of marker
    plt.title(f"Country GDPs in {config['year']}")
    plt.xlabel("Country")
    plt.ylabel("GDP (Current US$ [in Billions])")
    plt.xticks(rotation=90)
    plt.tight_layout()
    sizes = [g/1e10 for g in gdps]  # scale down for marker size
    plt.scatter(names, gdps, s=sizes, alpha=0.6)
    plt.xticks(rotation=90)
    plt.ylabel("GDP (Current US$ [in Billions])")
    plt.title(f"Country GDPs in {config['year']}")
    plt.tight_layout()
    plt.show()


#
# Tree Map - Global
#
def tree_map(year_slice, config):
    print("\n\n\t\033[0;32mThis is a special kind of graph\n\tIt's scope is global, and displays distribution of GDP in chosen year\033[0;0m\n\n")
    input("[Press Enter to Continue]")

    countries = list(map(lambda d: d["name"], year_slice))
    gdps = list(map(lambda d: d["gdp"], year_slice))

    # Only label countries contributing >1.5% of total GDP
    total = sum(gdps)
    labels = [c if g/total > 0.015 else "" for c, g in zip(countries, gdps)]

    plt.figure(figsize=(12,8))
    squarify.plot(
        sizes=gdps,
        label=labels,
        alpha=0.8,
        color=plt.cm.tab20.colors
    )
    plt.title(f"Country GDP Treemap ({config['year']})")
    plt.axis('off')
    plt.tight_layout()
    plt.show()


#
# Word Cloud - Global
#
def word_cloud(year_slice, config):
    print("\n\n\t\033[0;32mThis is a special kind of graph\n\tIt's scope is global, and displays distribution of GDP in chosen year\033[0;0m\n\n")
    input("[Press Enter to Continue]")
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
    plt.show()


#
# Slope Chart - Year
#
def slope_chart(config, reshaped, year_slice):
    prev_year = config["year"] - 1
    countries = list(map(lambda d: d["name"], year_slice))
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
    plt.ylabel("GDP (Current US$ [in Billions])")
    plt.title(f"Slope Chart: GDP Change {prev_year} → {config['year']}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()
