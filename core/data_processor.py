# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> data_processor.py

> Second logical part of the program
> Obtains formatted data from the data_loader function.
> Filters and aligns data from the given columns as required.
"""

import hashlib

from typing import List,Dict
from .protocols import ToStream, FromStream

##############################################################################
# Transformation Engine Class
#
# Recieving Data from Input thingy
# Basically implements functionality to:
#   - get data
#   - transform and transmit data
#       - reshape data
#       - verify data integrity
#       - send to telemetry if valid
#   - rename the columns and map to programmed ones
class TransformationEngine:

    # init data
    def __init__(self,config:Dict,service:FromStream,service2:ToStream)->None:
        self.config = config
        self.service = service
        self.service2 = service2
    
    # transform and transmit data
    def execute(self):

        # neeed to read forever
        while True:

            # get data
            raw_data = self.service.PickFromStream()

            # send empty packet to aggregator if you get an empty one
            if raw_data is None:
                print("[Core]: Worker done.")
                self.service2.SendToStream((None,None))
                break
            
            # reshape data (generic kyun keh SDA)
            reshaped_data = self.fix_fieldnames(self.config,raw_data)

            # check data integrity
            if(self.verify_security_hash(self.config,reshaped_data) == False):
                # if failed, print that we dropped it
                print(f"[Processor]: DROPPED ({
                      reshaped_data.get('metric_value','?')
                }), HASH {
                      str(reshaped_data.get('security_hash','????'))[-4:]
                }")
                # and don't do anything else on this packet
                continue

            # transmit to telemetry
            for i in reshaped_data.values():
                # need to ensure that this is a float
                # errors without this check
                if type(i) == float:
                    self.service2.SendToStream(
                            # avg    , data_packet
                            (float(i), reshaped_data)
                    )
                    break

    ###############################################################################
    # fixing colunm names
    #
    # Convert source_name columns into their implemented entity names
    # based entirely on project doc. very generic
    #
    # Columns:
    #   - entity_name
    #   - time_period
    #   - metric_value
    #   - security_hash
    #
    # ARG: dict instance, configuration file 
    # RET: dict instance
    def fix_fieldnames(self,config,row):

        result = {}
        type_map = {
            "integer": int,
            "float": float,
            "string": str,
            "bool": bool
        }

        # for every row of source:
        #   - map source col to programmed col
        #   - get correct data type for it
        #   - cast it to that type
        for n in config.get("schema_mapping").get("columns"):
            result[n["internal_mapping"]] = row[n["source_name"]]
            cast_function = type_map.get(n["data_type"]) 
            result[n["internal_mapping"]] = cast_function(result[n["internal_mapping"]])

        return result

    ###############################################################################
    # verifying data integrity
    #
    # it verifies Security hash of packet being received 
    #
    # ARG: row [dict instance], configuration file
    # RET: boolean
    def verify_security_hash(self,config,row)->bool:
        computed_hash = hashlib.pbkdf2_hmac(
            hash_name = "sha256",

            password = config.get("processing").get("stateless_tasks").get("secret_key").encode("utf-8"),
            
            salt = f"{round(float(row.get("metric_value")),2):.2f}".encode("utf-8"),

            iterations = config.get("processing").get("stateless_tasks").get("iterations")
        )
        return computed_hash.hex() == row.get("security_hash")
