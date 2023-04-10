###
# Speaker abstraction
###

import time

import requests

from helpers import PORT, STREAM_FILENAME, start_process

ICES_CONFIG_PATH = "/etc/ices.xml"


# This can be used just for starting and stopping the ices stream. Other Spekaers can
# then build on top of this to do more stuff, like chromecasting.
class Speaker:
    def play(self):
        start_ices()
        count = 0
        # https://stackoverflow.com/a/32659310/3846032
        url = f"http://127.0.0.1:{PORT}/status-json.xsl"
        print("Waiting for stream to come up...")
        while count < 5:
            resp = requests.get(url, timeout=0.5)
            if resp.json()["icestats"].get("source"):
                print("Stream came up!")
                return
            time.sleep(0.5)
            count += 1
        raise RuntimeError(f"Stream failed to start")

    def stop(self):
        stop_all_ices()

    def volume_up(self):
        pass

    def volume_down(self):
        pass


def start_ices():
    start_process(["ices2", ICES_CONFIG_PATH], daemon=True)


def stop_all_ices():
    start_process(["pkill", "ices2"])


# Provides a common interface for calling functions on the active speaker, if any.
class SpeakerManager:
    def __init__(self):
        self.active_speaker = None

    def play(self, speaker):
        if self.active_speaker:
            self.active_speaker.stop()
        self.active_speaker = speaker
        try:
            self.active_speaker.play()
        except Exception as e:
            print(
                f"Failed to play, stopping and setting active speaker to None again: {e}"
            )
            self.active_speaker.stop()
            self.active_speaker = None

    def stop(self):
        if not self.active_speaker:
            print("stop: No active speaker, doing nothing")
            return
        self.active_speaker.stop()
        self.active_speaker = None

    def volume_up(self):
        if not self.active_speaker:
            print("volume_up: No active speaker, doing nothing")
            return
        self.active_speaker.volume_up()

    def volume_down(self):
        if not self.active_speaker:
            print("volume_down: No active speaker, doing nothing")
            return
        self.active_speaker.volume_down()


SPEAKER_MANAGER = SpeakerManager()
