# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> src/data_loader.py

> First logical part of the program
> Obtains the dataset file, and loads the data in csv format
> Works independant of the Operating System
"""

# External Dependancies
import json
import csv
import os
from core.protocols import PipelineService
from typing import List,Dict



###############################################################################
# Input Manager Class
#
# Takes config file as argument
# Returns csv,json based on config file specifications
#
# ARG: config (dict)
# RET: data (list) 

class InputManager:
    
    def __init__(self,config:Dict,service:PipelineService):
        self.config = config
        self.service = service
    
    
    #now based on config file, relevant loading function would be called:
    def run(self):
        input = self.config.get("input")
        path = self.config.get("path")
        year = self.config.get("year")
        continent = self.config.get("continent")
        
        if input == "csv":
            data = self.load_gdp_data_csv(path)
        elif input == "json":
            data = self.load_gdp_data_json(path)
        else:
            raise ValueError(f"Unknown input type in json file : {input}")
            
        #time to send raw data to coree-->
        self.service.execute(data)
        
###############################################################################
# Data loader function
#
# Takes filepath as argument
# Returns csv data
#
# ARG: filepath (str)
# RET: csv data (list)
    def load_gdp_data_csv(self,filepath):
        # Error handling
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        # Read and return as list
        with open(filepath, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            return list(reader)

#use of DictReader has been avoided to standardize data and not do conversions in core
#Thus input reader, manually reads data and converts it into appropriate data types before 
#submitting it as a key,value pair in dictionary
    
###############################################################################
# Data loader function
#
# Takes filepath as argument
# Returns json data
#
# ARG: filepath (str)
# RET: json data (list)
    def load_gdp_data_json(self,filepath):
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"json file not found: {filepath}")
        # Read and return as list
        with open(filepath, encoding="utf-8") as f:
            reader = json.load(f)
            return reader
            
