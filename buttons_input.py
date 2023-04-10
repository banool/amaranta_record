# This file contains the logic for calling functions based on keyboard input.

import signal

from gpiozero import Button

from chromecast import LIVING_ROOM, ChromecastSpeaker
from helpers import wrapped_partial
from speaker import SPEAKER_MANAGER, Speaker


def run():
    play_button = Button(5)
    stop_button = Button(6)
    volume_up_button = Button(13)
    volume_down_button = Button(19)

    play_button.when_pressed = wrapped_partial(
        SPEAKER_MANAGER.play, ChromecastSpeaker(LIVING_ROOM)
    )
    stop_button.when_pressed = SPEAKER_MANAGER.stop
    volume_up_button.when_pressed = SPEAKER_MANAGER.volume_up
    volume_down_button.when_pressed = SPEAKER_MANAGER.volume_down

    print("Listening for button presses...")
    signal.pause()
