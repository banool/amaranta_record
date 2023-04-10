#!/usr/bin/env python

from time import time

import pychromecast

from helpers import STREAM_URL
from speaker import Speaker

LIVING_ROOM = "Living Room TV"

# From Amaranta, kept here for legacy reasons.
DINING_ROOM = "Dining Room Speaker"
COMMON_SPACE = "Common Space"

ALL_SPEAKERS = [DINING_ROOM, LIVING_ROOM, COMMON_SPACE]

# This can't be changed, it's pretty much a harcoded value from the Chromecast.
DISPLAY_NAME = "Default Media Receiver"

LAST_GET_ACTIVE_CAST_OBJECT_TIME = 0
LAST_ACTIVE_CAST_OBJECT = None


class ChromecastSpeaker(Speaker):
    def __init__(self, speaker_name):
        self.speaker_name = speaker_name

    def play(self):
        print(f"Attempting to play to {self.speaker_name}...")
        super().play()
        start_chromecast(self.speaker_name)
        print(f"Playing to {self.speaker_name}!")

    def stop(self):
        print("Stopping...")
        super().stop()
        stop_chromecast()
        print("Stopped")

    def volume_up(self):
        print("Turning volume up...")
        super().volume_up()
        cast = get_active_cast_object()
        if cast is None:
            return
        cast.volume_up()
        super().volume_down()
        print("Turned volume up")

    def volume_down(self):
        print("Turning volume down...")
        cast = get_active_cast_object()
        if cast is None:
            return
        cast.volume_down()
        print("Turned volume down")

    def __str__(self):
        return self.speaker_name


def get_cast_object(speaker_name):
    chromecasts, browser = pychromecast.get_listed_chromecasts(
        friendly_names=[speaker_name]
    )
    if not chromecasts:
        print(f"Failed to find chromecast with name {speaker_name}")
        return None
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
            active[cast.cast_info.friendly_name] = cast

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
        now < LAST_GET_ACTIVE_CAST_OBJECT_TIME + 15
        and LAST_ACTIVE_CAST_OBJECT is not None
    ):
        print("Using cached cast object")
        return LAST_ACTIVE_CAST_OBJECT

    cast = _get_active_cast_object()

    LAST_ACTIVE_CAST_OBJECT = cast
    LAST_GET_ACTIVE_CAST_OBJECT_TIME = now

    if cast:
        print(f"Fetched new cast object: {cast.cast_info.friendly_name}")
    else:
        print("Failed to find cast object, setting it to None")

    return cast


def start_chromecast(speaker_name):
    cast = get_cast_object(speaker_name)
    if cast is None:
        print(f"Cannot start casting to {speaker_name}, could not find device")
        return
    mc = cast.media_controller
    mc.play_media(
        STREAM_URL,
        "audio/ogg",
        title="Record Player",
        thumb="https://picsum.photos/800",
        stream_type="LIVE",
    )
    mc.block_until_active()


def stop_chromecast():
    cast = get_active_cast_object()
    if cast is None:
        return
    mc = cast.media_controller
    cast.quit_app()
    LAST_ACTIVE_CAST_OBJECT = None
    print("Set active cast object to None")
