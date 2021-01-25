#!/usr/bin/env python

import argparse
import keyboard
import pychromecast
import subprocess

from contextlib import suppress
from time import sleep


IP = "192.168.86.35"
PORT = 9001
STREAM_FILENAME = "example1.ogg"
ICES_CONFIG_PATH = "/etc/ices.xml"
ICECAST_CONFIG_PATH = "/etc/icecast2/icecast.xml"

###
# Helpers
###


def start_process(args, daemon=False):
    p = subprocess.Popen(args)
    if not daemon:
        p.communicate()


def get_cast_object():
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=["Dining Room speaker"]
    )
    cast = chromecasts[0]
    cast.wait()
    return cast


###
# Casting functions
###


def start_ices():
    start_process(["ices2", ICES_CONFIG_PATH], daemon=True)


def start_icecast():
    start_process(["icecast2", "-c", ICECAST_CONFIG_PATH], daemon=True)


def stop_all_ices():
    start_process(["pkill", "ices2"])


def stop_all_icecast():
    start_process(["pkill", "icecast2"])


def start_chromecast():
    cast = get_cast_object()
    mc = cast.media_controller
    mc.play_media(f"http://{IP}:{PORT}/{STREAM_FILENAME}", "audio/ogg")
    mc.block_until_active()


def stop_chromecast():
    cast = get_cast_object()
    mc = cast.media_controller
    cast.quit_app()


###
# Functions to bind to keys.
###


def play():
    stop()
    start_ices()
    start_chromecast()
    print("Started casting")
    # TODO: Flash LED


def stop():
    stop_chromecast()
    stop_all_ices()
    print("Stopped casting")


def volume_up():
    cast = get_cast_object()
    cast.volume_up()


def volume_down():
    cast = get_cast_object()
    cast.volume_down()


###
# Keyboard bindings
###


BIND_MAP = {
    "2": play,
    "5": stop,
    "a": volume_down,
    "b": volume_up,
}


def delegator(event):
    if event.event_type == "down":
        return
    func = BIND_MAP.get(event.name)
    if func is None:
        print(f"Ignoring key input: {event.name} ({event.scan_code})")
    else:
        print(f"Running function: {func.__name__}")
        func()


###
# Main
###

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--location", default="Common Space")
    args = parser.parse_args()


def main():
    keyboard.hook(delegator)
    keyboard.wait()


if __name__ == "__main__":
    main()
