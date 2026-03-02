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

from core.protocols import DataSink
from typing import List,Dict

class ConsoleWriter(DataSink):
    def write(self,records,config:Dict,filtered_data,reshaped_data) -> None:
        self.config = config
        self.dashboard_info(records,self.config)
        
    def dashboard_info(self,result,config,data_scope = "Continent"):
        # dashboard visualization (TUI based)
        print(f"\t\033[0;90m╭────────────────────────────────────┬─────────────╮")
        print(f"\t\033[0;90m│ \033[0;34mDASHBOARD FOR WORLD BANK ANALYTICS \033[0;90m│ \033[0;31m1970 ─ 2020 \033[0;90m│")
        print(f"\t\033[0;90m╰────────────────────────────────────┴─────────────╯")
        print(f"\t\033[0;90m────────────┬───────────────────────────────────────")
        print(f"\t\033[0;90m  \033[0;92mScope     \033[0;90m│\t\033[0;93m{data_scope}")
        print(f"\t\033[0;90m  \033[0;92mRegion    \033[0;90m│\t\033[0;93m{config['region']}")
        print(f"\t\033[0;90m  \033[0;92mYear      \033[0;90m│\t\033[0;93m{config['year']}")
        print(f"\t\033[0;90m  \033[0;92mOperation \033[0;90m│\t\033[0;93m{config['operation']}")
        # Handle 'not found' error
        if result is None:
            print(f"\t\033[0;90m  \033[0;0mNo data available for this configuration.")
            print(f"\t\033[0;90m────────────────────────────────────────────────────")
            return
        # Print result of computation
        if type(result)==list and len(result)>=1:
            if type(result[0]) == tuple:
                print(f"\t\033[0;90m  \033[0;92mResult    \033[0;90m│\t\033[0;93mCountry:{result[0][0]}\t\t\tGdp:{result[0][1]}")
                if len(result) > 1 :
                    for i in range(len(result)-1):
                        print(f"\t\t\tCountry:{result[i+1][0]}\t\t\tGdp:{result[i+1][1]}")
            else:
                print(f"\t\033[0;90m  \033[0;92mResult    \033[0;90m│\t\033[0;93mCountry:{result[0]}")
                if len(result) > 1 :
                    for i in range(len(result)-1):
                        print(f"\t\t\tCountry:{result[i+1]}")
        else:
            print(f"\t\033[0;90m  \033[0;92mResult    \033[0;90m│\t\033[0;93m{result}", end = "")
        if data_scope == "Country-wise":
            print(f"(Single country stats are the GDP value itself)")
        else:
            print(f"")
        print(f"\t\033[0;90m────────────┴───────────────────────────────────────")
    
