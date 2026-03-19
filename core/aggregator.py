# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> core/aggregator.py

> Stateful aggregation node of all the core engines
> Doing sliding window avgs and aggregation of processed data
> in here. This is basically the imperitive shell part of the requirements
"""

from typing import List, Dict
from .protocols import FromStream, ToStream


###############################################################################
# Functional Core
# 
# Does the sliding average and window updations
# Also, simply does not even care what the data is
# it is dumb and stupid. Just like SDA :)
#
# ARG: window (list), new_value (float), window_size (int)
# RET: tupel (new_window (list), average (float))
def compute_running_average(window: List[float], new_value: float, window_size: int):
    new_window = (window + [new_value])[-window_size:]
    average = sum(new_window) / len(new_window)
    return new_window, average


###############################################################################
# Aggregator Class
#
# This is the imperitive shell. It does whatever SDA teaches us not to do,
# because, at the end of the day, SOMEone has to go and write the loops.
#
# ARG: config (dict), service (FromStream), service2 (ToStream)
class Aggregator:

    def __init__(self, config: Dict, service: FromStream, service2: ToStream) -> None:
        self.config = config
        self.service = service
        self.service2 = service2
        self.window_size = config.get("processing").get("stateful_tasks").get("running_average_window_size")
        self.No_of_cores = config.get("pipeline_dynamics").get("core_parallelism")
        self.termination_count = 0
        self.window = []

    def run(self):
        while True:
            # extract from the tuple
            metric_value, data = self.service.PickFromStream()

            # Basically poll the cores continously by checking if the pipeline is
            # sending empty packets. One per core is fine. Cuz we can then mark that
            # one as terminated. But if there are more, than yeah. It means all you
            # get from that point onwards are jsut empty packets, which means the
            # aggregator is now done
            if data is None:
                self.termination_count += 1
                if self.termination_count >= self.No_of_cores:
                    print("[Aggregator]: All workers reported back. Cores done.")
                    # need to tell the output that we have an empty packet
                    self.service2.SendToStream((None, None))
                    break
                continue

            # Imperative Shell calls the Functional Core here
            # It makes that compute function.. compute. Yeah.
            self.window, average = compute_running_average(
                self.window, metric_value, self.window_size
            )
            
            # send the average as well as data over to next module
            self.service2.SendToStream((average, data))
