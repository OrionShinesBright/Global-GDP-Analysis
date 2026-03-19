# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> plugins/input/protocols.py

> Defines the outgoing protcols. Handles the
> choice of sink that needs to be activated
"""

from __future__ import annotations
from typing import List,Dict, TYPE_CHECKING

from .console_writer import ConsoleWriter
from .chart_writer import ChartWriter

from plugins.output.chart_implementations import _chart_store, _store_lock
from plugins.output.chart_implementations import register_queues

# conditional import
if TYPE_CHECKING:
    from core.protocols import ToStream, FromStream 

###############################################################################
# Outpput Manager Class
#
# Initializes the output-able parameters and also
# implements the functionality to choose the mode of output
class OutputManager:

    def __init__(self, config: Dict, service: FromStream, stream_map: dict) -> None:
        self.config     = config
        self.service    = service
        self.sink       = ConsoleWriter()
        self.chart      = ChartWriter()
        self.stream_map = stream_map
        self.count      = 0
    
    
    ###############################################################################
    # Choice of Sink
    #
    # implements the functionality to choose the mode of output
    #
    # ARG:
    # RET:
    def _choose_sink(self):
        # register the queues for monitoring
        register_queues(self.stream_map, self.config.get("pipeline_dynamics").get("stream_queue_max_size"))

        # begin output procedure instantiations
        from .console_writer import ConsoleWriter
        while True:
            # counter for total packets displayed
            self.count = self.count +1
            # extract tuple from incoming stream
            average,packetFromCore = self.service.PickFromStream()
            # handle empty packets
            if packetFromCore is None:
                print("[Output]: Termination Signal Received")
                break
            # else write it out to appropriate sink
            self.sink.write(packetFromCore,average,self.count)

            # get latest values out of the packets into a hashmap
            # this dict will be used in chart implementations and the
            # web server itself as well
            with _store_lock:
                _chart_store['__latest__'] = {
                    'entity_name':   packetFromCore.get('entity_name'),
                    'time_period':   packetFromCore.get('time_period'),
                    'metric_value':  packetFromCore.get('metric_value'),
                    'security_hash': packetFromCore.get('security_hash'),
                    'average':       average,
                    'count':         self.count
                }

            # get the charting process going
            for core_chart in self.config["visualizations"]["data_charts"]:
                # type A
                if core_chart["type"] == "real_time_line_graph_values":
                    self.chart.render(
                        core_chart["title"], core_chart["x_axis"], core_chart["y_axis"],
                        packetFromCore[core_chart["x_axis"]],
                        packetFromCore[core_chart["y_axis"]]
                    ) 
                # type B
                elif core_chart["type"] == "real_time_line_graph_average":        
                    self.chart.render(
                        core_chart["title"], core_chart["x_axis"], core_chart["y_axis"],
                        packetFromCore[core_chart["x_axis"]],
                        average
                    )
        # send the charts all the info so they may get plotted
        self.chart.finalize()  
