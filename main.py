# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> main.py

> Entry Point
> Controller for all operations
"""

import json

from core.data_processor import TransformationEngine
from core.aggregator import Aggregator

from plugins.input.data_loader import InputManager
from plugins.output.protocols import OutputManager
from plugins.output.pipeline_monitor import PipelineMonitor

from stream.Stream import QueueImplementation
from multiprocessing import Process

CONFIG_FILE = "config.json"

###############################################################################
# Configuration Loader Function
#
# Handles the file descriptors, loads contents into memory after parsing as json
#
# ARG:
# RET: json stream
def load_config():
    with open(CONFIG_FILE) as f:
        return json.load(f)

###############################################################################
# Main
#
# Abandon all hope, ye who enter here..
#
# ARG:
# RET:
def bootstrap():

    # letting the TA know (hope he doesn't get confused bruh)
    print("\n\n\t\tVisuals will be shown in your BROWSER.")
    print("\t\tA window to http://localhost:5000/ should open automatically.")
    print("\t\tIf it doesn't please copy and paste the url in your browser manually.\n")

    try:
    # 0. FETCH DATA
        config = load_config()

    # 1. STREAMS HANDLING

        # > 1(a). Input         -> Core
        RawDataStream = QueueImplementation(
                config.get("pipeline_dynamics").get("stream_queue_max_size")
        )
        # > 1(b). Core workers  -> Aggregator
        IntermediateStream = QueueImplementation(
                config.get("pipeline_dynamics").get("stream_queue_max_size")
        )
        # > 1(c). Aggregator    -> Output
        ProcessedDataStream = QueueImplementation(
                config.get("pipeline_dynamics").get("stream_queue_max_size")
        )

        # boolean dict for visualization
        map_to_streams = {
            "show_raw_stream":          "RawDataStream",
            "show_intermediate_stream": "IntermediateStream",
            "show_processed_stream":    "ProcessedDataStream"
        }

        # streams dict for pipeline monitor
        stream_map = {
            "RawDataStream":        RawDataStream,
            "IntermediateStream":   IntermediateStream,
            "ProcessedDataStream":  ProcessedDataStream
        }

        # check which stream to keep in visualizations
        for key in list(map_to_streams.keys()):
            if config["visualizations"]["telemetry"].get(key) == False:
                del stream_map[map_to_streams[key]]

        # get the monitor in running
        queues = PipelineMonitor(
                stream_map,
                config.get("pipeline_dynamics").get("stream_queue_max_size")
        )

    # 2. MODULE WIRING

        ############
        # i. Input #
        ############
        reader = InputManager(config, RawDataStream)
        
        ############
        # ii. Core #
        ############

        # Engines (Workers)
        core_engines = []
        for i in range(config.get("pipeline_dynamics").get("core_parallelism")):
            engine = TransformationEngine(config, RawDataStream, IntermediateStream)
            core_engines.append(engine)

        # Aggregator (imperitive shell)
        aggregator = Aggregator(config, IntermediateStream, ProcessedDataStream)

        ###############
        # iii. Output #
        ###############
        output_manager = OutputManager(config, ProcessedDataStream, stream_map)

    # 3. PROCESS MANAGEMENT

        # Creation
        Input = Process(target=reader.run)
        AggregatorProcess = Process(target=aggregator.run)
        Output = Process(target=output_manager._choose_sink)

        # Starting queues (allows us to manage all modules as async)
        queues.start()

        # Starting modules
        Output.start()                          # output

        AggregatorProcess.start()               # aggregator
        
        Process_cores = []                      # core engines
        for engine in core_engines:
            p = Process(target=engine.execute)
            Process_cores.append(p)
            p.start()

        Input.start()                           # input

        # Ending processes (by joining them with bootstrap again)
        Input.join()                            # input
        for p in Process_cores:                 # core engines
            p.join()
        AggregatorProcess.join()                # aggregator
        Output.join()                           # output
        queues.stop()                           # queues

    # handle errors gracefully (print stack trace)
    except Exception as e:
        import traceback
        traceback.print_exc()


#######
# Run #
#######
if __name__ == "__main__":
    bootstrap()
