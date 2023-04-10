# This file contains the logic for calling functions based on keyboard input.

import keyboard

from chromecast import LIVING_ROOM, ChromecastSpeaker
from helpers import wrapped_partial
from speaker import SPEAKER_MANAGER, Speaker

KEYBOARD_BIND_MAP = {
    "7": wrapped_partial(SPEAKER_MANAGER.play, ChromecastSpeaker(LIVING_ROOM)),
    # This is for just kicking off the stream without casting.
    "6": wrapped_partial(SPEAKER_MANAGER.play, Speaker()),
    "5": SPEAKER_MANAGER.stop,
    "a": SPEAKER_MANAGER.volume_up,
    "b": SPEAKER_MANAGER.volume_down,
}


def delegator(event):
    if event.event_type == "down":
        return
    func = KEYBOARD_BIND_MAP.get(event.name)
    if func is None:
        print(f"Ignoring key input: {event.name} ({event.scan_code})")
    else:
        print(f"Running function: {func.__name__}")
        func()


def run():
    keyboard.hook(delegator)
    keyboard.wait()
