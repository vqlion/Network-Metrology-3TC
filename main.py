import json
import matplotlib.pylab as plt
from datetime import *
import matplotlib.dates as mdates
import pandas as pd
from os import listdir
from os.path import isfile, join

#### vql's spaghetti code, unprecedented genius gift of god below ####
# just kiding have fun reading this bs


# This script is used to analyse json data from a curl command
# you may check the complete doc here https://curl.se/docs/manpage.html, basically curl is to fetch a website's page, among many other useful info
# here is the complete command (shell script)

# while true; do curl --limit-rate 1000K --write-out %{json} https://www.marmiton.org -o saved >> results.json && echo ",{\"timestamp\": \"$(date +%FT%T)\"}],[" >> results.json; sleep 30; done

# this gets the loading time of any webiste you put in parameter and outputs it (among many other stuff) to a json file
# then I added a bit of formating so it scales over time: the json file becomes an array with timestamps so we can read it and plot it!
# !!! The command is infinite until you stop it: it is a 'while true' command. It gives a result every 30 seconds by default, with a limit rate of 100kbits/s for each instruction

# load the json file

files = [f for f in listdir('results_json/')
         if isfile(join('results_json/', f))]
data = []
for f in files:
    data.append(json.load(open('results_json/' + f)))

### interesting parameters ###

# speed_download
# time_connect
# time_appconnect
# time_pretransfer
# time_namelookup
# time_starttransfer
# time_redirect
# time_total

# parameters to consider, up to 7 (restricted by number of colors on plot)
params = ['time_total']

times = [[] for i in range(len(data))]

values = [[[0.5 for k in range(len(data[j]))] for i in range(
    len(params))] for j in range(len(data))]

# goes through every line of the json file, and gets its time and the requested parameters in lists so they can be used later
for i in range(len(data)):
    for j in range(len(data[i])):
        times[i].append(datetime.strptime(
            data[i][j][1]["timestamp"], "%Y-%m-%dT%H:%M:%S"))
        for k in range(len(params)):
            if (not (params[k] == 'time_total' and (data[i][j][0][params[k]] > 2 or data[i][j][0][params[k]] < 0.01))):
                values[i][k][j] = data[i][j][0][params[k]]


# just the plot colors...
colors = ["r", "b", "g", "c", "m", "y", "k"]

# plots every parameters, function of time

fig, axs = plt.subplots(int(len(data) / 2), len(data) - int(len(data) / 2))

xformatter = mdates.DateFormatter('%H:%M')
for i in range(len(data)):
    for j in range(len(params)):
        row = 0
        col = i
        if(i >= int(len(data) / 2)): 
            row = 1
            col = i - int(len(data) / 2)
        tmp_df = pd.DataFrame({'times': times[i], 'val': values[i][j]})
        tmp_df = tmp_df.set_index('times')
        tmp_avg_df = tmp_df.rolling(window=120).mean()

        axs[row, col].plot(tmp_df, color=colors[j], label=params[j])
        axs[row, col].plot(tmp_avg_df, color=colors[j + 1], label=f"running avg of {params[j]}")
        axs[row, col].grid()
        axs[row, col].legend()
        axs[row, col].set_title(f"values for {times[i][0].date()}", fontsize=8)
        plt.gcf().axes[i].xaxis.set_major_formatter(xformatter)

plt.legend()
plt.grid()
plt.show()
