import json
import matplotlib.pylab as plt
from datetime import *


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
f = open("results_04112022.json")
data = json.load(f)

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
params = ["speed_download"]

times = []
values = [[0.5 for i in range(len(data))] for j in range(len(params))]

# goes through every line of the json file, and gets its time and the requested parameters in lists so they can be used later
for i in range(len(data)):
    times.append(datetime.strptime(
        data[i][1]["timestamp"], "%Y-%m-%dT%H:%M:%S"))
    for j in range(len(params)):
        if(not(params[j] == 'time_total' and (data[i][0][params[j]] > 1 or data[i][0][params[j]] < 0.01))):
            values[j][i] = data[i][0][params[j]]

# just the plot colors...
colors = ["r", "b", "g", "c", "m", "y", "k"]

# plots every parameters, function of time
for i in range(len(params)):
    plt.plot(times, values[i], color=colors[i], label=params[i])

plt.legend()
plt.grid()
plt.show()
