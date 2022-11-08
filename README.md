
# 🌐 Network metrology visualisation 🌐
MET Project in 3TC : analysis of the metrics of a website
This is a school project I have done as part of my course in TC department at INSA Lyon.

## Visualize the measurements of the metrics of a website.

The metrics are measured with a curl command. This command gets a website's page, as well as some useful information.
The principal information considered is the total time to download the website's page.
I also recommand checking the [curl documentation page](https://curl.se/docs/manpage.html).

It simulates an user going in a browser and updating the website's page every 30s, with a limit rate of 1000 kilobytes/s.

## Curl command 
The curl command used is the following :

```
while true; do curl --limit-rate 1000K --write-out %{json} www.example.com -o saved >> results.json && echo ",{\"timestamp\": \"$(date +%FT%T)\"}],[" >> results.json; sleep 30; done
```
The ```--limit-rate 1000K``` part limits the rate to have somewhat regular measures.
The ```--write-out %{json}``` is to tell curl to output the results in a json format.
The ```echo ",{\"timestamp\": \"$(date +%FT%T)\"}],[" >> results.json``` part adds a timestamp to the data, to be able to plat it later with python.

This commands generates a json file located in the current directory. The file is formatted to be an array.

### ⚠️ Multiple warnings ⚠️
- this is a ```while true``` command, which means it'll run forever, as long as you don't stop it. You have to stop it at some point (a simple ctrl+C will do)
- the output json file isn't quite an array. You have to format it a bit for it to become a complete array. Just **add two brackets at the beginning, and make sur the end is also a double bracket**.

## Usage
The [main.py](main.py) script reads through every json file in the [results_json](results_json) directory and plots the results and the rolling average. You can change the parameters directly in the python script.
You can add parameters to plot, and change the rolling average window.

Just run the python script to get the plots. Make sure you have all the librairies installed.

There is data in the results directories, these are the results of my measurements over www.marmiton.org :)
