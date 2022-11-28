""""Dog event tracking, Designed to interface with the exported data from:
https://dognote.app/

"""
import json
import click
from datetime import datetime

import matplotlib.pyplot as plt
import matplotlib.dates as pld
import matplotlib.colors as mcolors
import numpy as np

def parsefile(file:str):
    print(file)
    eventlist = dict()
    input_file = open(file)
    json_array = json.load(input_file)

    for item in json_array:
        event = item["Event"]
        date = datetime.fromisoformat(item['Time'][:-6])
        time = date.time()
        time = 24 * ((time.second + 60 * (time.minute + 60 * time.hour)) / (24 * 60 * 60))
        day = date.date()

        try:
            eventlist[event]["day"].append(day)
            eventlist[event]["time"].append(time)
        except:
            eventlist[event] = {"day":[day],"time":[time]}
    return eventlist


def plot(events, col):
    """Plot all events with a specific color

    Args:
        events (_type_): dictionary of arrays with keys day/time
        col (_type_): _description_
    """
    try:
        plt.scatter(events["day"],events["time"], color=col)
    except:
        raise "Invalid Dictionary format"
    

def setup_chart(title:str):
    """Initializes the matplotlib chart for viewing
    Args:
        title (str): Title for the chart
    """
    plt.xlabel('Date')
    plt.ylabel('Time (hours 0-24)')  
    plt.title(title)
    plt.gcf().autofmt_xdate()

    myFmt = pld.DateFormatter('%m-%d')
    plt.gca().xaxis.set_major_formatter(myFmt)
    plt.ylim([0, 24])
    plt.yticks(np.arange(0, 24, 1))
    plt.grid(axis = 'y')


@click.command()
@click.argument('input_file',
                type=click.Path(exists=True, file_okay=True, dir_okay=True,
                                writable=False, readable=True, resolve_path=True))


def main(input_file):
    # parse the events
    events = parsefile(input_file)

    setup_chart("Logged Events")
    legend={
        "Pee":"orange", 
        "Remove water":"blue", 
        "Food":"green",
        "Poop":"brown"
        }

    # plot the data
    for event in legend:
        color = legend[event]
        plot(events[event], color)

    plt.legend(legend.keys(),bbox_to_anchor=(1.00, 1.02), loc='upper left')
    plt.tight_layout()
    
    plt.show()


if __name__ == '__main__':
    main()


