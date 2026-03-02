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
from typing import List,Dict
from core.protocols import PipelineService, DataSink
from .compute_operations import *

##############################################################################
# Recieving Data from Input thingy:

class TransformationEngine(PipelineService):
    def __init__(self,config:Dict,sink:DataSink):
        self.config = config
        self.sink = sink
    
    #working on data
    def execute(self,raw_data:List[Dict]):
        
        
        target = self.config.get("region")
        year  = self.config.get("year")
    
        reshaped_data = self.reshape_data(raw_data)
        filtered_data = self.filter_data(reshaped_data,target,year)
        
        op = self.config.get("operation")
        
        results = self.compute_stat(filtered_data,op,reshaped_data,self.config)
        
    #time to send data to output fileee
        self.sink.write(results,self.config,filtered_data,reshaped_data)


###############################################################################
# Data Realignment Function
#
# Convert wide-year columns into:
# Country | Region | Year | GDP
#
# ARG: rows (list)
# RET: rows (list)
    def reshape_data(self,rows):
        return [item for row in rows for item in self.expand_row(row)]

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
    def filter_data(self,data, target, year, row_type=None):
        is_target_country = self.is_country(target)

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
# Row Consolidation Function, Called in reshape_data() for each row individually
#
# The years in the dataset are all displayed as separate columns, which is hard to work with
# Therefore this function integrates them as one column, by grouping their respective
# GDPs into a list.
#
# ARG: row (list)
# RET: row (list)
    def expand_row(self,row):
        # Holding names of dataset columns
        country = row["Country Name"]
        region = row["Continent"]
        # Figuring out the type for the region
        row_type = "country" if self.is_country(country) else "region"
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
                filter(lambda k: k.isdigit() and (row[k] != "" and row[k] != None), row.keys()),
            )
        )
###############################################################################
# Country vs Region Checking Function
#
# Helper function to be used in separation of data
#
# ARG: name (str)
# RET: is_country (bool)
    def is_country(self,name):
        try:
            pycountry.countries.lookup(name)
            return True
        except LookupError:
            return False
            
###############################################################################
# Computation Dispatcher
#
# Builds a uniform context dict and delegates to the matching function
# in OPERATIONS.  The caller (main.py) passes the full reshaped dataset
# and the raw config so that operations with wider scope (multi-year,
# global, etc.) have everything they need.
#
# Range fields are derived from config["year"], not read from config,
# so config.json stays in its original 4-field format:
#
#   year_start   = year - LOOKBACK_YEARS   (default: 10-year window)
#   year_end     = year
#   decline_years= DECLINE_WINDOW          (default: 5 consecutive years)
#
# Supported operation keys: see src/compute_operations.OPERATIONS
#
# ARG: filtered  (list)  : rows pre-filtered to config region + year
#      operation (str)   : config["operation"] key
#      reshaped  (list)  : full dataset (all years, all rows)
#      config    (dict)  : raw config dict from config.json
# RET: result    (any)   : type depends on operation; see compute_operations.py
    def compute_stat(self,filtered, operation, reshaped=None, config=None):
        if reshaped is None:
            reshaped = []
        if config is None:
            config = {}

        if operation not in OPERATIONS:
            raise ValueError(
                f"Unknown operation '{operation}'. "
                f"Valid operations: {sorted(OPERATIONS.keys())}"
            )

        # Internal defaults — derived from year, not read from config.json
        LOOKBACK_YEARS = 10
        DECLINE_WINDOW = 5

        year = config.get("year", 0)

        ctx = {
            "filtered"     : filtered,
            "reshaped"     : reshaped,
            "region"       : config.get("region", ""),
            "year"         : year,
            "year_start"   : year - LOOKBACK_YEARS,
            "year_end"     : year,
            "decline_years": DECLINE_WINDOW,
        }

        return OPERATIONS[operation](ctx)
