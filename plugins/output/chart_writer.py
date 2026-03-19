# SDA - Project, Spring 2026
#
# Taha Tahir     [24L-0677]
# Muhammad Rafay [24L-0649]

"""
> plugins/output/chart_writer.py

> Manages the actual writing out of te charts required on the dashboard to memeory
"""

from .chart_implementations import Setup_line_plot, Update_line_plot, Final_line_plot

###############################################################################
# Chart Writer Class
#
# Manages the calls to the setup, update, and terminate functions for charts
# as defined in the implementation file
class ChartWriter:

    def __init__(self):
        self.charts = {}
    
    ###############################################################################
    # render charts
    #
    # Chaecks if the chart exists. If it does not, then set it up.
    # and in both cases, update it with the latest data.
    #
    # ARG: title, x_(label, axis), y_(label, axis)
    # RET:
    def render(self,title,x_label,y_label,x_axis, y_axis):
        # check existance
        if title not in self.charts:
            figure,axis,line = Setup_line_plot(title,x_label,y_label)
            # init the dict if it does not exist
            self.charts[title] = {
                "figure": figure,
                "axis" : axis,
                "line" : line,
                "x_points" : [],
                "y_points" : []
            }
        
        # assign values to the chart labels and axes
        chart_already_created = self.charts[title]
        chart_already_created["x_points"].append(x_axis)
        chart_already_created["y_points"].append(y_axis)

        # assign values to the chart's newest point
        Update_line_plot(
            chart_already_created["figure"],
            chart_already_created["axis"],
            chart_already_created["line"],
            chart_already_created["x_points"],
            chart_already_created["y_points"]
        )

    ###############################################################################
    # finalize
    # 
    # lets you kill the chart updation cycle
    # VERY useless wrapper around the chart_implementation function for finalization
    # But that is what SDA is about yayyyyyy.
    def finalize(self):
        Final_line_plot()
