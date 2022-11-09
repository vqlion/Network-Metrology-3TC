import json
import matplotlib.pylab as plt
from datetime import *
import matplotlib.dates as mdates
import pandas as pd
from os import listdir
from os.path import isfile, join

## parameters ##

params = ['time_total'] # parameters to consider, up to 6 (restricted by number of colors on plot)
# I'd recommend one parameter at a time, given that the rolling average is also shown
# some interesting parameters are 'time_total' and 'speed_download'

rolling_window = 60  # the rolling average window : the number of values per mean

cut_highs = 2  # to cut absurd values when considering time_total

colors = ["r", "b", "g", "c", "m", "y", "k"]  # just the plot colors...

xformatter = mdates.DateFormatter('%H:%M') # the format of the dates on the graph

## ##

directory = 'ressources/json_files/' 

files = [f for f in listdir(directory)
         if isfile(join(directory, f))]
data = []
for f in files:
    data.append(json.load(open(directory + f)))
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

fig, axs = plt.subplots(len(data))
for i in range(len(data)):
    for j in range(len(params)):  # loop through every file and every parameter
        tmp_df = pd.DataFrame({'times': times[i], 'val': values[i][j]})
        tmp_df = tmp_df.set_index('times')
        tmp_avg_df = tmp_df.rolling(window=rolling_window).mean()
        
        axs[i].plot(tmp_df, color=colors[j], label="Total response time from the server")
        axs[i].plot(tmp_avg_df, color=colors[j + 1],
                        label=f"Rolling average, window = {rolling_window}")
        # plot the given parameter and its rolling average
        axs[i].grid()
        axs[0].legend()
        axs[i].set_title(f"Date: {times[i][0].date()}", fontsize=8)
        plt.gcf().axes[i].xaxis.set_major_formatter(xformatter)

fig.text(0.5, 0.04, 'Time of the day', ha='center')
fig.text(0.04, 0.5, 'Response time from server (s)', va='center', rotation='vertical')
fig.suptitle("Response time from www.marmiton.org over different days, depending on the hour of the day")
# some formatting to make the plot look nice !

plt.show()
