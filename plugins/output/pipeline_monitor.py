# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> plugins/output/pipeline_monitor.py

> Observer Pattern implemented here
> attaches itself to PipelineTelemetry and reacts to snapshots
> by updating the actual, live updating matplotlib progress bars.
"""

import time
import matplotlib.pyplot as plt

from multiprocessing import Process
from .pipeline_telemetry import PipelineTelemetry


###############################################################################
# Pipeline Monitor Class
#
# This is the Observer interface. It does the snapshots
# On each notify call from the thing it attaches to, it goes to mem and redraws the
# queue size bars.
class PipelineMonitor:

    # initalize the params
    def __init__(self, queues: dict, max_size: int, poll_interval: float = 0.5) -> None:
        self.queues = queues
        self.max_size = max_size
        self.poll_interval = poll_interval
        self.process = None
        self.bars = {}
        self.figure = None
    
    # obvious
    def start(self) -> None:
        self.process = Process(target=self._run_monitor, daemon=True)
        self.process.start()

    # obvious
    def stop(self) -> None:
        self.process.terminate()

    ###########################################################################
    # _run_monitor helper
    #
    # Entry point for the monitor process.
    # Sets up the plot, creates the Subject, subscribes self, and aloso starts polling.
    def _run_monitor(self) -> None:
        self._setup_plot()
        telemetry = PipelineTelemetry(self.queues, self.max_size, self.poll_interval)
        telemetry.subscribe(self)
        telemetry.run()

    # god awful nesting:

    # setup helper for run helper
    def _setup_plot(self) -> None:
        
        # Need to have concurrent charting
        plt.ion()
        labels = list(self.queues.keys())

        # begin the figure specs
        self.figure, axes = plt.subplots(
            1, len(labels), figsize=(7, len(labels) * 1.2 + 0.5)
        )
        self.figure.suptitle("Pipeline Monitor - Queue Sizes", fontweight="bold", fontsize=11)

        # ensure axes is always iterable even for a single subplot
        if len(labels) == 1:
            axes = [axes]

        for a, l in zip(axes, labels):
            a.set_xlim(0, self.max_size)
            a.set_ylim(-0.4, 0.4)
            a.set_yticks([])
            a.set_xlabel("Queue size", fontsize=8)
            # ensure the thing stays on screen (still causes reloading of page dimesions)
            # how do I even stop that. I give up.
            a.set_title(l, fontsize=9, loc="left", pad=2)
            a.barh(0, self.max_size, height=0.4, color="#e0e0e0")
            bar = a.barh(0, 0, color="#2ecc71")
            self.bars[l] = bar

        # trying to condense
        plt.tight_layout(pad=1.5)

        # draw gracefully
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    ###############################################################################
    # update
    #
    # lets us update the monitored value sin the bars
    #
    # ARG: snapshot
    # RET:
    def update(self, snapshot: dict) -> None:
        # extracts the snapshotted tuple
        for label, size in snapshot.items():
            # if empty, skip
            if label not in self.bars:
                continue
            # decide on a percentage based on if size is > 0
            pct = size / self.max_size if self.max_size else 0
            # assign labels and colors
            self.bars[label][0].set_width(max(size, 0.01))
            self.bars[label][0].set_color(self._color(pct))

        # only redraws changed regions (very optimal)
        self.figure.canvas.draw_idle()
        self.figure.canvas.flush_events()
        time.sleep(self.poll_interval)

    ################################################################################
    # _color helper
    #
    # decides colors if the bars
    # slowly go from green to red in a lovely little gradient
    #
    # ARG: percentages (float)
    # RET: hex colours
    def _color(self, pct: float) -> str:
        if pct < 0.1:
            return "#319413"
        elif pct < 0.2:
            return "#5fa411"
        elif pct < 0.3:
            return "#8eb40f"
        elif pct < 0.4:
            return "#bcc40d"
        elif pct < 0.5:
            return "#ead40b"
        elif pct < 0.6:
            return "#f1c40f"
        elif pct < 0.7:
            return "#ec9e16"
        elif pct < 0.8:
            return "#e8781e"
        elif pct < 0.9:
            return "#e45225"
        else:
            return "#e74c3c"
