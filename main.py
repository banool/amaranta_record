#!/usr/bin/env python

import keyboard
import pychromecast
import socket
import subprocess

from contextlib import suppress
from functools import lru_cache, partial, update_wrapper
from time import sleep, time


PORT = 9001
STREAM_FILENAME = "example1.ogg"
ICES_CONFIG_PATH = "/etc/ices.xml"
ICECAST_CONFIG_PATH = "/etc/icecast2/icecast.xml"

DINING_ROOM = "Dining Room Speaker"
LIVING_ROOM = "Living Room"
COMMON_SPACE = "Common Space"

ALL_SPEAKERS = [DINING_ROOM, LIVING_ROOM, COMMON_SPACE]

DISPLAY_NAME = "Default Media Receiver"

LAST_GET_ACTIVE_CAST_OBJECT_TIME = 0
LAST_ACTIVE_CAST_OBJECT = None


###
# Helpers
###

def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    return s.getsockname()[0]
    s.close()


IP = get_local_ip()
STREAM_URL = f"http://{IP}:{PORT}/{STREAM_FILENAME}"

print(f"STREAM_URL: {STREAM_URL}")


def wrapped_partial(func, *args, **kwargs):
    partial_func = partial(func, *args, **kwargs)
    update_wrapper(partial_func, func)
    return partial_func


def start_process(args, daemon=False):
    kwargs = {}
    if daemon:
        kwargs["start_new_session"] = True
    p = subprocess.Popen(args, **kwargs)
    if daemon:
        del p
    else:
        p.communicate()


def get_cast_object(speaker):
    chromecasts, browser = pychromecast.get_listed_chromecasts(friendly_names=[speaker])
    cast = chromecasts[0]
    cast.wait()
    return cast


def _get_active_cast_object():
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=ALL_SPEAKERS[:]
    )

    active = {}
    for cast in chromecasts:
        cast.wait()
        if cast.status.display_name == DISPLAY_NAME:
            active[cast.device.friendly_name] = cast

    if COMMON_SPACE in active:
        print(f"Active speaker: {COMMON_SPACE}")
        return active[COMMON_SPACE]

    if LIVING_ROOM in active:
        print(f"Active speaker: {LIVING_ROOM}")
        return active[LIVING_ROOM]

    if DINING_ROOM in active:
        print(f"Active speaker: {DINING_ROOM}")
        return active[DINING_ROOM]

    return None


def get_active_cast_object():
    global LAST_GET_ACTIVE_CAST_OBJECT_TIME
    global LAST_ACTIVE_CAST_OBJECT
    now = int(time())
    if (
        now < LAST_GET_ACTIVE_CAST_OBJECT_TIME + 5
        and LAST_ACTIVE_CAST_OBJECT is not None
    ):
        print("Using cached cast object")
        return LAST_ACTIVE_CAST_OBJECT

    cast = _get_active_cast_object()

    print("Fetched new cast object")

    LAST_ACTIVE_CAST_OBJECT = cast
    LAST_GET_ACTIVE_CAST_OBJECT_TIME = now

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


def start_chromecast(speaker):
    cast = get_cast_object(speaker)
    mc = cast.media_controller
    mc.play_media(STREAM_URL, "audio/ogg")
    mc.block_until_active()


def stop_chromecast():
    cast = get_active_cast_object()
    if cast is None:
        return
    mc = cast.media_controller
    cast.quit_app()


###
# Functions to bind to keys.
###


def play(speaker):
    stop()
    start_ices()
    if speaker:
        start_chromecast(speaker)
        print(f"Started casting to {speaker}")
    else:
        print("Started stream but didn't ask a chromecast to subscribe")
    # TODO: Flash LED


def stop():
    LAST_ACTIVE_CAST_OBJECT = None
    stop_chromecast()
    stop_all_ices()
    print("Stopped casting")


def volume_up():
    cast = get_active_cast_object()
    if cast is None:
        return
    cast.volume_up()


def volume_down():
    cast = get_active_cast_object()
    if cast is None:
        return
    cast.volume_down()


###
# Keyboard bindings
###


BIND_MAP = {
    "6": wrapped_partial(play, None),
    "7": wrapped_partial(play, DINING_ROOM),
    "8": wrapped_partial(play, LIVING_ROOM),
    "9": wrapped_partial(play, COMMON_SPACE),
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


def main():
    keyboard.hook(delegator)
    keyboard.wait()


if __name__ == "__main__":
    main()
