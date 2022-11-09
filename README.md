# 🌐 Network metrology visualisation 🌐
MET Project in 3TC : analysis of the metrics of a website
This is a school project I have done as part of a course in the Telecommunication department at INSA Lyon.

## 📈 Visualize the measurements of the metrics of a website 📈

The metrics are measured with a curl command. This command gets a website's page, as well as some useful information.
The principal information considered is the total time to download the website's page.
I also recommand checking the [curl documentation page](https://curl.se/docs/manpage.html).

It simulates an user going in a browser and updating the website's page every 30s, with a limit rate of 1000 kilobytes/s.

## 💻 Curl command 💻
The command is the following :

```bash
echo "[[" >> results.json && while true; do curl --limit-rate 1000K --write-out %{json} www.example.com -o saved >> results.json && echo ",{\"timestamp\": \"$(date +%FT%T)\"}],[" >> results.json; sleep 30; done
```
- The ```--limit-rate 1000K``` part limits the rate to have somewhat regular measures.
- The ```--write-out %{json}``` part is to tell curl to output the results in a json format.
- The ```echo ",{\"timestamp\": \"$(date +%FT%T)\"}],[" >> results.json``` part adds a timestamp to the data, to be able to plot it with python.

This commands generates a json file located in the current directory. The file is formatted to be an array.

To make the output file an array, you have to run the following command after stopping the looping command :

```sed -i '$ s/..$//' results.json && echo ']' >> results.json```
(to make sure the format of the json file is correct).

### ⚠️ Warning ⚠️
This is a ```while true``` command, which means it will run forever, as long as you don't stop it. You have to stop it at some point (a simple ctrl+C will do). Don't forget to type the second command after you stop it! (see above)

## 💻 Usage 💻
The [main.py](main.py) script reads through every json file in the [json_files](ressources/json_files/) directory and plots the results and the rolling average. You can change the parameters and the directory of the json files directly in the python script.
You can add parameters to plot, and change the rolling average window.

Run the python script to get the plots. Make sure you have all the librairies installed.

There are some example of the graphs you can produce in the [output_graphs](ressources/output_graphs/) directory. Those are the plots I produced for the project, measuring the website www.marmiton.org.
