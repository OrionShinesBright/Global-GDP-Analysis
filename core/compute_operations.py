# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> src/compute_operations.py

> Houses every compute_stat implementation.
> Registered into OPERATIONS dict at the bottom of the file.

> Each operation function receives the same uniform context dict:
>
>   cdict = {
>       "filtered"  : list[dict]   — rows scoped to config["region"] + config["year"],
>                                    type=="country" only  (may be empty)
>       "reshaped"  : list[dict]   — full dataset, all years, countries + regions
>       "region"    : str          — config["region"]
>       "year"      : int          — config["year"]
>       "year_start": int          — config.get("year_start", year)
>       "year_end"  : int          — config.get("year_end",   year)
>       "decline_years": int       — config.get("decline_years", 5)
>   }
>
> dashboard.py's format_result() handles all possible return shapes.
"""


###############################################################################
# Helpers

# Return all country-type rows whose region matches
def _countries_in_region(reshaped, region):
    return list(filter(
        lambda d: d["type"] == "country" and d["region"] == region,
        reshaped
    ))

# Return GDP float for a single country+year, or None if missing
def _gdp_for_country_year(reshaped, name, year):
    matches = list(filter(
        lambda d: d["type"] == "country" and d["name"] == name and d["year"] == year,
        reshaped
    ))
    return matches[0]["gdp"] if matches else None

# Inclusive list of years from year_start to year_end
def _year_range(cdict):
    return list(range(cdict["year_start"], cdict["year_end"] + 1))


###############################################################################
# 1. Top 10 Countries by GDP  (region + year)
#
# ARG: cdict (dict)
# RET: list[dict] (up to 10 rows, each with keys: name, region, year, gdp, type)
def op_top_10(cdict):
    data = cdict["filtered"]
    if not data:
        return []
    sorted_data = sorted(data, key=lambda d: d["gdp"], reverse=True)
    result = [(k["name"],k["gdp"]) for k in sorted_data[:10]]            
    return result


###############################################################################
# 2. Bottom 10 Countries by GDP  (region + year)
#
# ARG: cdict (dict)
# RET: list[dict] (up to 10 rows, each with keys: name, region, year, gdp, type)
def op_bottom_10(cdict):
    data = cdict["filtered"]
    if not data:
        return []
    sorted_data = sorted(data, key=lambda d: d["gdp"])
    return [(k["name"],k["gdp"]) for k in sorted_data[:10]]


###############################################################################
# 3. GDP Growth Rate of Each Country  (region, year_start -> year_end)
#
# Growth rate = (gdp_end - gdp_start) / gdp_start * 100
# Countries missing either endpoint are skipped.
#
# ARG: cdict (dict)
# RET: list[dict]  : sorted descending by rate
#                    keys: name (str), rate (float, percentage)
def op_growth_rate(cdict):
    reshaped   = cdict["reshaped"]
    region     = cdict["region"]
    year_start = cdict["year_start"]
    year_end   = cdict["year_end"]

    country_names = sorted(set(map(
        lambda d: d["name"],
        _countries_in_region(reshaped, region)
    )))

    def growth(name):
        gdp_s = _gdp_for_country_year(reshaped, name, year_start)
        gdp_e = _gdp_for_country_year(reshaped, name, year_end)
        if gdp_s is None or gdp_e is None or gdp_s == 0:
            return None
        return {"name": name, "rate": (gdp_e - gdp_s) / gdp_s * 100}

    results = list(filter(None, map(growth, country_names)))
    return sorted(results, key=lambda d: d["rate"], reverse=True)


###############################################################################
# 4. Average GDP by Continent  (year_start -> year_end)
#
# For each continent: average across all country-rows in the year range.
#
# ARG: cdict (dict)
# RET: dict[str -> float]{continent_name: avg_gdp}
def op_average_by_continent(cdict):
    reshaped   = cdict["reshaped"]
    year_start = cdict["year_start"]
    year_end   = cdict["year_end"]
    years      = set(_year_range(cdict))

    country_rows = list(filter(
        lambda d: d["type"] == "country" and d["year"] in years,
        reshaped
    ))

    # Group GDPs by continent
    continent_gdps = {}
    for row in country_rows:
        continent_gdps.setdefault(row["region"], []).append(row["gdp"])

    return [
        (continent, sum(gdps) / len(gdps))
        for continent, gdps in sorted(continent_gdps.items())
    ]


###############################################################################
# 5. Total Global GDP Trend  (year_start -> year_end)
#
# Reports the year-over-year percentage change in total global GDP across
# the date range.  Raw totals are an intermediate step only.
#
# ARG: cdict (dict)
# RET: list[tuple(int, float)]  -- [(year, pct_change), ...] sorted by year
#                                   pct_change is relative to the previous year;
#                                   the first year in the range has no entry.
def op_global_gdp_trend(cdict):
    reshaped = cdict["reshaped"]
    # Extend range by one year back so the first displayed year has a baseline
    years = list(range(cdict["year_start"] - 1, cdict["year_end"] + 1))

    def total_for_year(y):
        gdps = list(map(
            lambda d: d["gdp"],
            filter(lambda d: d["type"] == "country" and d["year"] == y, reshaped)
        ))
        return (y, sum(gdps)) if gdps else None

    raw = list(filter(None, map(total_for_year, years)))

    def pct_change(pair):
        (y_prev, gdp_prev), (y_curr, gdp_curr) = pair
        if gdp_prev == 0:
            return None
        return (y_curr, (gdp_curr - gdp_prev) / gdp_prev * 100)

    pairs = list(zip(raw, raw[1:]))
    return list(filter(None, map(pct_change, pairs)))


###############################################################################
# 6. Fastest Growing Continent  (year_start -> year_end)
#
# Measured by aggregate GDP growth rate across the period.
#
# ARG: cdict (dict)
# RET: str
def op_fastest_growing_continent(cdict):
    reshaped   = cdict["reshaped"]
    year_start = cdict["year_start"]
    year_end   = cdict["year_end"]

    continents = sorted(set(map(
        lambda d: d["region"],
        filter(lambda d: d["type"] == "country", reshaped)
    )))

    def continent_growth(continent):
        def gdp_sum_for_year(y):
            values = list(map(
                lambda d: d["gdp"],
                filter(
                    lambda d: d["type"] == "country"
                              and d["region"] == continent
                              and d["year"] == y,
                    reshaped
                )
            ))
            return sum(values) if values else None

        gdp_s = gdp_sum_for_year(year_start)
        gdp_e = gdp_sum_for_year(year_end)
        if gdp_s is None or gdp_e is None or gdp_s == 0:
            return None
        return (continent, (gdp_e - gdp_s) / gdp_s * 100)

    results = list(filter(None, map(continent_growth, continents)))
    if not results:
        return None
    return max(results, key=lambda t: t[1])[0]


###############################################################################
# 7. Countries with Consistent GDP Decline  (region, last decline_years years)
#
# A country qualifies if its GDP fell in every consecutive year-pair
# within the window [year - decline_years, year].
#
# ARG: cdict (dict)
# RET: list[str]
def op_consistent_decline(cdict):
    reshaped      = cdict["reshaped"]
    region        = cdict["region"]
    year_end      = cdict["year"]
    decline_years = cdict["decline_years"]
    window        = list(range(year_end - decline_years, year_end + 1))

    country_names = sorted(set(map(
        lambda d: d["name"],
        _countries_in_region(reshaped, region)
    )))

    def declined_consistently(name):
        gdps = list(map(
            lambda y: _gdp_for_country_year(reshaped, name, y),
            window
        ))
        # Need all years present
        if any(g is None for g in gdps):
            return False
        # Every consecutive pair must be strictly decreasing
        pairs = zip(gdps, gdps[1:])
        return all(prev > curr for prev, curr in pairs)

    return list(filter(declined_consistently, country_names))


###############################################################################
# 8. Contribution of Each Continent to Global GDP  (year_start -> year_end)
#
# Percentage share of each continent's total GDP vs. world total, averaged
# over the given year range.
#
# ARG: cdict (dict)
# RET: dict[str -> float]{continent_name: percentage_share}
def op_continent_contribution(cdict):
    reshaped   = cdict["reshaped"]
    year_start = cdict["year_start"]
    year_end   = cdict["year_end"]
    years      = set(_year_range(cdict))

    country_rows = list(filter(
        lambda d: d["type"] == "country" and d["year"] in years,
        reshaped
    ))

    if not country_rows:
        return {}

    # Sum GDPs by continent
    continent_totals = {}
    for row in country_rows:
        continent_totals[row["region"]] = (
            continent_totals.get(row["region"], 0.0) + row["gdp"]
        )

    global_total = sum(continent_totals.values())
    if global_total == 0:
        return {}

    return [
        (continent,(total / global_total) * 100)
        for continent, total in sorted(continent_totals.items())
    ]


###############################################################################
# Legacy operations

def op_average(cdict):
    """Average GDP across all rows in filtered data."""
    values = list(map(lambda d: d["gdp"], cdict["filtered"]))
    return sum(values) / len(values) if values else None


def op_sum(cdict):
    """Sum of GDP across all rows in filtered data."""
    values = list(map(lambda d: d["gdp"], cdict["filtered"]))
    return sum(values) if values else None


###############################################################################
# OPERATIONS registry
#
# Maps config["operation"] string -> function(cdict) -> result
#
OPERATIONS = {
    "average":                  op_average,
    "sum":                      op_sum,

    "top_10":                   op_top_10,
    "bottom_10":                op_bottom_10,
    "growth_rate":              op_growth_rate,
    "average_by_continent":     op_average_by_continent,
    "global_gdp_trend":         op_global_gdp_trend,
    "fastest_growing_continent": op_fastest_growing_continent,
    "consistent_decline":       op_consistent_decline,
    "continent_contribution":   op_continent_contribution,
}
