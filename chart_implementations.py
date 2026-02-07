import matplotlib.pyplot as plt

def bar_chart(names, gdps, data_scope):
    plt.figure()
    plt.bar(names, gdps)
    plt.title(f"{data_scope} GDP Comparison")
    plt.xlabel(data_scope)
    plt.ylabel("GDP")
    plt.xticks(rotation=90)
    plt.show()

def pie_chart(names, gdps, data_scope):
    plt.figure()
    plt.pie(
        gdps,
        labels=names,
        autopct="%1.1f%%",
        startangle=140
    )
    plt.title(f"{data_scope} GDP Distribution")
    plt.tight_layout()
    plt.show()

def line_plot(years, yearly_gdp):
    plt.figure()
    plt.plot(years, yearly_gdp)
    plt.title("Year-wise GDP Trend")
    plt.xlabel("Year")
    plt.ylabel("GDP")
    plt.show()

def lollipop_plot(names, gdps, config):
    plt.figure(figsize=(12,6))
    plt.hlines(y=names, xmin=0, xmax=gdps, color='skyblue')
    plt.plot(gdps, names, "o", color="orange")
    plt.title(f"Country GDPs in {config['year']}")
    plt.xlabel("GDP (Current US$)")
    plt.ylabel("Country")
    plt.tight_layout()
    plt.show()

def dot_plot(names, gdps, config):
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
    plt.show()

def tree_map(year_slice, config):
    import squarify
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
    plt.show()

def word_cloud(year_slice, config):
    from wordcloud import WordCloud
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
    plt.ylabel("GDP (Current US$)")
    plt.title(f"Slope Chart: GDP Change {prev_year} → {config['year']}")
    plt.grid(True)
    plt.tight_layout()
    plt.show()

