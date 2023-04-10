import functools
import socket
import subprocess


def wrapped_partial(func, *args, **kwargs):
    partial_func = functools.partial(func, *args, **kwargs)
    functools.update_wrapper(partial_func, func)
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


def get_local_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", 80))
    out = s.getsockname()[0]
    s.close()
    return out


IP = get_local_ip()
PORT = 9001
STREAM_FILENAME = "recordplayer.ogg"
STREAM_URL = f"http://{IP}:{PORT}/{STREAM_FILENAME}"

print(f"Working with stream {STREAM_URL}")
