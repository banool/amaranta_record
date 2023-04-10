# Amaranta Record

Code and configs related to our record player setup at Amaranta.

Read on for a guide on how to set this up.

## Install dependencies

First, install these:
- Python 3.7 (pip and virtualenv)
- ices2
- icecast

```
sudo apt install python3-pip python3-venv ices2 icecast2
```

If prompted, do not configure icecast2, we will use our own files.

## Copy code into server
You can copy this full repo over into the server like this:
```
./copy.sh dport@pi
```

## Set up virtual env
In the server:
```
cd /opt/amaranta_record
python3 -m venv myvenv --system-site-packages
. myvenv/bin/activate
pip install -r requirements.txt
```

We use `--system-site-packages` because on the Raspberry Pi, some packages are already installed at the system level, e.g. gpiozero.

## Copy configs 

Move the following files in `configs/` into place:
- ices.xml -> /etc/ices.xml
- icecast.xml -> /etc/icecast2/icecast.xml
- amaranta_record.service -> /etc/systemd/system/amaranta_record.service
- icecast.service -> /etc/systemd/system/icecast.service

## Update configs
You'll have to update `/etc/ices.xml` to use the correct audio input. So instead of `hw:1,0` it might be `hw:3,0`. You can figure it out by using this command: `aplay -l`.

## Start the service

Do this once you've copied all the config files in.

```
sudo mkdir -p /var/log/icecast2
sudo mkdir -p /var/log/ices
sudo chown nobody:nogroup /var/log/icecast2/
```
```
sudo systemctl daemon-reload
```
```
sudo systemctl enable amaranta_record
sudo systemctl start amaranta_record
```
```
sudo systemctl enable icecast
sudo systemctl start icecast
```

Done!

---

This section contains helpful tips for debugging / production.

## Discovering cast destinations
To find cast destinations do this. First, open up a python shell in the virtual environment. Then:
```
import pychromecast
services, browser = pychromecast.discovery.discover_chromecasts()
```

## Production
To check what's going on (look at the logs) run these:

```
# ices2
cat /var/log/ices/ices.log
# icecast
sudo journalctl -u icecast -f
# amaranta_record script
sudo journalctl -u amaranta_record -f
```
