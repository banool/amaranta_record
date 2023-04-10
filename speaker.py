###
# Speaker abstraction
###

from helpers import start_process

ICES_CONFIG_PATH = "/etc/ices.xml"


# This can be used just for starting and stopping the ices stream. Other Spekaers can
# then build on top of this to do more stuff, like chromecasting.
class Speaker:
    def play(self):
        start_ices()

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

    def play(speaker):
        if self.active_speaker:
            self.active_speaker.stop()
        self.active_speaker = speaker
        self.active_speaker.play()

    def stop():
        self.active_speaker.stop()
        self.active_speaker = None

    def volume_up():
        self.active_speaker.volume_up()

    def volume_down():
        self.active_speaker.volume_down()


SPEAKER_MANAGER = SpeakerManager()
