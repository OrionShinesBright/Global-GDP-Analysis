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
    try:
        #0. FETCH
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
        
    except Exception as e:
        import traceback
        traceback.print_exc()


#######
# Run #
#######
if __name__ == "__main__":
    bootstrap()
