# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> plugins/output/web/server.py

> Makes a static HTML page to display everything in one place
> Obviously output also goin to terminal, but this gives us a
> unified interface for the charts.
> To not be blocking, it runs as a daemon from inside the Output process.
> should auto-open the browser on startup. If not, then, please manually open this link:
    http://localhost:5000
"""

import json
import logging
import os
import threading
import time
import webbrowser

# helps us to serve the page on localhost
from flask import Flask, Response, request, render_template, send_from_directory

# gets us the current working dir
_HERE = os.path.dirname(os.path.abspath(__file__))


###############################################################################
# start server thread
#
# Entry point so needs to be called inside a threading.Thread.
# makes things harder, but this is the only way to it without
# overcomplications. Also registers all Flask (our hoster) routes,
# opens the browser, and opens a new tab to this page starts the app.
#
# ARG: chart_store (dict), queue_store (dict), store_lock, max_q_size (int)
# RET: None (force a None)
def start_server_thread(chart_store: dict, queue_store: dict, store_lock, max_q_size: int) -> None:

    # this is from the docs.
    app = Flask(
        __name__,
        template_folder = os.path.join(_HERE, 'templates'),
        static_folder   = os.path.join(_HERE, 'static')
    )
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

    ##########
    # ROUTES #
    ##########

    # Short little flask tutorial, cuz this stuff is hard. Writing this for myself
    #
    # Flask 'routes' map URLs to Python functions using the @app.route() decorator.
    # so basically:
    #                (URL) ------[@app.route()]--------> (Python Function)
    #
    # Kind like:
    # 
    # > app = Flask(__name__)
    # > @app.route('/hello') 
    # 
    # This maps a URL like 'http://localhost:5000/hello' to a python func like:
    # > def hello():
    # >     return 'Hello, World!'
    # When the user visits /hello, Flask calls that function and returns its response.

    ###########################################################################
    # /
    # Serves the main dashboard HTML page.
    @app.route('/')
    def index():
        return render_template('index.html')

    ###########################################################################
    # /config
    # Returns the parsed config.json as JSON for the dashboard to render.
    @app.route('/config')
    def config_endpoint():
        try:
            with open('config.json', encoding='utf-8') as f:
                return Response(
                    f.read(),
                    mimetype='application/json'
                )
        except FileNotFoundError:
            return Response(
                '{}',
                mimetype='application/json'
            )

    ###########################################################################
    # /chart.png
    # Returns the latest in-memory PNG buffer for the requested chart title.
    # Returns 204 if the chart hasn't been drawn yet.
    @app.route('/chart.png')
    def chart_png():
        title = request.args.get('title', '')
        with store_lock:
            data = chart_store.get(title)
        if data is None:
            return Response(status=204)
        return Response(
            data,
            mimetype='image/png',
            headers={
                'Cache-Control': 'no-store, no-cache',
                'Pragma': 'no-cache'
            }
        )

    ###########################################################################
    # /backpressure
    # Polls all registered queue sizes and returns a snapshot.
    @app.route('/backpressure')
    def backpressure():
        snapshot = {}
        for label, q in queue_store.items():
            try:
                snapshot[label] = q.get_size()
            except Exception:
                snapshot[label] = 0
        return Response(
            json.dumps({
                'queues': snapshot,
                'max': max_q_size
            }),
            mimetype='application/json'
        )

    ###########################################################################
    # /latest
    # Returns the most recently processed packet for the current packet panel.
    @app.route('/latest')
    def latest():
        with store_lock:
            data = chart_store.get('__latest__')
        if data is None:
            return Response(
                '{}',
                mimetype='application/json'
            )
        return Response(
            json.dumps(data),
            mimetype='application/json'
        )

    ###########################################################################
    # /status
    # Returns whether the pipeline has finished processing.
    @app.route('/status')
    def status():
        with store_lock:
            done = bool(chart_store.get('__done__', False))
        return Response(json.dumps({'done': done}), mimetype='application/json')

    ###########################################################################
    # _watch_for_done
    # Keeps the server alive for a few seconds after pipeline completes, then exits.
    def _watch_for_done():
        while True:
            time.sleep(2)
            with store_lock:
                if chart_store.get('__done__'):
                    time.sleep(2)
                    os._exit(0)

    threading.Thread(target=_watch_for_done, daemon=True).start()

    ###########################################################################
    # _open_browser
    # Opens the dashboard in the default browser after Flask is ready.
    def _open_browser():
        time.sleep(1.5)
        webbrowser.open('http://localhost:5000')

    # begin the thread
    threading.Thread(target=_open_browser, daemon=True).start()

    # run the app
    app.run(port=5000, threaded=True, use_reloader=False)
