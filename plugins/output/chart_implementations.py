# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> helpers/chart_implementations.py

> Helper Module, to be called from the dashboard.
> Renders real-time line charts to in-memory PNG buffers
> Needed to do this because directly embedding the
> Matplotlib charts into web interfaces is very hard and required me to make
> weird web-queues and stuff like that. Can't be bothered to do that.
> So have come up with this, slightly less elegant solution.
"""

import io
import time
import threading

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt


###############################################################################
# Shared in-memory stores
#
# _chart_store : chart title (str) maps to latest PNG bytes (bytes)
# _queue_store : label (str) maps to QueueImplementation, for backpressure display
_chart_store   = {}

_queue_store   = {}
_max_q_size    = 50

_store_lock    = threading.Lock()

_server_started = False
_server_lock   = threading.Lock()

_chart_count      = 0
_chart_count_lock = threading.Lock()

# colors
_PALETTE = [
    '#6366f1',
    '#06b6d4',
    '#22c55e',
    '#f59e0b'
] 


###############################################################################
# register_queues
#
# this hands the references of the queeues to the web server so that
# it can implement the backpressure charts
#
# ARG: stream_map (dict), max_size (int)
def register_queues(stream_map: dict, max_size: int) -> None:
    global _max_q_size
    _queue_store.update(stream_map)
    _max_q_size = max_size


###############################################################################
# _ensure_server
#
# Starts the Flask dashboard thread exactly once, in a background thread
# so it does not block the caller.
def _ensure_server() -> None:
    global _server_started
    with _server_lock:
        if _server_started:
            return
        _server_started = True

    from plugins.output.web.server import start_server_thread
    t = threading.Thread(
        target=start_server_thread,
        args=(_chart_store, _queue_store, _store_lock, _max_q_size),
        daemon=True
    )
    t.start()
    # Brief pause so Flask is ready before the first chart update hits
    time.sleep(1.5)


###############################################################################
# Setup_line_plot
#
# Creates a styled matplotlib figure (dark theme).
# Triggers WEb server startup on first call.
#
# ARG: title (str), x_label (str), y_label (str)
# RET: figure, axis, line
def Setup_line_plot(title, x_label, y_label):
    global _chart_count

    # get the server going
    _ensure_server()

    # make sure we know that the chart has instatiated
    with _chart_count_lock:
        color = _PALETTE[_chart_count % len(_PALETTE)]
        _chart_count += 1

    # extract out the elements
    figure, axis = plt.subplots(figsize=(8, 5))

    # do some voodoo magic lol
    figure.patch.set_facecolor('#1a1d27')
    axis.set_facecolor('#0f1117')
    axis.set_title(title,    color='#e2e8f0', fontsize=12, pad=10)
    axis.set_xlabel(x_label, color='#64748b', fontsize=10)
    axis.set_ylabel(y_label, color='#64748b', fontsize=10)
    axis.tick_params(colors='#64748b')
    axis.grid(True, color='#1e2130', linewidth=0.8)
    
    for spine in axis.spines.values():
        spine.set_edgecolor('#2a2d3a')

    line, = axis.plot([], [], marker='o', markersize=3, color=color, linewidth=2)
    plt.tight_layout(pad=1.5)
    figure._line_color = color

    return figure, axis, line


###############################################################################
# Update_line_plot
#
# Redraws the line with new data and saves result to the in-memory store.
#
# ARG: figure, axis, line, x_axis (list), y_axis (list)
def Update_line_plot(figure, axis, line, x_axis, y_axis):
    # wow magic
    cleaned = [
        (y, g) for y, g in zip(x_axis, y_axis)
        if g is not None
    ]
    if not cleaned:
        return
    # some more voodoo
    x_axis, y_axis = zip(*sorted(cleaned))
    line.set_xdata(x_axis)
    line.set_ydata(y_axis)
    axis.relim()
    axis.autoscale_view()

    # honestly Harry Potter was better
    buf = io.BytesIO()
    # ok this was fun to do
    figure.savefig(
        buf,
        format='png',
        dpi=90,
        bbox_inches='tight',
        facecolor=figure.get_facecolor()
    )
    buf.seek(0)

    title = axis.get_title()
    with _store_lock:
        _chart_store[title] = buf.getvalue()


###############################################################################
# Final_line_plot
#
# Marks pipeline as done and keeps the Output process alive so we
# can continue serving the final chart state for whatever amount of seconds.
def Final_line_plot():
    # set the flag so we know chart is stored
    with _store_lock:
        _chart_store['__done__'] = True
    # tell the person at the console that we are done.
    print("[Output]: done")
    print("\n\n\t\t Thank you. You may close the browser tab now.\n\n")
    # eepy meepy
    whatever = 2
    time.sleep(whatever)
