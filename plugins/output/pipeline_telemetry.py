# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> plugins/output/pipeline_telemetry.py

> the subject part of Observer Pattern
> Polls queue sizes and sends all attached observers a snapshot.
"""

import time

from typing import List, Dict

###############################################################################
# PipelineTelemetry
#
# This is th subject. It:
#   - holds references to the queues
#   - polls their sizes on an interval
#   - broadcasts a snapshot to every attached thing
#
# ARG: queues (dict), max_size (int), poll_interval (float)
class PipelineTelemetry:

    # inits the params
    def __init__(self, queues: Dict, max_size: int, poll_interval: float = 0.5) -> None:
        self.queues = queues
        self.max_size = max_size
        self.poll_interval = poll_interval
        self._observers = []

    ###########################################################################
    # subscribe
    #
    # Registers an observer to receive telemetry snapshots.
    # basically appends the observer to the list
    #
    # All observers ned to have update() implemented
    #
    # ARG: observer
    # RET:
    def subscribe(self, observer) -> None:
        self._observers.append(observer)

    ###########################################################################
    # _notify helper
    #
    # sneds the latest snapshot to every registered observer.
    #
    # ARG: snapshot
    # RET:
    def _notify(self, snapshot: Dict) -> None:
        for observer in self._observers:
            observer.update(snapshot)

    ###########################################################################
    # run loop
    #
    # works by daemonizing itself away. It:
    #   - makes the snapshot
    #   - notifies the observers
    #   - sleeps until next snapshot
    def run(self) -> None:
        while True:
            snapshot = {
                label: q.get_size()
                for label, q in self.queues.items()
            }
            self._notify(snapshot)
            time.sleep(self.poll_interval)
