from typing import Dict
import click
import configparser
import json
import calendar
import vlc, time

def play(link):
    # export PYTHON_VLC_MODULE_PATH=/usr/lib/x86_64-linux-gnu/vlc/plugins
    # creating a vlc instance
    player = vlc.Instance('--fullscreen --aout=alsa')

    # creating a media
    media = player.media_new(link)
    # creating a media player object
    media_player = player.media_player_new()

    media_player.set_media(media)

    # setting video scale
    media_player.video_set_scale(1)

    # start playing video
    media_player.play()

    # wait so the video can be played for 5 seconds
    # irrespective for length of video
    time.sleep(5)

config = configparser.ConfigParser()

def loadJson(input_file: str)->Dict:
    f = open(input_file)
    return json.load(f)

def get_workout_attr():
    day = int(config["Program"]["day"])
    week = int(config["Program"]["week"])
    return (day, week)

def get_cur_day(weeks:dict):
    day, week = get_workout_attr()
    print(f"{calendar.day_name[day]} - Week: {week+1} day: {day+1} Total Days: {day+(week*7)+1}")
    return weeks[f"{week+1}"][day]


def print_workout_details(workouts:dict, workout:str):
    print(f"\t{'Class':9}: {workout}")
    workout= workouts[f"{workout}"]
    for key in workout.keys():
        if type(workout[key]) is list:
            if len(workout[key]) == 0:
                print(f"\t{key:9}: None")
            else:
                print(f"\t{key:9}: {','.join(workout[key])}")
        else:
            print(f"\t{key:9}: {workout[key]}")


def increment_workout():
    day, week = get_workout_attr()
    day += 1
    if day > 6:
        day=0
        week += 1
    config["Program"]["week"] = f"{week}"
    config["Program"]["day"] = f"{day}"
    return day, week


def decrement_workout():
    day, week = get_workout_attr()
    day -= 1
    if day < 0:
        day=6
        week -= 1
    if week < 0:
        day = 0
        week = 0
    config["Program"]["week"] = f"{week}"
    config["Program"]["day"] = f"{day}"
    return day, week


def main():
    # play()
    config.read('settings.ini')
    data = loadJson(config["Settings"]["json_file"] )
    program = get_cur_day(data[config["Program"]["Name"]]["weeks"])
    print_workout_details(data["Workouts"],program)
    # assume workout done

    increment_workout()
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

if __name__ == '__main__':
    main()
