# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> src/data_loader.py

> First logical part of the program
> Obtains the dataset file, and streams data row-by-row into the pipeline.
> Works independent of the Operating System.
"""

import json
import time
import csv
import os

from core.protocols import ToStream
from typing import Dict


###############################################################################
# Input Manager Class
#
# Takes config file as argument
# Streams rows one-by-one into the pipeline with configured delay between them
#
# ARG: config (dict), service (ToStream)
class InputManager:

    def __init__(self, config: Dict, service: ToStream):
        self.config = config
        self.service = service

    ###############################################################################
    # run the accessing process
    #
    # Not the actual reader, really..
    # The real readers are the cSV and JSON helpers defined at the bottom
    #
    # Attempt at asynchronous (not really, cuz teacher removed the requirement) reading.
    # It reads like this:
    #   - reads one row
    #   - Sends off the packet
    #   - Sleeps for the confighured time
    #   - reads next row and then repeats
    def run(self):
        
        # path to file
        path = self.config.get("dataset_path")
        
        # check if CSV or JSON
        if path.endswith(".csv"):
            self._stream_csv(path)
        elif path.endswith(".json"):
            self._stream_json(path)
        else:
            raise ValueError(f"Unsupported file format: {path}")

        # if the execution thread goes past this comment, then that means we have
        # completely read the file
        # So we can now send the cores the signal to stop polling for a new packet
        for i in range(self.config.get("pipeline_dynamics").get("core_parallelism")):
            self.service.SendToStream(None)

    ###############################################################################
    # _stream_csv
    #
    # Does the reading for csv files
    #
    # ARG: filepath (str)
    def _stream_csv(self, filepath):
        # check i f file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"CSV file not found: {filepath}")
        # prepare to sleep
        delay = self.config.get("pipeline_dynamics").get("input_delay_seconds")
        # open the file
        with open(filepath, newline="", encoding="utf-8") as f:
            # start reading the file
            reader = csv.DictReader(f)
            # read row by row
            for row in reader:
                # send row to stream
                self.service.SendToStream(row)
                # sleep in between rows
                time.sleep(delay)

    ###############################################################################
    # _stream_json
    #
    # Does the reading for json files
    #
    # ARG: filepath (str)
    def _stream_json(self, filepath):
        # chekc if file exists
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"JSON file not found: {filepath}")
        # prep to sleep
        delay = self.config.get("pipeline_dynamics").get("input_delay_seconds")
        # open the file
        with open(filepath, encoding="utf-8") as f:
            records = json.load(f)
        # read row by row
        for record in records:
            # send row to stream
            self.service.SendToStream(record)
            # sleep as needed
            time.sleep(delay)
