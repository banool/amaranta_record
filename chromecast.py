#!/usr/bin/env python

import pychromecast

from time import time

from speaker import Speaker


DINING_ROOM = "Dining Room Speaker"
LIVING_ROOM = "Living Room"
COMMON_SPACE = "Common Space"

ALL_SPEAKERS = [DINING_ROOM, LIVING_ROOM, COMMON_SPACE]

DISPLAY_NAME = "Default Media Receiver"

LAST_GET_ACTIVE_CAST_OBJECT_TIME = 0
LAST_ACTIVE_CAST_OBJECT = None


class ChromecastSpeaker(Speaker):
    def __init__(self, speaker_name):
        self.speaker_name = speaker_name

    def play(self):
        super().play()
        start_chromecast(self.speaker_name)

    def stop(self):
        super().stop()
        stop_chromecast()

    def volume_up(self):
        cast = get_active_cast_object()
        if cast is None:
            return
        cast.volume_up()

    def volume_down(self):
        cast = get_active_cast_object()
        if cast is None:
            return
        cast.volume_down()

    def __str__(self):
        return self.speaker_name


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
    LAST_ACTIVE_CAST_OBJECT = None
