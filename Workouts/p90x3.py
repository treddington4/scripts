from typing import Dict
import click
import configparser
import json
import calendar
import vlc, time
from pynput import keyboard

from datetime import datetime
class vlcplayer:
        
    def __init__(self, link):
        self.skip = 30  # seconds
        self.pause = False
        # creating a vlc instance --fullscreen 
        self._player = vlc.Instance('--aout=alsa')

        # creating a media
        media = self._player.media_new(link)
        # creating a media player object
        self.media_player = self._player.media_player_new()

        self.media_player.set_media(media)

        # setting video scale
        self.media_player.video_set_scale(1)
        
        self.listener = keyboard.Listener(on_press=self.on_press)
        pass

    def on_press(self, key):
        current_time = self.media_player.get_time()
        if key == keyboard.Key.space:
            print("paused? {self.pause}")
            self.pause = not self.pause
            self.media_player.set_pause(self.pause)
        elif key == keyboard.Key.right:
            new_time = (int(current_time/1000) + self.skip) * 1000  # ms
            if new_time > self._duration:
                new_time = self._duration
            self.media_player.set_time(new_time)
            # time.sleep(0.011)
        elif key == keyboard.Key.left:
            new_time = (int(current_time/1000) - self.skip) * 1000  # ms
            # return False  # stop listener
            if current_time < 0:
                current_time = 0
            self.media_player.set_time(new_time)
            # time.sleep(0.011)

    def is_finished(self):
        value = self.media_player.get_time()
        if value == self._duration:
            self._end = datetime.now()
        # print(f"{value}/{duration} {value == duration}")
        return value == self._duration
    
    def play(self):
        self.listener.start()
        self._start = datetime.now()
        # start playing video
        self.media_player.play()

        while not self.media_player.is_playing():
            time.sleep(0.1)

        self._duration=self.media_player.get_length()
        # wait so the video can be played for 

    def summary(self):
        delta = self._end - self._start
        days, seconds = delta.days, delta.seconds
        hours = days * 24 + seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        print(f"Total duration:    {hours}h, {minutes}m, {seconds}s")

        seconds = self._duration // 1000  # to seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        seconds = seconds % 60
        print(f"Expected duration: {hours}h, {minutes}m, {seconds}s")

def play(link):
    P = vlcplayer(link)
    P.play()

    while not P.is_finished():
        time.sleep(0.1)
    P.summary()

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
    
    config.read('settings.ini')
    data = loadJson(config["Settings"]["json_file"] )
    program = get_cur_day(data[config["Program"]["Name"]]["weeks"])
    print_workout_details(data["Workouts"],program)
    play(data["Workouts"][program]["Link"])
    # assume workout done

    increment_workout()
    with open('settings.ini', 'w') as configfile:
        config.write(configfile)

if __name__ == '__main__':
    main()
