import json
import matplotlib.pylab as plt
from datetime import *
import matplotlib.dates as mdates
import pandas as pd
from os import listdir
from os.path import isfile, join

## parameters ##
# parameters to consider, up to 6 (restricted by number of colors on plot)
params = ['time_total']
# I'd recommend one parameter at a time, given that the rolling average is also shown
# Interesting parameters are 'time_total' and 'speed_download'

rolling_window = 120  # the rolling average window : the number of values per mean

cut_highs = 2  # to cut absurd values when considering time_total

colors = ["r", "b", "g", "c", "m", "y", "k"]  # just the plot colors...

# the format of the dates on the graph
xformatter = mdates.DateFormatter('%H:%M')

## ##

files = [f for f in listdir('results_json/')
         if isfile(join('results_json/', f))]
data = []
for f in files:
    data.append(json.load(open('results_json/' + f)))
# load the json files and store them in an array

times = [[] for i in range(len(data))]
values = [[[0.5 for k in range(len(data[j]))] for i in range(
    len(params))] for j in range(len(data))]

# goes through every line of the json file, and gets its time and the requested parameters in lists so they can be used later
for i in range(len(data)):
    for j in range(len(data[i])):
        times[i].append(datetime.strptime(
            data[i][j][1]["timestamp"], "%Y-%m-%dT%H:%M:%S"))  # stores the timestamps in the right format at the right place
        for k in range(len(params)):
            # check if the value is absurd
            if (not (params[k] == 'time_total' and (data[i][j][0][params[k]] > cut_highs or data[i][j][0][params[k]] < 0.01))):
                values[i][k][j] = data[i][j][0][params[k]]

fig, axs = plt.subplots(int(len(data) / 2), len(data) - int(len(data) / 2))
# create a plot window

for i in range(len(data)):
    for j in range(len(params)):  # loop through every file and every parameter
        row = 0
        col = i
        if (i >= int(len(data) / 2)):
            row = 1
            col = i - int(len(data) / 2)
        # to position the graph at the right place

        tmp_df = pd.DataFrame({'times': times[i], 'val': values[i][j]})
        tmp_df = tmp_df.set_index('times')
        tmp_avg_df = tmp_df.rolling(window=rolling_window).mean()

        axs[row, col].plot(tmp_df, color=colors[j], label=params[j])
        axs[row, col].plot(tmp_avg_df, color=colors[j + 1],
                           label=f"running avg of {params[j]}")

        axs[row, col].grid()
        axs[row, col].legend()
        axs[row, col].set_title(f"values for {times[i][0].date()}", fontsize=8)
        plt.gcf().axes[i].xaxis.set_major_formatter(xformatter)

plt.gcf().axes[len(data)].xaxis.set_major_formatter(xformatter)

plt.show()
